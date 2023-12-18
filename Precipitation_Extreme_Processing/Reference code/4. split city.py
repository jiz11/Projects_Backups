import pandas as pd

# 为方便后续计算所有城市的当地历史同期温度指标，将汇总的气温文件按城市拆分
df = pd.io.stata.read_stata("../weather/temp_city_1951_2016_daily.dta")

class_list = list(df['citycode'].drop_duplicates())

for i in class_list:
    df1 = df[df['citycode'] == i].drop(columns=['low_temp', 'avg_temp']).rename(columns={'high_temp': 'temp'})
    df2 = df1[(df1['year'] >= 1961) & (df1['year'] <= 1990)]

    df1.to_csv('../heatwave indicator/split city all years./%s.csv' % (i))
    df2.to_csv('../heatwave indicator/split city 30 years./%s.csv' % (i))