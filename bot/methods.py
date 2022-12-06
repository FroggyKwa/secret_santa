import telegram
from telegram import Update
from telegram.ext import CallbackContext
from db.models import Person, RelationShip


def get_name(update, context):
    name = update.message.text
    if len(name.split()) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введи фамилию и имя. 🤓')
        return 1
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Приятно познакомиться, {name}!\nВведи /start ещё раз, чтобы продолжить!')
    Person.create(id=update.effective_chat.id, username=update.effective_chat.username, name=name)
    return 0


def start(update: telegram.Update, context: CallbackContext):
    if not Person.select().where(Person.id == update.effective_chat.id).exists():
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Как тебя зовут? (Желательно фамилию и имя, чтобы твой санта знал, что подарок нужно подарить именно тебе)')
        return 1
    text = f'''Привет, мой многоуважаемый эмигрант - {update.effective_chat.full_name}! 🥸\nСогласись, что получать 🎁подарки🎁 на Новый год🎄 приятно, а дарить их еще приятнее. 😊\nПоэтому я создан для того, чтобы дарить радость нам, эмигрантам.\n\nПрикольно было бы организовать 🎅тайного санту🎅, чтобы получить подарок и подарить его своему другу/подруге. 😋\nСейчас расскажу, как это всё работает:\n\n1) Ты покупаешь какую-нибудь штуку в пределах 1000 рублей (минимума нет, можешь хоть шоколадку купить, получателю будет приятно не от суммы подарка, а от факта подарка 😋\n\n2) Когда решился дарить подарок, то пиши мне /get_recipient, после этого я запишу того, кому ты даришь подарок и ты, мой дорогой друг, должен будешь подарить подарок до 31 декабря🎄 (или немного позже, если тебя сейчас нет в Приморском крае)\n\n3) Если ты не хочешь дарить подарок человеку, который выпал тебе рандомно, то, пожалуйста, отбрось все нехорошие мысли про этого человека, ты дед мороз и ты даришь подарки даже самым негодяйским негодяям🤪. Подари радость и тебе вернётся вдвойне 💖\n\n4) Конечно, если тебе лень или никак не получается купить подарок, то ты волен ничего не дарить, но подумай сам, если не подаришь ты, то никто не подарит, потому что этот человек уже будет занят, как получатель (менять получателей нельзя, в этом весь смысл). А таким человеком, оставшимся без подарка, можешь быть и ты, мой друг, поэтому постарайся и не накосячь!😢\n\nНапиши /help, чтобы ознакомиться со всем функционалом '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return -1


def end(update, context):
    return -1


def get_info(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Команды бота:\n\n/start - стартует бота и присылает правила;\n\n/help - выводит список команд; \n\n/get_recipient - делает тебя Сантой и даёт задание подарить кому-то из эмигрантов улыбку \n\n/sent - присылает Санта, когда отправил подарок. Эта команда пришлёт уведомление получателю, что ему стоит в близжайшее время ждать подарок.\n\n/received - присылает получатель подарка, информируя Санту об этом и повышая карму отправителя.')


def get_recipient(update: telegram.Update, context: CallbackContext):
    from random import choice
    if not Person.select().where(Person.id == update.effective_chat.id).exists():
        return
    donor = Person.get_by_id(update.effective_chat.id)
    if RelationShip.select().where(RelationShip.donor == donor):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Главный Санта гордится твоей добротой и желанием дарить подарки всем, но для начала подари подарок назначенному тебе получателю, а потом мы уже подумаем, сможешь ли ты поднять настроение кому-нибудь еще! (подарков ведь много не бывает)🎁')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Напоминаю, твой подарок должен получить - {RelationShip.select().where(RelationShip.donor == donor)[0].recipient.name}')
        return
    not_used = list(Person.select().where((Person.is_recipient == False) & (Person.id != donor.id)))
    if not not_used:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='К сожалению свободных получателей пока нет.\n\n Дорогой друг, я предлагаю тебе подождать некоторое время и попробовать ввести /get_recipient снова. Тебя в список пользователей без санты я внёс. 😇')
        return
    recipient = choice(not_used)
    RelationShip.create(donor=donor, recipient=recipient)
    recipient.is_recipient = True
    recipient.save()
    context.bot.send_message(chat_id=recipient.id,
                             text='Для тебя нашёлся тайный санта! 🎅\n\nТеперь ты можешь написать команду /received, когда получишь подарок, тем самым повысив карму твоего Санты.')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Поздравляю! По воле бога рандома ты даришь подарок - {recipient.name}')


def received(update, context):
    if Person.get_by_id(update.effective_chat.id).is_recipient:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Поздравляю с наступающим новым годом! Спасибо, что уделил время этой игре, а тот факт, что подарок всё-таки достался тебе говорит, что всё прошло не зря.\n Благодарю за участие.')
        donor = RelationShip.select().where(RelationShip.recipient == Person.get_by_id(update.effective_chat.id))[0].donor
        context.bot.send_message(chat_id=donor.id,
                                 text='Ты хорошо потрудился. Твой подарок был получен! Уверен, что тот, кому достался твой подарок искренне улыбался и радовался, получив его! Спасибо за проделанную работу! :)')
        donor.karma_level += 1 if not donor.karma_level else 0
        donor.save()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ты не можешь использовать эту команду, т.к. твой Санта еще не нашёлся.')


def sent(update: Update, context: CallbackContext):
    relation = RelationShip.select().where(RelationShip.donor == Person.get_by_id(update.effective_chat.id))
    if relation.exists():
        relation = relation[0]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ты не являешься Сантой и поэтому не можешь писать эту команду.\n\n...точнее можешь, но ничего не произойдёт, охохо')
        return
    donor = relation.donor
    context.bot.send_message(chat_id=donor.id, text='Спасибо, что потрудился и отправил подарок!\n\nЯ напишу тебе, когда получатель наконец-то найдёт его под ёлочкой. Или куда там ты его спрятал..? :)')
    recipient = relation.recipient
    context.bot.send_message(chat_id=recipient.id, text='Твой подарок был отправлен!\nТвоя задача теперь найти его, улыбнуться и написать /received, чтобы дать понять Санте, что ты получил всё, что нужно!')

