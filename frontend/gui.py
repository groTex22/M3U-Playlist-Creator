import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from backend.createM3U import create_m3u
from .window_utils import center_window


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Центрируем окно на экране
        center_window(self)

        self.title("M3U Playlist Creator")
        self.geometry("600x450")

        # Настройки пресетов из вашего батника
        self.options = {
            "Dreamcast (.cdi)": ".cdi",
            "PlayStation (.bin, .cue)": ".bin .cue",
            "Sega CD (.bin, .iso)": ".bin .iso",
            "Все образы": ".cdi .gdi .bin .cue .iso .img .nrg .mdf",
            "Свой вариант": ""
        }

        # --- Заголовок ---
        self.label_title = ctk.CTkLabel(self, text="СОЗДАНИЕ M3U ПЛЕЙЛИСТОВ", font=("Roboto", 20, "bold"))
        self.label_title.pack(pady=(10, 10))

        # --- 1. Выбор папки ---
        # Заголовок
        self.folder_label = ctk.CTkLabel(self, text="Папка с файлами:")
        self.folder_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.pack(fill="x", padx=20)
        
        self.path_entry = ctk.CTkEntry(self.folder_frame, placeholder_text="Путь к папке с играми")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        self.browse_btn = ctk.CTkButton(self.folder_frame, text="Обзор...", width=80, command=self.choose_folder)
        self.browse_btn.pack(side="right", padx=(5, 10), pady=10)

        # --- 2. Выбор расширений ---
        self.ext_label = ctk.CTkLabel(self, text="Выберите платформу или расширения:")
        self.ext_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.ext_combo = ctk.CTkComboBox(
            self, 
            values=list(self.options.keys()),
            command=self.on_selected_extension,
            #width=400
        )
        self.ext_combo.pack(fill="x", padx=20, pady=(0, 10))
        self.ext_combo.set("Все образы")

        # --- Поле ввода расширений (редактируемое) ---
        self.ext_entry = ctk.CTkEntry(self, placeholder_text="Введите расширение например: .cdi .bin")
        self.ext_entry.pack(fill="x", padx=20, pady=5)
        self.ext_entry.insert(0, self.options["Все образы"])

        # === 3. Панель кнопок ===
        # Фрейм
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Кнопка запуска создания плейлиста
        self.run_btn = ctk.CTkButton(
            self.button_frame, 
            text="Создать M3U", 
            command=self.run_script
        )
        self.run_btn.pack(side="left", padx=10)

        # Кнопка выхода из программы
        self.exit_btn = ctk.CTkButton(
            self.button_frame, text="Выход", command=self.destroy, fg_color="#555"
        )
        self.exit_btn.pack(side="left", padx=10)

        # === 4. Логирование действий ===
        self.log = ctk.CTkTextbox(self, height=140)
        self.log.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.log.configure(state="disabled")

    def center_window(self):
        """Метод для размещения окна по центру экрана"""
        self.update_idletasks() # Обновляем параметры окна, чтобы получить точные размеры
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def choose_folder(self):
        """Открывает диалог выбора папки."""
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def on_selected_extension(self, choice):
        """
        Обрабатывает событие выбора расширения.
        Если выбрано "Свой вариант", то переключает на ручной ввод.
        """
        extensions = self.options.get(choice, "")
        if choice != "Свой вариант":
            self.ext_entry.delete(0, "end")
            self.ext_entry.insert(0, extensions)
        else:
            self.ext_entry.delete(0, "end")
            self.ext_entry.focus()

    def write_log(self, text):
        """Запись сообщений в лог."""
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def run_script(self):
        folder = self.path_entry.get().strip()
        exts = self.ext_entry.get().strip()

        if not folder:
            messagebox.showerror("Ошибка", "Выберите папку с файлами!")
            return
        if not exts:
            messagebox.showerror("Ошибка", "Укажите расширения файлов!")
            return
        if not os.path.exists(folder):
            messagebox.showerror("Ошибка", "Указанный путь не существует!")
            return

        try:
            # Запуск createM3U.py
            count = create_m3u(folder, exts)
            self.write_log(f"Количество созданных файлов: {count} \n✅ Создание плейлиста завершилось успешно!")

        except Exception as e:
                    messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def run_gui():
    app = App()
    app.mainloop()