import random
import grpc
import rpc_pb2
import rpc_pb2_grpc

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import aiogram
from aiogram import Bot, Dispatcher, types

# Firebase Admin SDK here
key = {
  "type": "service_account",
  "project_id": "grpc-ada9b",
  "private_key_id": "86f38cdb21f811c0a23b5d1e8603bd9f6fce538d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDWB5CI+5/TXQtB\nLgdCVLWZgo/Xq4WWaRNG0eDa7gDy9JX3tSgRDSb8cmENeCDDC8FbnQ1427urXKJI\nY/TCMDFLN2CgH8b74vHzisvN+j2sTlK9MFoXKa+u3EwnaKiAoEiUd+3fIUXHgFhK\n11xtlKc4bG7+G51wPbhRjvyFuIwVGr2R0HI6AloRMScB++tyfL7uHfEPlx8lwZFV\n7XvdFEKkaoylKAliQdjzCMMpq6JFUKReoHztUkwYfLmggdb9UWe4ZlbCB41wJetn\nj6uuLOu9Cm6VLvYsLBBLGNflM9qVrBxFbzS+TaSWguMjPMcCM5TfiBLK9rz6w8R7\ne73vhptnAgMBAAECggEAaEbDOpotolMAur7sNnsDB0m/PzqIGWIUTDrRLJksyTI1\nJrySSsx3pCMt+dv/Skgd6r6345xa8QBu6Ioao8nLGnRelWUmE27cpuWGqlIzXhHC\n6f32xrY+rBkU2VZ6UkDFW+Caek3Bq5NycPRASftVBX5/DTrzF85aURIzIgtp5JWA\ng9ernu/Ljw1aNKLJDeAiiDzyVG3cxcyHtvkj6Z4VB8wzlEHqFbTZMtuD1f02tzhF\nL+4U71gpwG/Cy90OlfiNfIA/waD/vJobuwjl+GmNvVQ2oVUEnv2ArehzKpLBpTOs\nVMrgqhEZ6b71XtDoxMnXeI5jLfClFuSdar5wRNOnAQKBgQDvoElr5nRRGaWk3Vea\nmhiwweGUkyr/8dqBf5jaoyiMeHAFSnunc+ybOlC/iygyAKqj0BAjFPN7lul3T0lo\nC3BDvJfili6x5w6V/dWbV+TFluv+bG3zD0YvQkCX/USY+QttV+DizMip0lmIirSh\ntOr348LQlS56E0yLF1TDj6aAQQKBgQDkp4YpwlBT/QFvr9WcMFVtmDRCTkWYkzBI\nLCS51YJXBUavLoA0AnMTOyBZTG//lhEQq6hIzfRt0ky6FhWRy/7XhRnVJwO1V9lC\nWqoycv0KHM2Knuc5YCHOBYxpQJO+C1r3b1Fwc1t7Hsjo9QD9R9/7dX5zKZzxPcC5\n+0zQDDyxpwKBgGlTJLJ+mwXCpiIvAAB+VvfqYEKz5SSWo5pkAUWojXwgu+w3bt6N\nf6RDH5bxjXtc+6QBIfapkNPz4y6D9Rn8XR4I2SHJLUEY9DpNVgRvv6hxy80Kz9EU\nF59SGZ40vmAWp0UqaTiHFnQ+dwgjH34sTVMkE08nI0SZEv3YBXPnwiGBAoGAJhz2\ndAd7tEQ79Q3uITa9RqNUMqkxWJlQNveEt6UrMK4kdhbeL80ouU/luHzRPl0ZQxoZ\n1ujdkWC4gVwlBERomiwJfkoeiB+4iyLps7cPDpx2dmC+UgYAHIM4QGMPPWJPK2dW\nv9O6r+8Vth8ApzdP0m5nQXLyQhP1CAsnZpZjl4kCgYEA6P556hUIeL8W33GYFFqb\nelWEz9tF7w97ySTJCY1B3VXukAyd9kc/LaG/tHLJqe9o7nfsmYZl6OF9fkE/IIgm\nr+AeEFCLiFNbq5+mVR6+/zKvKT0cW/RgaPaIWj7GTzl8Z+Veajk8Ctz7HVbmHKRi\nGIXRN2h1ahANmX8ZIhkXCLE=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-73d11@grpc-ada9b.iam.gserviceaccount.com",
  "client_id": "118417854839209851509",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73d11%40grpc-ada9b.iam.gserviceaccount.com"
}

# Initialize Firebase credentials
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# Initialize Telegram bot and dispatcher
bot = Bot("6172454074:AAFhBfGi0sJesjemvZzSuJPy52YKbyEyH-o")
dp = Dispatcher(bot)

# Create gRPC channel and stub
channel = grpc.insecure_channel('localhost:50051')
stub = rpc_pb2_grpc.FirestoreStub(channel)

### Telegram Bot Command Handler

# Sends message after /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer('Hello! welcome to grpc_bot!')  
  
# Sends message after /help
@dp.message_handler(commands=['help'])
async def welcome(message: types.Message):
    await message.answer('To add, type /get <your msg>')
    await message.answer('To get, type /get <your code>')
    await message.answer('To update, type /update <your code> <your msg>') 
    await message.answer('To delete, type /delete <your code>')       

# Handle /add <msg> command, then add it to database
@dp.message_handler(commands=['add'])
async def add_document(message: types.Message):
    # Extract msg from the message
    msg = message.text.split(' ')[1]
    # Generate a random 9-digit ID
    new_code = str(random.randint(100000000, 999999999))
    
    # Call the AddDocument method from your gRPC stub
    response = stub.AddDocument(rpc_pb2.Document(code=new_code, name=msg))
    
    # Send confirmation message to the user
    await message.reply(f"New document added with code: {new_code}")

# Handle /get <code> command, then send to the user
@dp.message_handler(commands=['get'])
async def get_document(message: types.Message):
    # Extract code from the message
    code = message.text.split(' ')[1]
    
    # Call the GetDocument method from your gRPC stub
    response = stub.GetDocument(rpc_pb2.DocumentRequest(code=code))
    
    # Send confirmation message to the user
    await bot.send_message(chat_id=message.chat.id, text=response.name)
    
# Handle /update <code> <msg> command, then update the corresponding document
@dp.message_handler(commands=['update'])
async def update_document(message: types.Message):
    # Extract code and new msg from the message
    args = message.text.split(' ')
    code = args[1]
    new_msg = args[2]
    
    # Call the UpdateDocument method from your gRPC stub
    stub.UpdateDocument(rpc_pb2.DocumentUpdate(code=code, name=new_msg))
    
    # Send confirmation message to the user
    await message.reply(f"Document with code {code} has been updated with: {new_msg}")

# Handle /delete <code> command, then delete the corresponding document
@dp.message_handler(commands=['delete'])
async def delete_document(message: types.Message):
    # Extract code from the message
    code = message.text.split(' ')[1]
    
    # Call the DeleteDocument method from your gRPC stub
    stub.DeleteDocument(rpc_pb2.DocumentRequest(code=code))
    
    # Send confirmation message to the user
    await message.reply(f"Document with code {code} has been deleted")


### Execute

if __name__ == '__main__':
    # Start the Telegram bot
    aiogram.executor.start_polling(dp, skip_updates=True)
