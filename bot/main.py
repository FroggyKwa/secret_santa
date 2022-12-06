from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler
from methods import *
from db.models import create_tables


if __name__ == '__main__':
    create_tables()
    TOKEN = '5005415883:AAEhstGVL9vXscgcc6ZXHlrJay3YPbA54RE'
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    get_name_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={0: [MessageHandler(None, start)],
                1: [MessageHandler(None, get_name)]},
        fallbacks=[CommandHandler('end', end)]
    )
    dispatcher = updater.dispatcher
    dispatcher.add_handler(get_name_conversation_handler)
    dispatcher.add_handler(CommandHandler('help', get_info))
    dispatcher.add_handler(CommandHandler('received', received))
    dispatcher.add_handler(CommandHandler('sent', sent))
    dispatcher.add_handler(CommandHandler('get_recipient', get_recipient))

    updater.start_polling()
