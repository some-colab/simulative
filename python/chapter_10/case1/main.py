import os
import re
import glob
import csv
import pandas as pd

def process_files(source_dir, destination_dir):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    source_dir = os.path.join(dir_path, source_dir)
    destination_dir = os.path.join(dir_path, destination_dir)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # фильтр
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d+\.csv$')
    
    # список всех файлов в исходной папке
    all_files = glob.glob(os.path.join(source_dir, '*'))
    # Фильтруем по шаблону
    csv_files = [file for file in all_files if pattern.match(os.path.basename(file))]
    
    if not csv_files:
        print("Не найдено файлов, по заданному шаблону.")
        return
    
    # Сортируем (не понятно: надо - не надо)
    csv_files.sort()
    
    # Путь к результирующему файлу
    combined_file_path = os.path.join(destination_dir, 'combined_data.csv')
    
    # Флаг, показывающий, что заголовок уже записан
    header_written = False
    # собственно сам заголовок (может быть другой)
    header_init = ''

    with open(combined_file_path, 'w', encoding='utf-8') as outfile:
        for file in csv_files:
            with open(file, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()
                if not lines:
                    # пустой файл
                    continue
                # Если заголовок еще не записан
                if not header_written:
                    outfile.write(lines[0])
                    header_written = True
                    header_init = lines[0]
                    outfile.writelines(lines[1:])
                    continue

                print(header_init == lines[0])
                if lines[0] != header_init:
                    continue

                # Записываем данные файла, пропуская первую строку 
                outfile.writelines(lines[1:])
    
    print(f"Объединенный файл: {combined_file_path}")


if __name__=='__main__':
    # process_files('report-main', 'comb_reports')
    
    user_answer = pd.read_csv('D:\\projects\\simulative\\python\\chapter_10\\case1\\comb_reports\\combined_data.csv')
    correct_answer = pd.read_csv('D:\\projects\\simulative\\python\\chapter_10\\case1\\comb_reports\\data.csv')

    try:
        assert (user_answer == correct_answer).all().all(), 'Ответы не совпадают'
        assert user_answer.columns.equals(correct_answer.columns), 'Названия столбцов не совпадают'
    except Exception as err:
        raise AssertionError(f'При проверке возникла ошибка {repr(err)}')
    else:
        print('Поздравляем, Вы справились и успешно прошли все проверки!')
