import copy
import pandas as pd

filePath = '../governors heatwave exposure/governor hw dummy merged_compressed.csv'
result = []

df = pd.read_stata(filePath)
for index, row in df.iterrows():
    year_from = int(row['tenure_begin'])
    year_to = int(row['tenure_end'])
    print(index)
    for i in range(year_from, year_to + 1):
        temp = copy.deepcopy(row)
        temp['year'] = i
        temp['tenure'] = i - year_from + 1
        result.append(temp)

a = pd.DataFrame(result)
b = a.drop(columns=['tenure_begin', 'tenure_end'])
c = b.drop_duplicates()
c.to_csv(f'../governors heatwave exposure/governor hw dummy merged_panel.csv')


'''
f_name = os.listdir(filePath)

for file_name in f_name:
    cur_file_path = filePath + '/' + file_name

    # Extract the base name without extension
    base_name = os.path.splitext(file_name)[0]
    # Split the base name using underscores
    split_parts = base_name.split('_')
    # Extract the numbers from the split parts
    perc = int(split_parts[-2])  # Second-to-last element
    day = int(split_parts[-1])  # Last element
'''