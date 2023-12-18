etccdi.precipitation <- function(input_txt){
  data_txt <- read.table(input_txt,header = TRUE, sep = ",")
  id <- tools::file_path_sans_ext(basename(input_txt))
  data_PCICt <- as.PCICt(do.call(paste, 
                                 data_txt[,c("year", "month", "day")]), 
                         format="%Y%m%d", 
                         cal = "gregorian")
  ci <- climdexInput.raw(prec = data_txt$Pre_2020_esti,
                         prec.dates = data_PCICt,
                         base.range = c(1961,1990))
  
  result_r95ptot <- climdex.r95ptot(ci)
  result_r99ptot <- climdex.r99ptot(ci)
  result_prcptot <- climdex.prcptot(ci)
  result_r10mm <- climdex.r10mm(ci)
  result_r20mm <- climdex.r20mm(ci)
  result_sdii <- climdex.sdii(ci)
  
  result_df <- data.frame(
    Year = names(result_r95ptot),
    R95pTOT = as.numeric(result_r95ptot),
    R99pTOT = as.numeric(result_r99ptot),
    PRCPTOT = as.numeric(result_prcptot),
    R10mm = as.numeric(result_r10mm),
    R20mm = as.numeric(result_r20mm),
    SDII = as.numeric(result_sdii)
  )
  
  result_df$dt_code <- rep(data_txt[1,1], nrow(result_df))
  result_df$dt_name <- rep(data_txt[1,2], nrow(result_df))
  result_df$ct_code <- rep(data_txt[1,3], nrow(result_df))
  result_df$pr_code <- rep(data_txt[1,5], nrow(result_df))
  
  output_filename <- paste0("./Output_ETCCDI_Precipitation/County_Level/", 
                            id, ".csv")
  write.csv(result_df,output_filename, row.names = FALSE)
}

county_PCICinput_batch <- list.files( path = "./Processed_County_PCICt_Input/", 
                                      pattern = "*.txt", full.names = TRUE)
lapply(county_PCICinput_batch, etccdi.precipitation) 
