def center_window(window):
    """
    Центрирование окна на экране.
    :param window: объект окна (например, экземпляр Ctk или Tk).
    """
    window.update_idletasks()  # Обновляем состояние окна, чтобы получить точные размеры
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    win_width = window.winfo_width()
    win_height = window.winfo_height()
    
    # Вычисляем положение окна по центру экрана
    x_pos = (screen_width // 2) - win_width
    y_pos = (screen_height // 2) - win_height
    
    # Устанавливаем новое расположение окна
    window.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")