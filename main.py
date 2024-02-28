import mysql.connector
import random
import telebot

# Подключение к базе данных
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bot_db"
)
mycursor = mydb.cursor()

# Создание таблицы, если она не существует
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, name VARCHAR(255), phone_number VARCHAR(255), project_awareness VARCHAR(255), call_time VARCHAR(255), source VARCHAR(255), random_number INT, PRIMARY KEY (id))")

# Создание бота
bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создание нового пользователя
    mycursor.execute("INSERT INTO users (name, phone_number, project_awareness, call_time, source, random_number) VALUES (%s, %s, %s, %s, %s, %s)", (None, None, None, None, None, None))
    mydb.commit()

    # Получение ID пользователя
    mycursor.execute("SELECT id FROM users WHERE name IS NULL")
    user_id = mycursor.fetchone()[0]

    # Отправка приветственного сообщения
    bot.send_message(message.chat.id, "Привет! Давайте познакомимся.")

    # Отправка сообщения с просьбой ввести ФИО
    bot.send_message(message.chat.id, "Пожалуйста, введите ваше ФИО:")
    bot.register_next_step_handler(message, get_name, user_id)

# Обработчик ввода ФИО
def get_name(message, user_id):
    # Обновление имени пользователя
    mycursor.execute("UPDATE users SET name = %s WHERE id = %s", (message.text, user_id))
    mydb.commit()

    # Отправка сообщения с просьбой ввести номер телефона
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш номер телефона:")
    bot.register_next_step_handler(message, get_phone_number, user_id)

# Обработчик ввода номера телефона
def get_phone_number(message, user_id):
    # Проверка правильности введенного номера телефона
    if not message.text.isdigit() or len(message.text) != 11:
        bot.send_message(message.chat.id, "Некорректный номер телефона. Пожалуйста, введите номер телефона в формате +79123456789:")
        bot.register_next_step_handler(message, get_phone_number, user_id)
        return

    # Обновление номера телефона пользователя
    mycursor.execute("UPDATE users SET phone_number = %s WHERE id = %s", (message.text, user_id))
    mydb.commit()

    # Отправка сообщения с просьбой указать, знает ли пользователь о необходимом проекте
    bot.send_message(message.chat.id, "Знаете ли вы о необходимом проекте? (Да/Нет)")
    bot.register_next_step_handler(message, get_project_awareness, user_id)

# Обработчик ввода информации о знании проекта
def get_project_awareness(message, user_id):
    # Обновление информации о знании проекта
    mycursor.execute("UPDATE users SET project_awareness = %s WHERE id = %s", (message.text, user_id))
    mydb.commit()

    # Отправка сообщения с просьбой указать удобное время для звонка
    bot.send_message(message.chat.id, "Укажите удобное время для звонка:")
    bot.register_next_step_handler(message, get_call_time, user_id)

# Обработчик ввода удобного времени для звонка
def get_call_time(message, user_id):
    # Обновление информации об удобном времени для звонка
    mycursor.execute("UPDATE users SET call_time = %s WHERE id = %s", (message.text, user_id))
    mydb.commit()

    # Отправка сообщения с просьбой указать, откуда пользователь узнал о боте
    bot.send_message(message.chat.id, "Откуда вы узнали о нас?")
    bot.register_next_step_handler(message, get_source, user_id)

# Обработчик ввода источника информации о боте
def get_source(message, user_id):
    # Обновление информации об источнике информации о боте
    mycursor.execute("UPDATE users SET source = %s WHERE id = %s", (message.text, user_id))
    mydb.commit()

    # Генерация случайного номера
    random_number = random.randint(1, 100)

    # Обновление случайного номера пользователя
    mycursor.execute("UPDATE users SET random_number = %s WHERE id = %s", (random_number, user_id))
    mydb.commit()

    # Подготовка сообщения с результатом
    result_message = "Ваши данные успешно сохранены."
    result_message += f"\nФИО: {message.from_user.first_name}"
    result_message += f"\nНомер телефона: {message.from_user.phone_number}"
    result_message += f"\nЗнание о проекте: {message.text}"
    result_message += f"\nУдобное время для звонка: {message.text}"
    result_message += f"\nИсточник информации о боте: {message.text}"
    result_message += f"\nВаш случайный номер: {random_number}"

    # Отправка сообщения с результатом
    bot.send_message(message.chat.id, result_message)

# Запуск бота
bot.polling()
```