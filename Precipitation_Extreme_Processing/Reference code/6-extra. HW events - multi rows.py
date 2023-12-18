import os
import pandas as pd

## 此脚本只用于制作展示性的HW events文件，并未实际用于指标制作中

percentiles = [93, 95, 97, 99]
day_sums = [3, 5, 7]

for percentile in percentiles:
    for day_sum in day_sums:
        indicator = pd.read_csv(
            f'../heatwave indicator/HW percentiles/{percentile}_percentile_reference.csv')
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

            for idx in range(day_sum - 1, len(re3) + 1):  # calculate different durations of HW
                day_sum_values = re3.loc[idx - day_sum + 1:idx, 'warm day']
                if day_sum_values.sum() == day_sum:
                    data_rows = re3.loc[idx - day_sum + 1:idx]
                    data_rows = data_rows.reindex(
                        columns=heatwave.columns)  # Reorganize columns to match heatwave dataframe
                    heatwave = pd.concat([heatwave, data_rows], ignore_index=True)

        heatwave.drop_duplicates(inplace=True)
        output_file = f'../heatwave indicator/heatwave events/{percentile}_{day_sum} heatwave events.csv'
        heatwave.to_csv(output_file, index=False)
## 然后此数据同样经历了7. py的处理，最终得到'../heatwave indicator/HW events'文件夹中的文件
'''
        heatwave['date'] = heatwave.apply(lambda row: f"{row['year']}-{row['month']}-{row['day']}", axis=1)
        heatwave['DATE_OBJ'] = [datetime.strptime(d, '%Y-%m-%d') for d in heatwave['date']]
        heatwave['DATE_INT'] = list([d.toordinal() for d in heatwave['DATE_OBJ']])

        event = 1
        eve = [event]

        for idx1, row in heatwave.iterrows():
            if 1 <= idx1:
                day1 = heatwave.loc[idx1 - 1, 'DATE_INT']
                day2 = heatwave.loc[idx1, 'DATE_INT']
                city1 = heatwave.loc[idx1 - 1, 'citycode']
                city2 = heatwave.loc[idx1, 'citycode']
                if day2 - day1 == 1 and city1 == city2:
                    event = event
                else:
                    event += 1
                eve.append(event)

        heatwave['consecutive'] = eve
        heatwave.drop(heatwave.columns[[7, 8, 9, 10]], axis=1, inplace=True)
'''

