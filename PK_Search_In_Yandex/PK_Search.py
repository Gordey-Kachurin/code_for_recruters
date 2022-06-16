import csv
import os
import sys
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import simpledialog



regions = ['Алматы','Нур-Султан','Шымкент','Актобе','Караганда','Тараз',
'Павлодар','Усть-Каменогорск','Семей','Атырау','Костанай','Кызылорда',
'Уральск','Петропавловск','Актау','Темиртау','Туркестан','Кокшетау',
'Талдыкорган','Экибастуз','Рудный',
'Казахстан',    
'Акмолинская область', 'Актюбинская область', 'Алматинская область',
'Атырауская область', 'Западно-Казахстанская область',
'Жамбылская область', 'Карагандинская область',
'Костанайская область', 'Кызылординская область',
'Мангистауская область', 'Южно-Казахстанская область',
'Павлодарская область', 'Северо-Казахстанская область',
'Восточно-Казахстанская область', 'Туркестанская область']

category = 'Медицинская лаборатория'

# INPUT BOX
window = tk.Tk()
window.withdraw()
company_name = simpledialog.askstring(title='Поиск организации', 
prompt=f'Поиск в Яндекс по категории "{category}". Осуществляется в пределах РК.\n\
Запускать можно не более {int(500/len(regions))} раз(а) в сутки.\n\
\n\
Во время работы создается папка с названием искомой организации.\n\
В папке создаются файлы по каждому региону и один общий.\n\
При открытии файлов в Excel нужно указать разделитель (подчеркивание): "_".\n\
\n\
Введите название организации как в Яндекс картах.\n\
Пример: Инвитро, Invivo (вводить только одно значение)')

if company_name == '' or company_name == None:
    sys.exit()


fieldnames = ['Организация','Широта (latitude)','Долгота (longitude)', 'Адрес','Вебсайт','doogal.co.uk']
files = []

# CREATE DIRECTORY AND WORK IN CREATED DIRECTORY
try:
    currentDirectory = os.getcwd()
    os.mkdir(company_name)
    os.chdir(os.path.join(currentDirectory , company_name))
      
except FileExistsError:
    os.chdir(os.path.join(currentDirectory , company_name))


for region in regions:
 
 
# CONNECT TO YANDEX AND SEARCH FOR DATA. THEN CREATE INDENTED FILE FOR HUMAN READING
    search = company_name + ' ' + category + ' ' + region
    payload = {'text': search,'type':'biz','results': 5000 ,'lang':'ru_RU',  'apikey' : '4675***************************1999' }
    connection = requests.get('https://search-maps.yandex.ru/v1/', params=payload)
    soup = BeautifulSoup(connection.text, 'html.parser')
    parsed = json.loads(soup.text)

    with open (company_name + ' ' + region +'.txt', 'w', encoding="utf-8") as f:
        f.write(json.dumps(parsed, indent=2)) #sort_keys=True
    connection.close

# CREATE FILE AND PUT VALUES FOR 'fieldnames' FROM JSON 
    with open (company_name + ' ' + region +'.txt', 'r', encoding="utf-8") as f:    
        json_load = json.load(f)
        count = 2
        with open (company_name + ' ' + region +'.csv', 'w', encoding="utf-8", newline='') as selection_from_json:
            files.append(company_name + ' ' + region +'.csv')            
            csv_writer = csv.DictWriter(selection_from_json, fieldnames=fieldnames, delimiter='_')
            csv_writer.writeheader()
            # csv_writer = csv.writer(new, delimiter='_')
            # csv_writer.writerow(fieldnames)

    # SEARCH VALUES IN JSON FOR 'fieldnames' 
            try:
                for i in json_load['features']:
                    longitude, latitude = i['geometry']['coordinates']
                    company = i['properties']['CompanyMetaData']['name']
                    address = i['properties']['CompanyMetaData']['address']
                    url = i['properties']['CompanyMetaData']['url']
                    row = f'{company}_{latitude}_{longitude}_{address}_{url}_=СЦЕПИТЬ(B{count};", ";C{count})'
                    selection_from_json.write(row + '\n')
                    count += 1
                    
            except KeyError:
                pass
    os.remove(company_name + ' ' + region +'.txt')        
          

# MERGE FILES
with open('Все (с дубликатами).csv', 'w', encoding="utf-8") as outfile:
    for each_file in files:
        with open(each_file, 'r', encoding="utf-8") as f:
            for line in f:
                outfile.write(line)


# REMOVE DUPLICATES IN MERGED FILE USING PANDAS
df = pd.read_csv('Все (с дубликатами).csv',sep='_',dtype={'Широта (latitude)':str, 'Долгота (longitude)':str}) #, header=None , header=None, skiprows=1
df.sort_values('Адрес', inplace=True)
no_duplicates = df.drop_duplicates(subset=['Адрес'], keep='first')
no_duplicates.drop(no_duplicates.index[0]).to_csv('Все (без дубликатов).csv', sep='_', index=False)

# df.drop_duplicates(subset=['Адрес'], keep='first').to_csv('Все (без дубликатов).csv', sep='_', index=False)
# df = pd.read_csv(r'Все (без дубликатов).csv',sep='_',dtype={'Широта (latitude)':str, 'Долгота (longitude)':str}) 
# df.drop(0).to_csv('Все (no дубликатов).csv', sep='_', index=False) #df.index[0]


# CORRECT EXCEL FUNCTION IN MERGED FILE AND WRITE RESULT TO A NEW FILE
with open('Все (без дубликатов).csv', 'r', encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter='_') 
    row_number = 2
    with open(company_name + " Одним файлом.csv", 'w', encoding="utf-8",newline='') as new:
        writer = csv.DictWriter(new, fieldnames=fieldnames, delimiter='_')
        writer.writeheader()
        for each_row in reader:
            each_row['doogal.co.uk'] = f'=СЦЕПИТЬ(B{row_number};", ";C{row_number})'
            row_number += 1
            writer.writerow(each_row)
os.remove('Все (без дубликатов).csv')
os.remove("Все (с дубликатами).csv")



