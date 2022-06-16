import json
# import time
# import sys
import os
import webbrowser

import tkinter as tk
# from tkinter import * - this import gave a warning in VS Code
# from tkinter import ttk
import pandas as pd
import requests
import time

file_name = 'BIN data.xlsx'
def search_gov_data_and_export_to_file(company_business_id, file_name):
    dfs = []
    
    s = requests.Session() # https://requests.readthedocs.io/en/master/user/advanced/
    # DATA.GOV.KZ BLOCKS HEADER 'user-agent: requests'. YOU MAY ALSO TRY http.client LIBRARY
    s.headers.update({ 'User-Agent': 'Mozilla/5.0', })

    # PROGRAM SEARCHES DATA BY CHUNKS. 'data.egov.kz' DIDN'T ALLOW TO SEARCH ENTIRE LIST AT ONCE.
    x = 0
    searched_ids = 4    
    time_start = time.perf_counter() 

    for _ in company_business_id[x:]:
        
        while x < len(company_business_id):
            if searched_ids >= 50:
                # looks like 15 seconds sleep won't give Expected object or value error.
                # if we sleep 0 seconds it still works somehow
                time.sleep(0)  
                searched_ids = 4 

            search_params = {"size":100, "query" : { "terms": { "bin": company_business_id[x:x+4] }}}
            search_params_converted = json.dumps(search_params)
        
            try:
                # DO NOT SEPARATE URL WITH "\" SIGN. IT DIDN'T WORK WITH LOOP
                response = s.get(f'https://data.egov.kz/api/v4/gbd_ul/v1?source={search_params_converted}&apiKey=2**************************2e')
                df = pd.read_json(response.text)
                dfs.append(df)
                response.close()
                result = pd.concat(dfs, sort=False)
                result.to_excel(os.path.join(os.getcwd() , file_name),sheet_name=f'{file_name}', index=False, freeze_panes=(1,0)) 
                x = x + 4
                searched_ids += 4
            except Exception as e:
                result = pd.concat(dfs, sort=False)
                    # BASICALLY WE REWRITING FILE FROM SCRATCH EACH TIME WE HAVE ERROR
                result.to_excel(os.path.join(os.getcwd() , file_name),sheet_name=f'{file_name}', index=False, freeze_panes=(1,0)) 
                print('{0} error on {1}'.format( e,  company_business_id[x:x+4]) )
             
                
             
            # print(search_params_converted, len(dfs), response.elapsed.total_seconds(),response.url)           
    time_finish = time.perf_counter()    
    print('Finished processing {0} searches in {1} seconds'.format(len(company_business_id), time_finish - time_start))
   #    result = pd.concat(dfs, sort=False) 
        # IN THIS PROGRAM GUI DID'T ALLOW PASTING USING 'Ctrl+V' WHEN FILE NAMED IN LANGUAGE OTHER THAN ENGLISH 
   #    result.to_excel(os.path.join(os.getcwd() , file_name),sheet_name=f'{file_name}', index=False, freeze_panes=(1,0)) 
        # result.to_csv((os.path.join(os.getcwd() , 'data_by_BIN.csv')),sep='_', index=False)


def get_data_by_id():
       
    raw_text = text_Box.get("1.0","end-1c")
    
    # CONVERT TEXT TO LIST.
    raw_text = raw_text.split(",")
    
    #FOR EACH ITEM IN LIST REMOVE '\n' AND SPACE.
    raw_text = [item.replace("\n", "") for item in raw_text]
    raw_text = [item.replace(" ", "") for item in raw_text]
    
    #REMOVE EMPTY ITEMS FROM LIST
    text = [] 
    for item in raw_text: 
        if item not in text: 
            text.append(item) 
            
    search_gov_data_and_export_to_file(text, file_name)
    
def open_url(url):
    webbrowser.open_new(url)  


# GRAPHICAL USER INTERFACE 
# IN THIS PROGRAM GUI DID'T ALLOW PASTING USING 'Ctrl+V' WHEN FILE NAMED IN LANGUAGE OTHER THAN ENGLISH 
# BEFORE COPYING CODE FROM JYPITER NOTEBOOK OR BEFORE MAKING '.exe' FILE WITH 'pyinstaller' 
#    EACH tkinter WIDGET AND 'Tk' MUST BE PREPENDED WITH 'tkinter.' OR 'tk.' (if 'import tkinter as tk' )
#    ALL 'pack' METHODS MUST BE WRITTEN IN QUOTES AND LOWERCASE
# EXAMPLE:
#    INCORRECT USE: 'BOTH' ; CORRECT USE: 'both'
#    INCORRECT USE: 'Frame' ; CORRECT USE: 'tk.Frame'

root = tk.Tk(className='Выгрузка данных по БИН')
root.minsize(width=500, height=330)
# root.maxsize(width=100, height=100)

label_frame = tk.Frame(root)
label_frame.pack(expand = False, fill="both")


label = tk.Label(label_frame, wraplength=500 , text=f'\nПрограмма выгружает данные организаций по БИН.\n\
Поиск происходит на портале "Открытые данные" (data.egov.kz).\n\
\nВведите БИНы через запятую, нажмите на поиск, программа выгрузит данные в файл "{file_name}".\
 Файл будет в том же месте, где была запущена программа.',
             font=("Segoe UI", 10))
label.pack()

link = tk.Label(label_frame, font=("Segoe UI", 8), text="Ссылка на данные", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e: open_url("https://data.egov.kz/datasets/view?index=gbd_ul"))


text_and_scroll_frame = tk.Frame(root)
text_and_scroll_frame.pack(expand = True, fill="both")

scrollbar = tk.Scrollbar(text_and_scroll_frame)
scrollbar.pack(side='right', fill='y')

text_Box = tk.Text(text_and_scroll_frame,font=("Segoe UI", 11), wrap='word', height=7, width=40, yscrollcommand=scrollbar.set) 
text_Box.pack(expand = True, fill = "both")
scrollbar.config(command=text_Box.yview)


button_frame = tk.Frame(root)
button_frame.pack(expand = False)#, fill="both")
buttonCommit = tk.Button(button_frame, height=1, width=25,font=("Segoe UI", 10), text="Поиск данных по БИН", 
                    command=lambda: get_data_by_id())
#command=lambda: retrieve_input() >>> just means do this when i press the button
buttonCommit.pack()#fill=BOTH)

root.mainloop()

