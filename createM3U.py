import os
import re
import sys
from collections import defaultdict

# Получение аргументов
def get_args():
    if len(sys.argv) > 1:
        folder_path = sys.argv[1].strip('"')
    
    if len(sys.argv) > 2:
        extensions_str = sys.argv[2]
    
    return folder_path, extensions_str

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

def create_m3u(folder_path, target_exts):
    """Создает M3U файлы для файлов с указанными расширениями"""
    groups = defaultdict(list)

    # --- поиск файлов ---
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Проверяем все расширения
            for ext in target_exts:
                if file.lower().endswith(ext):

                    name = os.path.splitext(file)[0]

                    # 1) Убираем слово Rus и Kudos
                    clean_name = re.sub(r"\b(Rus|Kudos)\b", "", name, flags=re.IGNORECASE)

                    # 2) Убираем CD1 / CD2 / Disc1 / Disc_2 / Disc 3
                    base_name = re.sub(r"\s*(CD|Disc)[\s_]*\d+", "", clean_name, flags=re.IGNORECASE)

                    # 3) Убираем лишние пробелы
                    base_name = " ".join(base_name.split())

                    # Полный путь к файлу
                    full_path = os.path.join(root, file)

                    # Группируем
                    groups[(root, base_name)].append(full_path)
                    # Выходим из цикла по расширениям, так как файл уже найден
                    break

    # --- создание m3u ---
    created_count = 0
    for (folder, base_name), file_list in groups.items():

        # Имя плейлиста
        m3u_path = os.path.join(folder, base_name + ".m3u")

        with open(m3u_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for file_path in sorted(file_list):
                f.write(file_path + "\n")

        print("Создан плейлист:", m3u_path)

def main():
    print("Создание M3U")

    # Получаем аргументы командной строки
    folder_path, extensions_str = get_args()

    # Парсим расширения файлов в список
    target_exts = parse_extensions(extensions_str)
    
    # Создаем файлы m3U
    create_m3u(folder_path, target_exts)


# Запускаемся
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nОперация прервана пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nНЕОЖИДАННАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)