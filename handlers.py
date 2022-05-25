from faunadb.client import FaunaClient
from faunadb import query as q
import os
from dotenv import load_dotenv
from telegram.ext import ConversationHandler

load_dotenv()


START, ADD_USER, BUSINESS_INFO, ADD_PRODUCTS = range(4)

client = FaunaClient(
    os.getenv("FAUNA_TOKEN"),
    domain="db.eu.fauna.com"
)


def start(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    bot.send_message(
        text="Hi fellow, Welcome to SMEbot ,"
        "Please tell me about yourself, "
        "provide your full name, email, and phone number, "
        "separated by comma each e.g: "
        "John Doe, JohnD@gmail.com, +234567897809",
        chat_id=chat_id
    )
    return ADD_USER


def add_new_user(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    data = update.message.text.split(',')
    print(data)
    if len(data) != 3:
        bot.send_message(
            chat_id=chat_id,
            text="Invalid entry, please make sure to input the details "
            "as requested in the instructions"
        )
        bot.send_message(
            chat_id=chat_id,
            text="Type /start, to restart bot"
        )
    new_user = client.query(
        q.create(
            q.collection("User"),
            {
                "data": {
                    "name": data[0],
                    "email": data[1],
                    "tel": data[2],
                    "chat_id": chat_id
                }
            }
        )
    )
    print(new_user)
    bot.send_message(
        chat_id=chat_id,
        text="Collected information succesfully!..🎉🎉 \n"
        "Please enter the details of your business."
        "provide your BrandName, Brand email, Address, and phone number"
        "in that order, each separated by comma(,) each e.g: "
        "JDWears, JDWears@gmail.com, 101-Mike Avenue-Ikeja, +234567897809"
    )
    return BUSINESS_INFO


def update_biz_info(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    data = update.message.text.split(',')
    if len(data) != 4:
        bot.send_message(
            chat_id=chat_id,
            text="Invalid entry, please try again"
        )
    new_business = client.query(
        q.collection('Business', {
            'data': {
                "name": data[0],
                "email": data[1],
                "address": data[2],
                "telephone": data[3]
            }
        })
    )
    print(new_business)
    bot.send_message(
        chat_id=chat_id,
        text="Collected information succesfully!..🎉🎉 \n"
    )
    return ADD_PRODUCTS

def cancel(update, context):
    return ConversationHandler.END
