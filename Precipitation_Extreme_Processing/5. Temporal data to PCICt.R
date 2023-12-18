csv.to.pcict.txt <- function(input_csv){
  temporal_data <- read.csv(input_csv)
  county_code <- tools::file_path_sans_ext(basename(input_csv))
  temporal_data$date <- as.Date(as.character(temporal_data$date), 
                                format = "%Y%m%d")
  output_txt <- temporal_data %>% 
    #Add date columns.
    mutate(year = year(date), 
           month = month(date),
           day = day(date)) %>% 
    #Delete redundant columns.
    subset(select = -c(longitude, latitude, optional))
  output_filename <- paste0("./Processed_County_PCICt_Input/", county_code, ".txt")
  #Set "row.names = FALSE" or you will get an extra first column.
  write.table(output_txt, output_filename, sep = ",", row.names = FALSE)
}

county_temporal_batch <- list.files(path = "./Processed_County_TemporalData/", 
                                   pattern = "*.csv", full.names = TRUE)
lapply(county_temporal_batch, csv.to.pcict.txt)

cat("PCICt txt files generation complete.\n")