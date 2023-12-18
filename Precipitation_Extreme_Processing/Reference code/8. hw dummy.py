import pandas as pd


percentiles = [93, 95, 97, 99]
day_sums = [3, 5, 7]

for percentile in percentiles:
    for day_sum in day_sums:
        leader = pd.read_stata('../governors/governor-calculation.dta')

        heat = pd.read_csv(f'../heatwave indicator/heatwave events/new/{percentile}_{day_sum} hw events.csv')
        heat.columns = ['市代码', '市', 'year', 'event']
        heat2 = heat.drop(labels=['市', 'event'], axis=1)

        ans = []
        dum = []
        count = 0

        # 做嵌套的for循环
        ## 对于每个leader 而言,记录他们的出生地和年龄段（5-15）信息
        for idx2, row2 in leader.iterrows():
            leader_5 = int(row2['year5'])
            leader_15 = int(row2['year15'])
            leader_birth_area = int(row2['birthcode'])

            cur_result = 0
            dummy = 0
            ## 对于每个heawave record而言
            for idx1, row1 in heat2.iterrows():
                heat_time = int(row1['year'])
                heat_location = int(row1['市代码'])
                ## 如果官员的出生地和成长期满足条件，cur_result计数加一 （sum of events）
                if leader_5 <= heat_time <= leader_15 and heat_location == leader_birth_area:
                    cur_result += 1
            # 创建dummy var
            if cur_result != 0:
                dummy = 1

            ans.append(cur_result)
            dum.append(dummy)

            count += 1
            print('finish ' + str(count), 'percent:', percentile, 'duration', day_sum)

        leader[f'dummy_{percentile}_{day_sum}'] = dum
        leader[f'events_{percentile}_{day_sum}'] = ans
        leader.to_csv(f'../governors heatwave exposure/governor hw dummy_{percentile}_{day_sum}.csv')