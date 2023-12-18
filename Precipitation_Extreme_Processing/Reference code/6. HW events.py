import os
import pandas as pd

# 统计全部城市全部年份heatwave events数据（在此文件中，热浪的连续性问题尚未考虑）
percentiles = [90, 93, 95, 97, 99]
day_sums = [3, 5, 7]

for percentile in percentiles:
    for day_sum in day_sums:
        indicator = pd.read_csv(f'../heatwave indicator/HW percentiles/{percentile}_percentile_reference.csv')
        heatwave = pd.DataFrame(
            columns=['citycode', 'cityname', 'year', 'month', 'day', 'temp', f'{percentile}_indicator'])

        filePath = '../heatwave indicator/split city all years'

        f_name = os.listdir(filePath)

        for file_name in f_name:
            cur_file_path = filePath + '/' + file_name
            daily = pd.read_csv(cur_file_path)
            print("city", file_name, "day", day_sum, "percent", percentile)
            df = daily[(daily.month >= 6) & (daily.month <= 8)]
            result = pd.merge(df, indicator, how='left', on=['cityname', 'month', 'day'])
            re3 = result.drop(result.columns[[0, 1]], axis=1)
            re3.rename(columns={'citycode_y': 'citycode'}, inplace=True)
            re3['warm day'] = re3.apply(lambda x: 1 if x.temp >= x[f'{percentile}_indicator'] else 0, axis=1)

            for idx in range(day_sum - 1, len(re3) + 1):  #calculate different durations of HW
                day_sum_values = re3.loc[idx - day_sum + 1:idx, 'warm day']
                if day_sum_values.sum() == day_sum:
                    new_row = pd.DataFrame([re3.loc[idx]], columns=heatwave.columns)
                    heatwave = pd.concat([heatwave, new_row], ignore_index=True)

        output_file = f'../heatwave indicator/heatwave events/{percentile}_{day_sum}_heatwave_events.csv'
        heatwave.to_csv(output_file, index=False)
