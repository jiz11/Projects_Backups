## Counties points interpolation (IDW)

#Read daily precipitation files.
station_daily_batch <- list.files( path = "./Processed_Station_DailyData/", 
                                   pattern = "*.csv", full.names = TRUE)

#Generate idw function
IDW.county.Daily <- function(input_Station_Daily, centroids){
  precip_data <- read.csv(input_Station_Daily)
  
  pre_2020_data <- subset(precip_data, PRE_Time_2020 < 32766)
  
  if (!all(is.na(pre_2020_data$PRE_Time_2020))) {
    coordinates(pre_2020_data) <- c("Lon", "Lat")
    precip_2020 <- idw(formula = PRE_Time_2020 ~ 1, 
                       locations = pre_2020_data, 
                       newdata = centroids)
    centroids$Pre_2020_esti <- as.vector(precip_2020$var1.pred)
  } else {
    precip_2020 <- rep(NA, nrow(centroids))
    centroids$Pre_2020_esti <- precip_2020
  }
  
  #Extract station file name as the date information for city centroids.
  date <- tools::file_path_sans_ext(basename(input_Station_Daily))
  centroids$date <- rep(date, nrow(centroids))
  
  #Output city precipitation indices files.
  output_filename <- paste0("./Processed_County_DailyData/county_", date, ".csv")
  write.csv(centroids, file = output_filename, row.names = FALSE)
}

#Read city centroids data as vector.
county_centroids <- read_csv("RawData/district_centroid_table.csv")
coordinates(county_centroids) <- c("longitude", "latitude")

#Run the function for city cetroids.
lapply(station_daily_batch, IDW.county.Daily, centroids = county_centroids)
cat("County IDW processes complete.\n")
