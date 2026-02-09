import os
import re
import sys
from collections import defaultdict

# Парсер расширений в список
def parse_extensions(extensions_str):
    """Преобразует строку расширений в список"""
    # Убираем запятые, точки в начале не обязательны
    extensions_str = extensions_str.replace(',', ' ')
    extensions = []
    
    for ext in extensions_str.strip().split():
        ext = ext.strip()
        if ext:
            # Добавляем точку, если её нет
            if not ext.startswith('.'):
                ext = '.' + ext
            # Приводим к нижнему регистру
            ext = ext.lower()
            extensions.append(ext)
    
    return list(set(extensions))  # Убираем дубликаты  

def group_files_by_base_name(folder_path, target_exts):
    """
    Группирует файлы по базовому имени (после чистки названий),
    учитывая заданные расширения.
    """
    groups = defaultdict(list)

    for root, _, files in os.walk(folder_path):
        for file in files:
            # Выделяем чистое расширение файла
            _, file_ext = os.path.splitext(file)
            # Приводим расширение к нижнему регистру для упрощения сравнения
            file_ext_lower = file_ext.lower()

            # Проверяем, входит ли расширение файла в список разрешённых
            if file_ext_lower in target_exts:
                name = os.path.splitext(file)[0]

                # Очищаем имя файла от спецсимволов
                clean_name = re.sub(r"\b(Rus|Kudos)\b", "", name, flags=re.IGNORECASE)
                base_name = re.sub(r"\s*(CD|Disc)[\s_]*\d+", "", clean_name, flags=re.IGNORECASE)
                base_name = " ".join(base_name.split())

                # Полный путь к файлу
                full_path = os.path.join(root, file)

                # Группируем
                groups[(root, base_name)].append(full_path)

    return groups

def create_m3u(folder_path, extensions_str):
    """Создает M3U файлы для файлов с указанными расширениями"""
    # Преобразуем строку расширений в нормальный список
    target_exts = parse_extensions(extensions_str)

    # Группируем файлы по основному имени
    groups = group_files_by_base_name(folder_path, target_exts)

    # --- создание m3u ---
    created_count = 0
    for (folder, base_name), file_list in groups.items():

        # Имя плейлиста
        m3u_path = os.path.join(folder, base_name + ".m3u")

        with open(m3u_path, "w", encoding="utf-8") as f:
            for file_path in sorted(file_list):
                # возьмем только название файла, т.к пишем в ту же папку, полный путь не нужен
                filename_only = os.path.basename(file_path)
                f.write(filename_only + "\n")
        created_count += 1        

        print("Создан плейлист:", m3u_path)

    return created_count  
