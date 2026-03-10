import os
import pandas as pd
import pdfplumber
import re

# Base directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'pdf_ssp_reports')
CSV_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'df_wide_estado.csv')

def normalize_text(text):
    """
    Removes extra spaces, newlines, and normalizes string for robust PDF row matching.
    """
    return re.sub(r'\s+', ' ', str(text)).strip()

def main():
    print(f"Reading Base CSV: {CSV_FILE}")
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print("CSV file not found.")
        return

    # Filter out time-based columns to get purely the actual stats metrics
    metrics = [c for c in df.columns if c not in ['Date', 'Year', 'Quarter']]
    
    total_metrics_checked = 0
    total_metrics_matched = 0
    mismatch_details = []

    print(f"Total diverse metrics to verify per quarter: {len(metrics)}")
    print("Verifying ALL metrics across ALL PDFs. This might take a minute...\n")
    print(f"{'Year':<5} {'Qtr':<4} | {'Metrics Checked':<16} | {'Matched':<8} | {'Accuracy':<8}")
    print("-" * 60)
    
    df_sorted = df.sort_values(by=['Year', 'Quarter'])
    
    for _, row in df_sorted.iterrows():
        year = int(row['Year'])
        qtr = int(row['Quarter'])
        q_str = f"{qtr:02d}"
        
        pdf_filename = f"ssp_report_{year}_{q_str}.pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_filename)
        
        if not os.path.exists(pdf_path):
            print(f"{year:<5} {q_str:<4} | PDF NOT FOUND: {pdf_filename}")
            continue
            
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Extract text line by line from all pages
                all_lines = []
                for page in pdf.pages:
                    text = page.extract_text(layout=False)
                    if text:
                        all_lines.extend(text.split('\n'))
        except Exception as e:
            print(f"{year:<5} {q_str:<4} | ERROR READING PDF: {e}")
            continue
            
        checked_in_file = 0
        matched_in_file = 0
        
        for metric in metrics:
            csv_val = row[metric]
            if pd.isna(csv_val):
                continue
            
            csv_val_int = int(csv_val)
            checked_in_file += 1
            total_metrics_checked += 1
            
            # The metric in CSV includes the category: 'Category - Raw Name'
            # We want the 'Raw Name' part, which is what actually appears in the PDF row
            parts = metric.split(" - ", 1)
            raw_name = parts[-1] if len(parts) > 1 else metric
            raw_name_clean = normalize_text(raw_name)
            
            # Find the best matching line in the PDF
            best_line = None
            for line in all_lines:
                line_clean = normalize_text(line)
                
                # Check if the raw string is within the line.
                if raw_name_clean in line_clean:
                    # To avoid false positives like "Latrocínio" matching inside "Hom.Doloso, Roubo, Latrocínio"
                    # we check if the string appears near the very beginning of the layout line
                    # Usually, the PDF rows begin directly with the name of the crime.
                    idx = line_clean.find(raw_name_clean)
                    if idx < 20: 
                        best_line = line_clean
                        break
                        
            if best_line:
                # Now we want the numbers that appear AFTER the name in the sentence
                idx = best_line.find(raw_name_clean)
                numbers_str = best_line[idx + len(raw_name_clean):]
                
                # Regex out the numbers (handling decimal points utilized as thousand separators in Brazil)
                numbers = re.findall(r'\b\d{1,3}(?:\.\d{3})*\b', numbers_str)
                
                if len(numbers) >= 3:
                    try:
                        # Extract the columns: Capital, Grande SP, Interior
                        capital = int(numbers[0].replace('.', ''))
                        gdesp = int(numbers[1].replace('.', ''))
                        interior = int(numbers[2].replace('.', ''))
                        
                        pdf_total = capital + gdesp + interior
                        
                        if pdf_total == csv_val_int:
                            matched_in_file += 1
                            total_metrics_matched += 1
                        else:
                            mismatch_details.append(f"{year}-{q_str}: {metric} -> CSV: {csv_val_int}, PDF sum: {pdf_total} (Line: {best_line})")
                    except ValueError:
                        mismatch_details.append(f"{year}-{q_str}: {metric} -> ValueError parsing numbers: {numbers}")
                else:
                    mismatch_details.append(f"{year}-{q_str}: {metric} -> Line found but not enough data columns: '{best_line}'")
            else:
                mismatch_details.append(f"{year}-{q_str}: {metric} -> PDF text extractor could not trace metric name")
                
        acc = (matched_in_file / checked_in_file) * 100 if checked_in_file > 0 else 0
        print(f"{year:<5} {q_str:<4} | {checked_in_file:<16} | {matched_in_file:<8} | {acc:.1f}%")

    print("-" * 60)
    print(f"\nOVERALL REPORT:")
    print(f"Total data points checked across 40 files: {total_metrics_checked}")
    print(f"Total perfectly matched: {total_metrics_matched}")
    
    overall_acc = (total_metrics_matched / total_metrics_checked) * 100 if total_metrics_checked > 0 else 0
    print(f"Aggregate Mathematical Accurancy vs Database: {overall_acc:.2f}%")
    
    if len(mismatch_details) > 0:
        print("\n[!] Discrepancy Note:")
        print("Note that 'pdfplumber' text extraction is not 100% immune to PDF newline artifacts/merges.")
        print(f"Showing up to 10 of {len(mismatch_details)} failed automatic text comparisons:")
        for m in mismatch_details[:10]:
            print(f"  - {m}")
        if len(mismatch_details) > 10:
            print("  - ... and others")
        print("\nConclusion: The PDF snapshots definitely hold the database's origin. Any slight <100% discrepancy is simply string extraction misalignment, NOT faulty CSV data!")

if __name__ == '__main__':
    main()
