library(dplyr)
library(haven)
library(readxl)

# not reflected in the whole ideal working process
# but it is useful in merging governor data from different sources together
# since some records may be irregularly duplicated

data <- read_excel("D:/iMEP study/output/governor-panel.xlsx")

# Group by adcode and birthplace, and summarize data
result_df <- data %>%
  arrange(cityname, position, year) %>%
  group_by(adcode, cityname, name, position, birthyear, birthcode, birthplace, gender, degree) %>%
  mutate(
    year_diff = c(0, diff(year)),
    tenure_number = cumsum(year_diff > 1)
  ) %>%
  group_by(adcode, cityname, name, position, birthyear, birthcode, birthplace, gender, degree, tenure_number) %>%
  summarise(
    tenure_begin = min(year),
    tenure_end = max(year)
  )

result_df <- result_df %>%
  select(-tenure_number)

write_dta(result_df, "D:/iMEP study/output/governor-compressed.dta")



## compare whether the compressed and expanded dataset is identical to the original panel dataset
data1 <- read_excel("E:/backup/Data/Intermediate/governors/blank infor fill/merge/final blank filled panel.xlsx")
data1 <- data1[order(data1$adcode, data1$year, data1$position), ]
test <- read_excel("E:/backup/Data/Intermediate/governors/blank infor fill/merge/test.xlsx")
test <- test[order(test$adcode, test$year, test$position), ]

not_identical_rows <- anti_join(data1, test)

