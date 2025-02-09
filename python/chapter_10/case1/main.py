import os
import re
import glob
import csv


def process_files(source_dir, destination_dir):
    
    # если папки назначения - нет
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
                # Записываем данные файла, пропуская первую строку 
                # если в каждом файле есть заголовок
                outfile.writelines(lines[1:])
    
    print(f"Объединенный файл: {combined_file_path}")


if __name__=='__main__':
    path = os.path.join(os.getcwd(), 'python\\chapter_10\\case1')
    process_files(path, path)
