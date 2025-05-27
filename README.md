# Скрипт для парсинга csv файлов

Шаги по запуску скрипта
1. Перейдите в терминале в любую удобную директорию и пропишите:
```angular17html
git clone https://github.com/JaxckR/testTask_1.git
```
2. Создайте и активируйте виртуальную среду <br>
Windows
```angular17html
python -m venv venv
```
```angular17html
venv\Scripts\activate
```
Linux
```angular17html
python3 -m venv venv
```
```angular17html
source venv/bin/activate
```
3. Перейдите в директорию с главным файлом
```angular17html
cd src/app
```
4. Запустите приложение
```angular17html
python main.py *csv files* --report payout
```
<br>
Важное примечание <br>
Все csv файлы должны находиться строго в директории data. При запуске приложения необходимо лишь указать имя файла

Пример запуска скрипта для data1.csv
```angular17html
python main.py data1.csv --report payout
```