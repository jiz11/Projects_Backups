etccdi.to.annual <- function(input_combined, output_drive){
  etccdi_annual_list <- input_combined %>% group_by(Year) %>% group_split()
  for (etccdi_annual in etccdi_annual_list) {
    year <- unique(etccdi_annual$Year)
    output_fliename <- paste0(output_drive, "CountyLevel_", 
                              year, ".csv")
    write.csv(etccdi_annual,output_fliename, row.names = FALSE)
  }
}

output_county <- "./Output_ETCCDI_MapInput/"

county_etccdi_batch <- list.files(path = "./Output_ETCCDI_Precipitation/County_Level/",
                                  pattern = ".csv", full.names = TRUE)
county_etccdi_combined <- lapply(county_etccdi_batch, read.csv) %>% bind_rows()

etccdi.to.annual(county_etccdi_combined, output_county)