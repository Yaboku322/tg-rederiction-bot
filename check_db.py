from database import Database

db = Database("messages.db")
messages = db.get_messages()

if not messages:
    print("Base empty.")
else:
    for msg in messages:
        print(f"ID: {msg[0]} | User: {msg[2]} | Text: {msg[3]} | Time: {msg[4]}")

db.close()