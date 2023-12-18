library(dplyr)
library(readr)
library(fs)  # For working with file system
library(purrr)

# Set the path to the folder containing the datasets
folder_path <- "../governors heatwave exposure"

# List all files in the folder
files <- dir_ls(path = folder_path, regexp = "\\.csv$")

# Initialize a list to store the data frames
data_frames <- list()

# Read each dataset into separate data frames
for (file in files) {
  df <- read_csv(file)
  df <- subset(df, select = -c(...1, cityname, birthplace, year5, year15))
  data_frames[[length(data_frames) + 1]] <- df
}

# Specify the key columns for merging
key_columns <- c("adcode", "name", "tenure_begin", "tenure_end", "birthyear", "birthcode", "position", "gender", "degree")

# Merge data frames using dplyr::full_join (you can choose a different join type if needed)
merged_df <- data_frames %>%
  reduce(full_join, by = key_columns)

write_csv(merged_df, "../governors heatwave exposure/governor hw dummy merged_compressed.csv")
