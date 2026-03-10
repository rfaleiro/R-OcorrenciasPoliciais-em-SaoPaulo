# Load libraries from requirements.txt
find_reqs <- function() {
  for (d in c(".", "..", "../..", "../../..", "ocorrencias-em-sao-paulo", "ocorrencias-em-sao-paulo/R_Ocorrencias_em_sao_paulo/..")) {
    p <- file.path(d, "requirements.txt")
    if (file.exists(p)) {
      return(p)
    }
  }
  return(NA)
}
req_path <- find_reqs()
if (!is.na(req_path)) {
  reqs <- readLines(req_path, warn = FALSE)
  r_start <- match("# R Dependencies", reqs)
  if (!is.na(r_start)) {
    r_pkgs <- trimws(reqs[(r_start + 1):length(reqs)])
    r_pkgs <- r_pkgs[r_pkgs != "" & !startsWith(r_pkgs, "#")]
    if (!require("pacman", quietly = TRUE)) install.packages("pacman", repos = "http://cran.us.r-project.org")
    pacman::p_load(char = r_pkgs)
  }
} else {
  stop("Could not find requirements.txt")
}

# Reading data
df_wide <- read.csv("ocorrencias-em-sao-paulo/R_Ocorrencias_em_sao_paulo/data/processed/df_wide_estado.csv", header = TRUE, check.names = FALSE)
df_wide$Date <- as.Date(df_wide$Date)

# Extract a vector of all unique metrics directly from the columns that remain
# Exclude the grouping/time columns
unique_metrics <- setdiff(names(df_wide), c("Date", "Year", "Quarter"))


# 6. Open a PDF graphics device to save all plots in one file
# This will save a file called "All_Metrics_Time_Series.pdf" in your working directory
pdf("ocorrencias-em-sao-paulo/R_Ocorrencias_em_sao_paulo/output/pdfs/All_Metrics_Time_Series.pdf", width = 10, height = 6)

# 7. Start the FOR loop
for (metric_name in unique_metrics) {
  # Check if all values for this metric are NA
  if (all(is.na(df_wide[[metric_name]]))) {
    next
  }

  # Create the ggplot directly using the column from df_wide
  # Sym() is used to inject the column name from the string cleanly
  p <- ggplot(df_wide, aes(x = Date, y = !!sym(metric_name))) +
    geom_line(color = "#1A73E8", size = 1.2, na.rm = TRUE) +
    geom_point(color = "#1A73E8", size = 2, na.rm = TRUE) +
    geom_smooth(method = "loess", color = "darkgray", linetype = "dashed", se = FALSE, na.rm = TRUE) +
    scale_y_continuous(labels = comma) +
    scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
    theme_minimal() +
    labs(
      title = paste(str_wrap(metric_name, width = 70)), # Dynamic title based on loop
      subtitle = "Ocorrências por trimestre de 2016 a 2025",
      x = "Ano",
      y = "Boletins de Ocorrência",
      caption = "Fonte: Estado de São Paulo"
    ) +
    theme(
      plot.title = element_text(face = "bold", size = 12),
      plot.subtitle = element_text(color = "gray40", size = 11),
      axis.title = element_text(face = "bold"),
      panel.grid.minor = element_blank()
    )

  # IMPORTANT: In a loop, you must explicitly print() the ggplot object
  print(p)
}

# 8. Close the PDF device to save the file
dev.off()

print("All plots have been successfully generated and saved to 'All_Metrics_Time_Series.pdf'")
