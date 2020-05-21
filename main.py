'''Importing class ManageUser from support'''
import support
from functools import wraps
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import yaml
from telegram import InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup, ChatAction
import os
from uuid import uuid4
import logging
from telegram.ext import InlineQueryHandler
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


'''creating a ManageUser obj'''
users = support.ManageUser()

'''
user.newUser(id) -> returns(-1) if(queue is empty) wait untill a stranger is found 
user.newUser(id) -> returns(id of another user) 
'''


def start(update, context):
    chatId = update.effective_chat.id
    if(users.isInDec(chatId) == -1) or (users.isInDec(chatId) == -2):
        if (users.isInDec(chatId) == -2):
            context.bot.send_message(chat_id=chatId, text="BOT : Welcome")
            if users.newUser(chatId) == -1:
                context.bot.send_message(
                    chat_id=chatId, text="BOT : Wait.... we are trying to match you!!.....")
            else:
                context.bot.send_message(
                    chat_id=chatId, text="BOT : We matched you to a stranger ")
                context.bot.send_message(chat_id=users.isInDec(
                    chatId), text="BOT : We matched you to a stranger ")
                print("INFO : ", chatId, " --- ", users.isInDec(chatId))
        else:
            context.bot.send_message(
                chat_id=chatId, text="BOT : Please Wait....Your in a queue... we are trying to match you!!.....")
    else:
        context.bot.send_message(
            chat_id=chatId, text="BOT : You are already matcher to a stranger... '/stop' to End it")


'''
when user send some message it forwards to the matched user using the dictionary in the object
isInDec - is in dictionary
users.isInDec(chatId) ->  returns -1, if(queue is empty)
users.isInDec(chatId) ->  returns -2, if(end the conversation)
users.isInDec(chatId) ->  returns(ID) if he is in the dictionary
'''


def echo(update, context):
    chatId = update.effective_chat.id
    if(users.isInDec(chatId) == -1):
        context.bot.send_message(
            chat_id=chatId, text="BOT : Wait.... we are trying to match you!!.....")
    elif(users.isInDec(chatId) == -2):
        context.bot.send_message(
            chat_id=chatId, text="BOT : Press '/start' to Start a New connection")
    else:

        query = update.message.text
        # print(update.message)
        context.bot.send_message(chat_id=users.isInDec(chatId), text=query)


'''When user ends the conversation'''


def stop(update, context):
    chatId = update.effective_chat.id

    if(users.isInDec(chatId) == -1):
        context.bot.send_message(
            chat_id=chatId, text="BOT : Sorry for your inconvenience ... Thanls for Using...")
        users.delOneFromQueue(chatId)
    elif(users.isInDec(chatId) == -2):
        context.bot.send_message(
            chat_id=chatId, text="BOT : Press '/start' to Start a New connection")
    else:
        context.bot.send_message(
            chat_id=chatId, text="BOT : You are Disconnected from the Stranger...")
        context.bot.send_message(chat_id=users.isInDec(
            chatId), text="BOT : You are Disconnected from the Stranger...")
        # del the ids from the dictionary
        users.delFromDic(chatId, users.isInDec(chatId))


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config = yaml.load(
        open(os.path.join(base_path, 'config.yaml')).read(), Loader=yaml.FullLoader)
    updater = Updater(token=config['general']['token'], use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
