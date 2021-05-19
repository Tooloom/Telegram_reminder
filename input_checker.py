import re
from datetime import datetime
from datetime import timedelta


def user_input_checker(text):
    if text == 'Назад':
        return 'Назад'
    if text == 'Показать уведомления':
        return 'Показать уведомления'
    result = re.findall(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}\s\w+', text)
    if len(result) != 0:
        year = int(result[0].split('-')[0])
        month = int(result[0].split('-')[1])
        day = int(result[0].split('-')[2][0:2])
        hour = int(re.findall(r'\s\d\d:\d\d\s', text)[0].split(':')[0])
        minute = int(re.findall(r'\s\d\d:\d\d\s', text)[0].split(':')[1])

        try:
            given_date = datetime(year, month, day, hour, minute)
            current_date = datetime.now()
            now_plus_5 = current_date + timedelta(minutes=1)
            if now_plus_5 > given_date:
                return 'Нельзя задавать уведомления в прошлом'
        except ValueError:
            return 'Дата и время введены неверно'
        return 'OK'
    else:
        return 'Некорректные данные'
