create.city.temporal <- function(input_cities_daily, output_path){
  
  city_name_list <- input_cities_daily %>% group_by(city_name) %>%group_split()
  
  for (city_data in city_name_list) {
    city_name <- unique(city_data$city_name)
    write.csv(city_data, file.path(output_path, paste0(city_name,".csv")),
              row.names = FALSE)
  }
}

city_temporal_drive <- "./Processed_City_TemporalData/"

#Read cities daily precipitation data.
city_daily_batch <- list.files(path = "./Processed_City_DailyData",
                               pattern = "*.csv", full.names = TRUE)
#Combine city daily files into one dataframe.
city_combined <- lapply(city_daily_batch, read.csv) %>% 
  bind_rows() %>% filter(Pre_2020_esti >= 1)

create.city.temporal(city_daily_batch, city_temporal_drive)