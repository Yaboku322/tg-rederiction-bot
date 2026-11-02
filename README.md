# tg-redirection-bot

Бот для анонимной связи с администратором.
Пользователь пишет боту, сообщение пересылается админу.
Админ может ответить или отклонить запрос.
Хранит историю сообщений.
Выводит последние 10 сообщений по команде /history.
Отменяет режим ответа по команде /cancel.

in english:
A bot for anonymous communication with an administrator.
A user sends a message to the bot, and the message is forwarded to the administrator.
The administrator can then respond or decline the request.
Stores message history.
Displays the last 10 messages when the /history command is used.
Сancels response mode via the /cancel command.


## Technology
- SQLite (the database)
- Python
- pyTelegramBotAPI
- andro-cfw (обход блокировок)

in english:
- andro-cfw (bypassing blocks)

# Start
1. Создать '.env' с 'TOKEN' и 'ADMIN_ID'.
2. 'pip install -r requirements.txt'
3. 'python 1petproject_tgBOT.py'

in english:
1. Create '.env' with 'TOKEN' and 'ADMIN_ID'.
2. 'pip install -r requirements.txt'
3. 'python 1petproject_tgBOT.py'
