import os
import shutil
import sys

def program_instructions():
    directory  = "C:\\Users\\gk\Downloads\Приказы\COVID 19 КВИ Коронавирус"
    directory = directory.replace('/','\\')
    print('''
    Программа предназначена для копирования папки без файлов '*.eml' и '*.ini'.
    Полученная копия папки с файлами может использоваться для передачи франчайзи.
     
    Написана на языке программирования Python (пайтон/питон). Версия Python 3.7.8.

    Для запуска программы необходимо указать полный путь к исходной папке. 
    Например: "{}"
    
    Чтобы найти полный путь, зайдите в исходную папку. Найдите строку в верхней части окна
    примерно следующего содержания: "Этот компьютер > Загрузки > Приказы > COVID 19 КВИ Коронавирус"
    Нажмите на строку левой кнопкой мыши, она выделиться синим и покажет полный путь к папке, который нужно скопировать и вставить в программу.

    Вставлять в программу полный путь к папке нужно без пробелов и других знаков. После вставки нажмите Enter.
    Для вставки можно использовать сочетание клавиш "Ctrl+v".

    Если сочетание клавиш "Ctrl+v" не работает, нажмите правую кнопкку мыши в поле вставки после того, как скопировали путь.
    
    Если скопированный путь по прежнему не вставляется: 
    на верхней части окна программы кликните посередине правой кнопкой мыши, появится меню, в меню наведите на "Изменить", затем нажмите на "Вставить".
    "Верхня часть окна программы" - это та, у которой в правой части расположены кнопки "Свернуть", "Развернуть", "Закрыть" (крестик).     

    '''.format(directory))


def print_delete_dash():
    dir_err  = "C:/Users/gk/Desktop/Выезда - КДЛ/Октябрь/02.10.20"
    dir_err = dir_err.replace('/','\\')
    dir_err2  = "C:/Users/gk/Desktop/Выезда КДЛ/Октябрь/02-10-20"
    dir_err2 = dir_err2.replace('/','\\')
    dir_no_err = "C:/Users/gk/Desktop/Выезда КДЛ/Октябрь/02.10.20"
    dir_no_err = dir_no_err.replace('/','\\')
    print('''
    Необходимо удалить знак тире "—" с названий папок.
    Например: 
    "{0}" - неверно, потому что есть тире в названии одной из папок.
    "{1}" - неверно, потому что есть тире в названии одной из папок.
    "{2}" - верно, потому что нет тире в названиях папок.
    '''.format(dir_err,  dir_err2, dir_no_err))

def get_path():
    path = input('    Введите путь к папке и нажмите Enter: ')
    # while '-' in path or "—" in path:
    #     print_delete_dash()
    #     path = input('    Введите путь к папке и нажмите Enter: ')
    return path


def list_files(directory):
    
    for subdir, dirs, files in os.walk(directory):
            for filename in files:
                print(filename)
    print('\nВыше перечислены файлы в папке "{directory}" и ее подпапках.\n'.format(directory=directory))
 

def list_empty_directories(destinaiton):
    empty_dirs = []
    for (dirpath, dirnames, filenames) in os.walk(destinaiton):
        if len(dirnames) == 0 and len(filenames) == 0 :   
            empty_dirs.append(dirpath)      
            #os.rmdir(dirpath)

    for empty_dir in empty_dirs:
        print('Пустая папка:', empty_dir)
    print('\n')

if __name__ == '__main__':
     
    program_instructions()
    source = get_path()
    splitted = os.path.split(source)
    destinaiton = splitted[0] + os.sep + splitted[1] + ' копия для франчайзи'
    shutil.copytree(source, destinaiton, ignore=shutil.ignore_patterns('*.eml', '*.ini'))
    list_files(destinaiton)
    try:
        list_empty_directories(destinaiton)
    except PermissionError as e:
        print(e)     
    input('Нажмите Enter пару раз для выхода')
    sys.exit()