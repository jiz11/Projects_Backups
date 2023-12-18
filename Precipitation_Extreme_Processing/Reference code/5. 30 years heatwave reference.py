import os
import pandas as pd
import numpy as np

# 计算某市6-8月每天的参考温度指标
# percentile的数据源是1961-1970年间，每年当天以及前后总计15天的气温数据（15-day moving window）
# 例如，为计算某地6月1日的高温参考值，需考虑1961-1970年每年当地5.25-6.8日的气温
#  即percentile的数据集正常而言包括30 years * 15 days = 450 records
def generate_percentile_files(percentile):
    filePath = '../heatwave indicator/split city 30 years'
    f_name = os.listdir(filePath)

    result = pd.DataFrame(columns=['citycode', 'cityname', 'month', 'day', f'{percentile}_indicator'])

    count = 0

    for file_name in f_name:
        cur_file_path = os.path.join(filePath, file_name)
        city = pd.read_csv(cur_file_path)
#        city = pd.read_csv("D:/weather/HW references/542500.csv")

        for idx, row in city.iterrows():
            window = []
            if 31 <= idx <= 122: # range()左闭右开；考虑闰年，所以手动寻找行号（excel辅助计算）
                window = list(range(idx - 7, idx + 8)) + list(range(idx + 146, idx + 161)) + list(
                    range(idx + 299, idx + 314)) + list(range(idx + 452, idx + 467)) + list(
                    range(idx + 605, idx + 620)) + list(range(idx + 758, idx + 773)) + list(
                    range(idx + 911, idx + 926)) + list(range(idx + 1064, idx + 1079)) + list(
                    range(idx + 1217, idx + 1232)) + list(range(idx + 1370, idx + 1385)) + list(
                    range(idx + 1523, idx + 1538)) + list(range(idx + 1676, idx + 1691)) + list(
                    range(idx + 1829, idx + 1844)) + list(range(idx + 1982, idx + 1997)) + list(
                    range(idx + 2135, idx + 2150)) + list(range(idx + 2288, idx + 2303)) + list(
                    range(idx + 2441, idx + 2456)) + list(range(idx + 2594, idx + 2609)) + list(
                    range(idx + 2747, idx + 2762)) + list(range(idx + 2900, idx + 2915)) + list(
                    range(idx + 3053, idx + 3068)) + list(range(idx + 3206, idx + 3221)) + list(
                    range(idx + 3359, idx + 3374)) + list(range(idx + 3512, idx + 3527)) + list(
                    range(idx + 3665, idx + 3680)) + list(range(idx + 3818, idx + 3833)) + list(
                    range(idx + 3971, idx + 3986)) + list(range(idx + 4124, idx + 4139)) + list(
                    range(idx + 4277, idx + 4292)) + list(range(idx + 4430, idx + 4445))
                temp = city.loc[window, 'high_temp']
                indicator = np.nanpercentile(temp, percentile)

                citycode = row['citycode']
                cityname = row['cityname']
                month = row['month']
                day = row['day']

                new_row = pd.DataFrame([[citycode, cityname, month, day, indicator]], columns=result.columns)
                result = pd.concat([result, new_row], ignore_index=True)

        count += 1
        print("city:", count, "percent", percentile)

    result.to_csv(f'../heatwave indicator/HW percentiles/{percentile}_percentile_reference.csv', index=False)

# Loop over different percentiles
percentiles_to_generate = [90, 93, 95, 97, 99]

for percentile in percentiles_to_generate:
    generate_percentile_files(percentile)