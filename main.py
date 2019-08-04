import pandas as pd
import os
import completeness as cp
import create as crt

files = os.listdir('./')
dataset_directory = '/Users/ira/Desktop/grib_proj/dataset'
if 'gribData.csv' not in files:
    crt.create_csv(dataset_directory)

df = pd.read_csv('gribData.csv')

error_date_files = []
error_earliness_files = []
error_one_hour_step = []
error_name_files = []
error_six_hour_step = []
error_completeness = []

number_of_rows = len(df.index)

# проверка даты начала
for index, row in df.iterrows():
    # проверка выхода за границу дат
    if row['dataDate'] < 20130224 or row['dataDate'] > 20130301:
        error_date_files.append(row['filename'])
    # проверка нижней границы
    if row['dataDate'] == 20130224 and row['dataTime'] < 1800:
        error_date_files.append(row['filename'])
    # проверка верхней границы
    if row['dataDate'] == 20130301 and row['dataTime'] > 600:
        error_date_files.append(row['filename'])
    # проверка границ заблаговременности
    if row['P1'] < 0 or row['P1'] > 60:
        error_earliness_files.append(row['filename'])

    # проверка совпадения данных и имени файла
    if row['dataTime'] == 0:
        dataTime = '0000'
    elif row['dataTime'] == 600:
        dataTime = '0600'
    else:
        dataTime = str(row['dataTime'])
    if row['P1'] // 10 == 0:
        P1 = '00' + str(row['P1'])
    else:
        P1 = '0' + str(row['P1'])
    # pattern = str(row['dataDate']) + dataTime + '+' + P1 + 'H00M'
    pattern = f"{row['dataDate']}{dataTime}+{P1}H00M"
    if pattern not in row['filename']:
        error_name_files.append(row['filename'])

    # проверка полноты данных [1x1x606x606]
    if row['numberOfCodedValues'] != 367236:
        error_completeness.append(row['filename'])

    print(f'{index} row passed')

# Проверка заблоговременности
for index in range(number_of_rows - 1):
    if (
            df.loc[i, 'P1'] + 1 != df.loc[index+1, 'P1'] and
            df.loc[i, 'dataDate'] == df.loc[index+1, 'dataDate'] and
            df.loc[i, 'dataTime'] == df.loc[index+1, 'dataTime']
    ):
        # error_one_hour_step.append(str(df.loc[i, 'filename']) + ' ' + str(df.loc[i + 1, 'filename']))
        error_one_hour_step.append(f"{df.loc[i, 'filename']} {df.loc[i + 1, 'filename']}")

# проверка шага в 6 часов
for index in range(1, number_of_rows - 1):
    if (
            df.loc[index, 'dataTime'] != df.loc[index-1, 'dataTime'] and
            df.loc[index, 'dataTime'] != df.loc[index+1, 'dataTime'] and
            df.loc[index, 'dataDate'] == df.loc[index-1, 'dataDate'] and
            df.loc[index, 'dataDate'] == df.loc[index+1, 'dataDate']
    ):
        error_six_hour_step.append(df.loc[index, 'filename'])

# дполнение проверки полноты данных
zero_files = cp.completeness(dataset_directory)  # возращает файлы, в которых не 3 записи
error_completeness.extend(zero_files)

# запись результатов в файл
with open('result.txt', 'w') as file:
    file.write('Файлы с датой, вышедшей за границы\n')
    file.writelines('\n'.join(error_date_files) + '\n')
    file.write('Файлы с ошибкой в имени\n')
    file.writelines('\n'.join(error_name_files) + '\n')
    file.write('Ошбика типа 6-hour-step\n')
    file.writelines('\n'.join(error_six_hour_step) + '\n')
    file.write('Ошибка типа 1-hour-step\n')
    file.writelines('\n'.join(error_one_hour_step) + '\n')
    file.write('Ошибка полноты данных\n')
    file.writelines('\n'.join(error_completeness) + '\n')
    file.write('Ошибка границ заблаговременности')
    file.writelines('\n'.join(error_earliness_files) + '\n')

# отладочный блок
# print('completeness')
# print(error_completeness)
# print()
# print('Error date')
# print(error_date_files)
# print()
# print('Error name')
# print(error_name_files)
# print()
# print('Error 6-hour-step')
# print(error_six_hour_step)
# print()
# print('Error 1-hour-step')
# for item in error_one_hour_step:
# 	print(item)
