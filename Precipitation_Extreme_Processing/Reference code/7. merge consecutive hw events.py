import os
import pandas as pd
from datetime import datetime

# merge consecutive HW events
# 即假如在持续3天的热浪标准下，若有连续四天的情况，则该热浪事件将在6.HW events.py中被连续记录两次。此脚本将解决这一问题
input_directory = '../heatwave indicator/heatwave events/'
output_directory = '../heatwave indicator/heatwave events/new'

# Get a list of all CSV files in the input directory
input_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]

for input_file in input_files:
    file_parts = os.path.splitext(input_file)[0].split('_')
    percentile = int(file_parts[0])
    day_sum = int(file_parts[1])

    print(percentile, day_sum)

    hw_days = pd.read_csv(os.path.join(input_directory, input_file))

    dat = []

    for idx, row in hw_days.iterrows():
        date_str = f"{row['year']}-{row['month']}-{row['day']}"
        dat.append(date_str)

    hw_days['date'] = dat
    hw_days['DATE_OBJ'] = [datetime.strptime(d, '%Y-%m-%d') for d in hw_days['date']]
    hw_days['DATE_INT'] = list([d.toordinal() for d in hw_days['DATE_OBJ']])

    event = 1
    eve = [event]

    for idx, row in hw_days.iterrows():
        if 1 <= idx:
            day1 = hw_days.loc[idx - 1, 'DATE_INT']
            day2 = hw_days.loc[idx, 'DATE_INT']
            city1 = hw_days.loc[idx - 1, 'citycode']
            city2 = hw_days.loc[idx, 'citycode']
            a = int(day2) - int(day1)
            if day2 - day1 == 1 and city1 == city2:
                event = event
            else:
                event += 1
            eve.append(event)

    hw_days['consecutive'] = eve

#    hw_eve = hw_days.drop(hw_days.columns[[3, 4, 5, 6, 7, 8, 9]], axis=1)
    hw_eve = hw_days.drop(hw_days.columns[[7, 8, 9]], axis=1)

    output_file = os.path.join(output_directory, f'{percentile}_{day_sum} hw events.csv')
    hw_eve.to_csv(output_file, index=False)
