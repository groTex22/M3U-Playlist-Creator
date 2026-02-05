@echo off
chcp 65001 

title Создание M3U плейлистов (расширенная версия)

:menu
cls
echo ============================================
echo   СОЗДАНИЕ M3U
echo ============================================
echo.
echo 1. Создать плейлисты для Dreamcast (.cdi)
echo 2. Создать плейлисты для PlayStation (.bin, .cue)
echo 3. Создать плейлисты для Sega CD (.bin, .iso)
echo 4. Создать плейлисты для всех образов
echo 5. Указать свои расширения
echo 6. Выход
echo.
set /p choice="Выберите действие (1-6): "

if "%choice%"=="1" (
    set "extensions=.cdi"
    goto input_folder
)
if "%choice%"=="2" (
    set "extensions=.bin .cue"
    goto input_folder
)
if "%choice%"=="3" (
    set "extensions=.bin .iso"
    goto input_folder
)
if "%choice%"=="4" (
    set "extensions=.cdi .gdi .bin .cue .iso .img .nrg .mdf"
    goto input_folder
)
if "%choice%"=="5" goto custom_ext
if "%choice%"=="6" exit /b 0

echo Неверный выбор!
pause
goto menu

:custom_ext
cls
echo ============================================
echo   ВВОД СВОИХ РАСШИРЕНИЙ
echo ============================================
echo.
echo Введите расширения через пробел.
echo Пример: .cdi .gdi .bin .cue
echo.
:retry_ext
set "extensions="
set /p extensions="Расширения: "
if "%extensions%"=="" (
    echo Расширения не указаны!
    echo.
    echo 1. Повторить
    echo 2. Выйти
    echo.
    set /p retry="Выберите действие: "
    
    if "%retry%"=="1" goto retry_ext
    if "%retry%"=="2" exit /b 0
    
    echo Неверный выбор. Выход.
    pause
    exit /b 1
)
goto input_folder



:input_folder
cls
echo ============================================
echo   ВЫБОР ПАПКИ
echo ============================================
echo.
echo Введите путь к папке или выберите действие:
echo.
echo 1. Ввести путь вручную
echo 2. Использовать текущую папку
echo 3. Выйти
echo.

rem Сброс переменной перед новым вводом
set "folder_path="

set /p folder_choice="Выберите (1-3): "

if "%folder_choice%"=="1" (
    echo.
    set /p folder_path="Введите путь: "
	rem Проверка на пустой ввод
     if not defined folder_path (
        echo Путь не указан!
        pause
        goto input_folder
    )
)
if "%folder_choice%"=="2" (
    set "folder_path=%cd%"
)
if "%folder_choice%"=="3" (
    exit /b 0
)

rem Проверка, что folder_path установлен
if not defined folder_path (
    echo Ошибка: папка не выбрана!
    pause
    goto input_folder
)
    
rem Проверка существования папки
if not exist "%folder_path%\" (
    echo Папка "%folder_path%" не существует!
	echo.
	echo Повторить?
	echo 1. Да
	echo 2. Нет
    set /p folder_retry="Выберите (1-2): "
	
	if "%folder_retry%"=="1" (
    goto input_folder
	)
	if "%folder_retry%"=="2" (
    exit /b 0
	)
)

echo.
echo ============================================
echo   НАСТРОЙКИ ПРИНЯТЫ
echo ============================================
echo Папка: "%folder_path%"
echo Расширения: %extensions%
echo.
echo Передаем в Python...

pause
python createM3U.py "%folder_path%" "%extensions%"

if errorlevel 1 (
    echo.
    echo ============================================
    echo   ОШИБКА ВЫПОЛНЕНИЯ PYTHON СКРИПТА
    echo ============================================
    echo Python скрипт завершился с ошибкой!
    echo Код ошибки: %errorlevel%
)

rem Если Python выполнился успешно (код возврата 0)
echo.
echo ============================================
echo   ВЫПОЛНЕНИЕ УСПЕШНО ЗАВЕРШЕНО
echo ============================================
echo Python скрипт выполнен успешно!
echo.

pause
