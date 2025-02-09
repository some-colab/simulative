import os
import re
import glob
import csv
import pandas as pd

def is_sublist(lst, sub):
    sub_len = len(sub)
    for i in range(len(lst) - sub_len + 1):
        if lst[i:i+sub_len] == sub:
            return i
    return -1


def process_files(source_dir, destination_dir):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    source_dir = os.path.join(dir_path, source_dir)
    destination_dir = os.path.join(dir_path, destination_dir)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # фильтр
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d+\.csv$')
    
    all_files = glob.glob(os.path.join(source_dir, '*'))
    csv_files = [file for file in all_files if pattern.match(os.path.basename(file))]
    
    if not csv_files:
        print("Не найдено файлов, по заданному шаблону.")
        return
    
    # Сортируем (не понятно: надо - не надо)
    csv_files.sort()
    
    # Путь к результирующему файлу
    combined_file_path = os.path.join(destination_dir, 'combined_data.csv')
    
    header_written = False
    header_init = []
    output_list = []

    for file in csv_files:
        with open(file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            header = next(reader)
            sublist_index = 0

            if not header_written:
                output_list.append(header)
                header_written = True
                header_init = list(header)
            else:
                sublist_index = is_sublist(header, header_init)
            
            for row in reader:
                output_list.append(row[sublist_index:])
                    
    with open(combined_file_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',', quotechar='"')
        for row in output_list:
            writer.writerow(row)


if __name__=='__main__':
    process_files('report-main', 'comb_reports')
    
    user_answer = pd.read_csv('D:\\projects\\simulative\\python\\chapter_10\\case1\\comb_reports\\combined_data.csv')
    correct_answer = pd.read_csv('D:\\projects\\simulative\\python\\chapter_10\\case1\\comb_reports\\data.csv')

    try:
        assert (user_answer == correct_answer).all().all(), 'Ответы не совпадают'
        assert user_answer.columns.equals(correct_answer.columns), 'Названия столбцов не совпадают'
    except Exception as err:
        raise AssertionError(f'При проверке возникла ошибка {repr(err)}')
    else:
        print('Поздравляем, Вы справились и успешно прошли все проверки!')
