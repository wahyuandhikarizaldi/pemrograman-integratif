# Telegram Bot with gRPC API and Protobuf

## Library
- firebase_admin : For database
- aiogram : For Telegram bot

## How the bot works?
- /add "your-msg" to add new doc to the database.
- /get "your-code" to get the specified doc then send it to the client.
- /update "your-code" "your-msg" to edit the specified doc.
- /delete "your-msg" to delete the specified doc.
