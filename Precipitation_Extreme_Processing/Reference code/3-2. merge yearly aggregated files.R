library(purrr)
library(dplyr)
library(haven)

# city
file_list <- list.files(path = "../weather/raw data/SURF_CLI_CHN_MUL_DAY_V3.0/Result/city", pattern = "*.csv", full.names = TRUE)
merged_data <- map_dfr(file_list, read.csv)
write_dta(merged_data, "../weather/temp_city_1951_2016_daily.dta")

# county
file_list <- list.files(path = "../weather/raw data/SURF_CLI_CHN_MUL_DAY_V3.0/Result/county", pattern = "*.csv", full.names = TRUE)
i = 0
merged_data <- data.frame()  # Create an empty data frame
for (file in file_list) {
  temp_data <- read.csv(file)
  merged_data <- rbind(merged_data, temp_data)
  i = i + 1
  print(i)
}

write_dta(merged_data, "../weather/temp_county_1951_2016_daily.dta")
