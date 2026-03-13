import sys
import subprocess
import os
import csv

def load_requirements():
    req_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'requirements.txt')
    if not os.path.exists(req_path):
        # Fallback if run from a different directory
        req_path = 'requirements.txt'
    
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            lines = f.readlines()
        py_reqs = []
        for line in lines:
            line = line.strip()
            if line == '# R Dependencies': break
            if line and not line.startswith('#'):
                py_reqs.append(line)
        
        if py_reqs:
            try:
                import requests
                from bs4 import BeautifulSoup
                from playwright.sync_api import sync_playwright
            except ImportError:
                print("Missing python dependencies. Installing from requirements.txt...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", *py_reqs])
                # Playwright requires a separate command to install its browser binaries
                if "playwright" in py_reqs or "playwright" in "\n".join(py_reqs):
                    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

load_requirements()
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Define output path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'raw', 'ssp_data_2016_2025.csv')
PDF_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'pdf_ssp_reports')

def clean_number(value):
    """
    Removes thousand separators (.) from numeric strings.
    Example: "145.598" -> "145598"
    """
    if not value:
        return ""
    # Remove dots that are used as thousand separators
    return value.replace('.', '').strip()

def fetch_and_parse_playwright(year, quarter, page, pdf_dir):
    # Format quarter as 01, 02, etc.
    q_str = f"{quarter:02d}"
    url = f"https://www.ssp.sp.gov.br/assets/estatistica/trimestral/arquivos/{year}-{q_str}.htm"
    pdf_path = os.path.join(pdf_dir, f"ssp_report_{year}_{q_str}.pdf")
    
    print(f"Fetching {url}...")
    try:
        response = page.goto(url, timeout=30000, wait_until="networkidle")
        if not response or not response.ok:
            print(f"  Failed to load page: {response.status if response else 'Unknown Error'}")
            return []
            
        # Optional: ensure layout renders correctly before saving PDF
        page.evaluate("document.body.style.background = 'white';")
        
        # Save page as PDF
        page.pdf(path=pdf_path, format="A4", landscape=True)
        print(f"  Saved PDF to -> {pdf_path}")
        
        html_content = page.content()
    except Exception as e:
        print(f"  Error fetching via Playwright: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    
    if not tables:
        print("  No tables found.")
        return []

    # Find main table
    target_table = None
    max_rows = 0
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) > max_rows:
            max_rows = len(rows)
            target_table = table
            
    if not target_table:
        print("  Main table not found.")
        return []

    rows = target_table.find_all('tr')
    extracted_data = []
    
    # Per-file processing state
    current_category = "Uncategorized"
    
    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_data = []
        for cell in cells:
            text = cell.get_text(strip=True)
            row_data.append(text)
            
        if row_data:
            # Check for ITEM row (Category)
            # Original Column A is at index 0
            if len(row_data) > 1 and row_data[0].strip() == "ITEM":
                current_category = row_data[1].strip()

            # Remove first column (Column A)
            cleaned_row = row_data[1:]
            
            # Skip empty rows
            if not any(cell.strip() for cell in cleaned_row):
                continue
            
            # Identify header row
            is_header = False
            if len(cleaned_row) > 1 and cleaned_row[1] == "Capital":
                is_header = True
                
            if is_header:
                # Return header with special flag
                row_with_meta = ["HEADER", "Category"] + cleaned_row
                extracted_data.append(row_with_meta)
            else:
                # Apply number cleaning to data rows
                # cleaned_row = [Natureza, Capital, ...]
                # Index 0 is Natureza (text), Index 1+ are numbers
                
                # Prepend Category to Natureza to ensure uniqueness
                natureza_unique = f"{current_category} - {cleaned_row[0]}"
                
                formatted_row = [natureza_unique] + [clean_number(val) for val in cleaned_row[1:]]
                
                # Add Year, Quarter, Category
                final_row = [str(year), q_str, current_category] + formatted_row
                extracted_data.append(final_row)
                
    return extracted_data

def main():
    os.makedirs(PDF_DIR, exist_ok=True)
    all_data = []
    header_written = False
    
    with sync_playwright() as p:
        print("Launching Chromium browser for scraping and PDF export...")
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Loop 2016 to 2025
        for year in range(2016, 2026):
            for quarter in range(1, 5):
                file_rows = fetch_and_parse_playwright(year, quarter, page, PDF_DIR)
                
                for row in file_rows:
                    if row[0] == "HEADER":
                        if not header_written:
                            # Extract the dynamic header part from this row
                            # row structure: ["HEADER", "Category", Col1, Col2...]
                            # desired output header: ["Year", "Quarter", "Category", Col1, Col2...]
                            
                            dynamic_headers = row[2:] # specific stats columns
                            
                            # The first column in dynamic_headers is currently 'Ocorrências policiais registradas, por natureza'
                            # Overwrite it with 'metric' as requested by the user
                            if dynamic_headers:
                                dynamic_headers[0] = "Metric"
                                
                            full_header = ["Year", "Quarter", "Category"] + dynamic_headers
                            all_data.append(full_header)
                            header_written = True
                    else:
                        all_data.append(row)
                        
        browser.close()
                    
    print(f"Total rows collected: {len(all_data)}")
    print(f"Writing to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_data)
        
    print("Done. PDF reports saved in:", PDF_DIR)

if __name__ == "__main__":
    main()