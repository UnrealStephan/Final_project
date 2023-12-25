import telebot
import time
from telebot import types
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('train_clean.csv')
df.head()
columns_train = df.columns[:-1:]
columns_target = df.columns[-1]
Y = df[columns_target]
X = df[columns_train]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
model = LogisticRegression(C = 0.008858667904100823)
model.fit(X_train, Y_train)
train_predictions = model.predict(X_test)

def Jarvis(passenger_data):
    X_test = passenger_data
    answer = model.predict(X_test)
    return answer

bot = telebot.TeleBot('6446106930:AAFegtVAO31RmcAAduisqcrU1lQFPKw-BXM')

@bot.message_handler(commands=['start'])
def welcome(message):

  bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!\n'
                                    'Напишите одной строкой следующие данные о пассажире:\n'
                                    'HomePlanet (Europa / Earth / Mars)\n'
                                    'CryoSleep (TRUE / FALSE)\n'
                                    'Destination (TRAPPIST-1e / PSO J318.5-22 / 55 Cancri e)\n'
                                    'Age\n'
                                    'VIP (TRUE / FALSE)\n'
                                    'RoomService\n'
                                    'FoodCourt\n'
                                    'ShoppingMall\n'
                                    'Spa\n'
                                    'VRDeck\n'
                                    'А я предскажу, будет ли пассажир перенесен в альтернативное измерение')

  bot.send_message(message.chat.id, 'Пример вашей строки:\nEarth	TRUE	TRAPPIST-1e	27 FALSE	0	0	0	0	0')

@bot.message_handler(commands=['help'])
def help(message):

  bot.send_message(message.chat.id, 'Бот предсказывает, будет ли пассажир перенесен в альтернативное '
                                    'измерение во время столкновения с пространственно-временной '
                                    'аномалией на космическом корабле "Титаник"')

  bot.send_message(message.chat.id, 'Напишите одной строкой следующие данные о пассажире:\n'
                                    'HomePlanet (Europa / Earth / Mars)\n'
                                    'CryoSleep (TRUE / FALSE)\n'
                                    'Destination (TRAPPIST-1e / PSO J318.5-22 / 55 Cancri e)\n'
                                    'Age\n'
                                    'VIP (TRUE / FALSE)\n'
                                    'RoomService\n'
                                    'FoodCourt\n'
                                    'ShoppingMall\n'
                                    'Spa\n'
                                    'VRDeck\n'
                                    'А я предскажу, будет ли пассажир перенесен в альтернативное измерение')

  bot.send_message(message.chat.id, 'Пример вашей строки:\nEarth	TRUE	TRAPPIST-1e	27 FALSE	0	0	0	0	0')

@bot.message_handler(content_types=['text'])
def answer(message):

  passenger_data = message.text.split()

  if len(passenger_data) < 10:
    bot.send_message(message.chat.id, 'Что-то не так с данными, пожалуйста, используйте шаблон:\nEarth	TRUE	TRAPPIST-1e	27 FALSE	0	0	0	0	0')
    return

  if passenger_data[2] == '55':
    passenger_data.remove('55')
    passenger_data.remove('Cancri')
  elif passenger_data[2] == 'PSO':
    passenger_data.remove('PSO')

  passenger_df = pd.DataFrame([passenger_data])

  passenger_df = passenger_df.replace('Earth', 0)
  passenger_df = passenger_df.replace('Europa', 1)
  passenger_df = passenger_df.replace('Mars', 2)
  passenger_df = passenger_df.replace('TRUE', 1)
  passenger_df = passenger_df.replace('FALSE', 0)
  passenger_df = passenger_df.replace('TRAPPIST-1e', 2)
  passenger_df = passenger_df.replace('J318.5-22', 1)
  passenger_df = passenger_df.replace('e', 0)
  col = passenger_df.columns.values.tolist()

  try:

    passenger_df[col] = passenger_df[col].astype(float)

  except ValueError:

    bot.send_message(message.chat.id, 'Что-то не так с данными, пожалуйста, используйте шаблон:\nEarth	TRUE	TRAPPIST-1e	27 FALSE	0	0	0	0	0')
    return

  if len(passenger_data) != 10:
    bot.send_message(message.chat.id, 'Что-то не так с данными, пожалуйста, используйте шаблон:\nEarth	TRUE	TRAPPIST-1e	27 FALSE	0	0	0	0	0')
    return

  answer = Jarvis(passenger_df)

  if bool(answer) == False:
    bot.send_message(message.chat.id, 'Этот пассажир не будет перенесен в альтернативное измерение!')
    bot.send_message(message.chat.id, 'Проверить еще пассажира?')

  elif bool(answer) == True:
    bot.send_message(message.chat.id, 'Увы, этот пассажир будет перенесен в альтернативное измерение...')
    bot.send_message(message.chat.id, 'Проверить еще пассажира?')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except ():
            time.sleep(5)
