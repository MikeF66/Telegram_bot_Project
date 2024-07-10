import requests
from config import TOKEN, CALENDAR_API_KEY
from translate import translate, translate_to_en

def get_holidays(country, year):
    url = f'https://calendarific.com/api/v2/holidays?&api_key={CALENDAR_API_KEY}&country={country}&year={year}'
    print(url)
    response = requests.get(url)
    return response.json()
def get_list(country, year):
    holidays = get_holidays(country, year)
    holiday_list = []
    error = None
    if 'response' in holidays and 'holidays' in holidays['response']:
        for holiday in holidays['response']['holidays']:
            name = holiday['name']
            date = holiday['date']['iso']
            description = holiday['description']
            holiday = [name, date,description]
            holiday_list.append(holiday)
    else:
        error = "Нет доступных данных о праздниках."
        return holiday_list, error




