# импортим либы
import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from datetime import datetime, timedelta

# задаем язык и api ключи
config_dict = get_default_config()
config_dict['language'] = 'ru' 
owm = OWM('api-owm-key', config_dict)
mgr = owm.weather_manager()
bot = telebot.TeleBot('api-telegram-key')

print('Бот работает')

# функция старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для отправки погоды.\nИспользуй команды:\n/weather <город> \n/forecast <город>')
    print(f'Отправлено приветствие {message.from_user.id}')
# функция текущая погода
@bot.message_handler(commands=['weather'])
def weather_now(message):
    try:
        # срезаем только город с ответа
        city = message.text[9:]
        observation = mgr.weather_at_place(city)
        w = observation.weather

        # показатели
        temp = round(w.temperature('celsius')['temp'])
        status = w.detailed_status
        hum = w.humidity
        wind = round(w.wind()['speed'])

        # добавляем к статусу соответствующий смайлик
        if 'ясно' in str(w.detailed_status):
            smile = '☀️'
        elif 'небольшая облачность' in str(w.detailed_status) or 'переменная облачность' in str(w.detailed_status):
            smile = '🌤️'
        elif 'облачно с прояснениями' in str(w.detailed_status):
            smile = '⛅'
        elif 'пасмурно' in str(w.detailed_status) or 'полностью облачно' in str(w.detailed_status):
            smile = '☁️'
        elif 'кратковременный дождь' in str(w.detailed_status):
            smile = '🌧️'
        elif 'дождь' in str(w.detailed_status):
            smile = '☔'
        elif 'гроза' in str(w.detailed_status):
            smile = '⛈️'
        elif 'снег' in str(w.detailed_status):
            smile = '❄️'
        elif 'туман' in str(w.detailed_status):
            smile = '🌫️'
        else:
            smile = ''
        
        # склоняем градусы
        if 1 == int(temp):
            grad = 'градус'
        elif 2 <= int(temp) <= 4 or -2 >= int(temp) >= -4:
            grad = 'градуса'
        else:
            grad = 'градусов'
    
        # формируем ответ и отправляем его
        text = f"В городе {city} сейчас {status}{smile}\n🌡️ Температура: {temp} {grad} по Цельсию.\n💨 Ветер: {wind} м\с\n💧 Текущая влажность составляет {hum} %"
        bot.send_message(message.chat.id, text)
        print(f'Отправлена текущая погода пользователю {message.from_user.id}')
    
    # если что-то пошло не так, отправляем сообщение пользователю об ошибке
    except:
        bot.send_message(message.chat.id, f'Упс, что-то пошло не так. \nСкорее всего \'{city}\' не город.\nПроверьте правильность написания названия города.')
        print(f'Ошибка в текущей погоде у пользователя {message.from_user.id}')
# функция прогноз
@bot.message_handler(commands=['forecast'])
def weather_tomorrow(message):
    try:
        # задаем дату завтрашнего дня
        tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)

        # срезаем только город с ответа
        city = message.text[10:]
        mgr = owm.weather_manager()
        forecaster = mgr.forecast_at_place(city, '3h')

        # перебираем всю погоду за 3 часа(потому что меньше чем на 3 часа нельзя делать прогноз)
        for weather in forecaster.forecast:
            date = datetime.fromtimestamp(weather.reference_time())
            if date >= tomorrow:
                # показатели
                status = weather.detailed_status
                temp = round(weather.temperature('celsius')['temp'])
                hum = weather.humidity
                wind = round(weather.wind()['speed'])

                # добавляем к статусу соответствующий смайлик
                if 'ясно' in str(weather.detailed_status):
                    smile = '☀️'

                elif 'небольшая облачность' in str(weather.detailed_status) or 'переменная облачность' in str(weather.detailed_status):
                    smile = '🌤️'

                elif 'облачно с прояснениями' in str(weather.detailed_status):
                    smile = '⛅'

                elif 'пасмурно' in str(weather.detailed_status) or 'полностью облачно' in str(weather.detailed_status):
                    smile = '☁️'

                elif 'кратковременный дождь' in str(weather.detailed_status):
                    smile = '🌧️'

                elif 'дождь' in str(weather.detailed_status):
                    smile = '☔'

                elif 'гроза' in str(weather.detailed_status):
                    smile = '⛈️'

                elif 'снег' in str(weather.detailed_status):
                    smile = '❄️'

                elif 'туман' in str(weather.detailed_status):
                    smile = '🌫️'

                else:
                    smile = ''

                # склоняем градусы
                if str(1) in str(temp):
                    grad = 'градус'
                elif 2 <= int(temp) <= 4 or -2 >= int(temp) >= -4:
                    grad = 'градуса'
                else:
                    grad = 'градусов'
            
                # формируем ответ и отправляем его
                text = f'Завтра в городе {city} будет {status}{smile}\n🌡️ Температура: {temp} {grad} по Цельсию\n💨 Ветер: {wind} м\с\n💧 Влажность будет составлять {hum} %'
                bot.send_message(message.chat.id, text)
                print(f'Отправлен прогноз пользователю {message.from_user.id}')
                break

    # если что-то пошло не так, отправляем сообщение пользователю об ошибке
    except:
        bot.send_message(message.chat.id, f'Упс, что-то пошло не так. \nСкорее всего \'{city}\' не город.\nПроверьте правильность написания названия города.')
        print(f'Ошибка в прогнозе у пользователя {message.from_user.id}')
bot.polling()
print('Бот выключен')




