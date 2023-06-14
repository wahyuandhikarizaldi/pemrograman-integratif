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
  "<YOUR-SDK-HERE>"
}

# Initialize Firebase credentials
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# Initialize Telegram bot and dispatcher
bot = Bot("<YOUR-BOT-TOKEN-HERE>")
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
