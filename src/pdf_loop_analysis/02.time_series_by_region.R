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

# 1. Read the raw dataset
df_wide <- read.csv("ocorrencias-em-sao-paulo/R_Ocorrencias_em_sao_paulo/data/processed/df_wide_regiao.csv", header = TRUE, check.names = FALSE)
df_wide$Date <- as.Date(df_wide$Date)

# Rename Deinters to specific valid Region names
df_wide <- df_wide %>%
  mutate(Region = case_when(
    Region == "Deinter 1" ~ "São José dos Campos",
    Region == "Deinter 2" ~ "Campinas",
    Region == "Deinter 3" ~ "Ribeirão Preto",
    Region == "Deinter 4" ~ "Bauru",
    Region == "Deinter 5" ~ "São José do Rio Preto",
    Region == "Deinter 6" ~ "Santos",
    Region == "Deinter 7" ~ "Sorocaba",
    Region == "Deinter 8" ~ "Presidente Prudente",
    Region == "Deinter 9" ~ "Piracicaba",
    Region == "Deinter 10" ~ "Araçatuba",
    TRUE ~ Region
  ))

# Remove Capital, Interior, and Gde SP(1) from the analysis
df_wide <- df_wide[!df_wide$Region %in% c("Capital", "Interior", "Gde SP(1)"), ]

# (Data is already aggregated by Date and Region, and pivoted wider on metric)

# Extract a vector of all unique metrics directly from the columns that remain
# Exclude the grouping columns
unique_metrics <- setdiff(names(df_wide), c("Date", "Region"))

# Save the unique metrics to a CSV file
write.csv(data.frame(Metric = unique_metrics), "ocorrencias-em-sao-paulo/R_Ocorrencias_em_sao_paulo/data/processed/unique_metrics.csv", row.names = FALSE)

# 6. Open a PDF graphics device to save all plots in one file
pdf("ocorrencias-em-sao-paulo/R_Ocorrencias_em_sao_paulo/output/pdfs/All_Metrics_Regions_Time_Series.pdf", width = 12, height = 7)

# 7. Start the FOR loop
for (metric_name in unique_metrics) {
  # Skip to the next metric if all values are NA
  if (all(is.na(df_wide[[metric_name]]))) {
    next
  }

  # Create the ggplot directly using the column from df_wide
  p <- ggplot(df_wide, aes(x = Date, y = !!sym(metric_name), color = Region)) +
    geom_line(alpha = 0.8, linewidth = 1.2, na.rm = TRUE) +
    geom_point(alpha = 0.8, size = 1.8, na.rm = TRUE) +
    scale_y_continuous(labels = comma) +
    scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
    scale_color_viridis_d(option = "turbo") + # "turbo" provides highly distinct, bright colors
    theme_light() + # A cleaner, high-contrast theme
    labs(
      title = paste(str_wrap(metric_name, width = 60)),
      subtitle = "Ocorrências por trimestre de 2016 a 2025",
      x = "Ano",
      y = "Boletins de Ocorrência",
      color = "Região",
      caption = "Fonte: Estado de São Paulo"
    ) +
    theme(
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(color = "gray40", size = 12),
      axis.title = element_text(face = "bold"),
      legend.position = "right",
      legend.title = element_text(face = "bold", size = 12),
      legend.text = element_text(size = 10),
      panel.grid.minor = element_blank()
    )

  # Print the plot to the PDF
  print(p)
}

# 8. Close the PDF device
dev.off()

print("All regional breakdown plots have been generated and saved to 'All_Metrics_Regions_Time_Series.pdf'")
