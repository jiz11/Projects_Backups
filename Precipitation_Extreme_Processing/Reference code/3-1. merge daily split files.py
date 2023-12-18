import os
import pandas as pd

## 将所有按天拆分的城市/县气温插值数据汇总成一个表格，将时间信息作为额外列
## 由于数据量过大，电脑运行内存不足，因此先将日数据汇总到每年，再用R汇总所用年度数据并生成.dta文件（用python生成.dta文件似乎总有问题）

def get_compare(files: str):
    temp_name = files.replace('.csv', '')
    splits = temp_name.split('-')
    return int(splits[0]) * 10000 + int(splits[1]) * 100 + int(splits[2])

# filePath = '../weather/raw data/SURF_CLI_CHN_MUL_DAY_V3.0/processed/city_int'
filePath = '../weather/raw data/SURF_CLI_CHN_MUL_DAY_V3.0/processed/county_int'

f_name = os.listdir(filePath)
f_name.sort(key=lambda x: get_compare(x))

# column_names = ['citycode', 'cityname', 'year', 'month', 'day', 'avg_temp', 'high_temp', 'low_temp']
column_names = ['countycode', 'countyname', 'year', 'month', 'day', 'avg_temp', 'high_temp', 'low_temp']

for prefix in range(1951, 2017):
    # Create a new DataFrame for each year
    data = pd.DataFrame(columns=column_names)

    for file_name in f_name:
        name = file_name.replace('.csv', '')
        file_prefix = int(name.split('-')[0])

        if file_prefix == prefix:
            infix = name.split('-')[1]
            postfix = name.split('-')[2]
            if len(infix) == 1:
                infix = '0' + infix
            if len(postfix) == 1:
                postfix = '0' + postfix

            cur_file_path = filePath + '/' + file_name
            daily = pd.read_csv(cur_file_path)

            df = pd.DataFrame()

#            df['citycode'] = pd.DataFrame(daily, columns=['citycode'])
#            df['cityname'] = pd.DataFrame(daily, columns=['cityname'])
            df['countycode'] = pd.DataFrame(daily, columns=['countycode'])
            df['countyname'] = pd.DataFrame(daily, columns=['countyname'])
            df['year'] = prefix
            df['month'] = infix
            df['day'] = postfix
            df['avg_temp'] = pd.DataFrame(daily, columns=['avg_temp'])
            df['high_temp'] = pd.DataFrame(daily, columns=['low_temp'])
            df['low_temp'] = pd.DataFrame(daily, columns=['high_temp'])

            # Drop rows where 'countyname' is an empty string
            df.drop(df[df['countyname'] == ' '].index, inplace=True)

            data = pd.concat([data, df], ignore_index=True)
            print('finish ' + str(name))

    # Save the DataFrame as a separate CSV file for each year
#    result = f'../weather/raw data/SURF_CLI_CHN_MUL_DAY_V3.0/Result/city/{prefix}.csv'
    result = f'../weather/raw data/SURF_CLI_CHN_MUL_DAY_V3.0/Result/county/{prefix}.csv'
    data.to_csv(result, index=False)
    print(f'Saved {prefix} file')

print('all finish')
