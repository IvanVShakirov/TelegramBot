import re
from aiogram import types


def reg_handlers(dp, bot, db):
    @dp.message_handler(commands=["start"])
    async def register_user(message: types.Message):
        chat_id = message.from_user.id
        id = await db.add_new_user()
        count_users = await db.count_users()
        text = ""
        if not id:
            id = await db.get_id()  # TODO unused variable; `id` is a built-in function
        else:
            text += "Новый пользователь создан. Добро пожаловать"
        text += f"""Сейчас в базе {count_users} человек"""

        await bot.send_message(chat_id, text)

    @dp.message_handler(commands=["help"])
    async def help(message: types.Message):
        chat_id = message.from_user.id
        text = "Доступные команды" \
               + "\n" + "(вводить без звездочек)" \
               + "\n" + "send *текст документа*" \
               + "\n" + "send_answer *номер документа* *текст ответа*" \
               + "\n" + "delete_doc *номер документа*" \
               + "\n" + "delete_answer *номер документа*" \
               + "\n" + "get_doc *номер документа*" \
               + "\n" + "get_answer *номер документа*" \
               + "\n" + "get_doc_list -список документов" \
               + "\n" + "get_answer_list - список ответов"
        await bot.send_message(chat_id, text)

    @dp.message_handler(regexp="/send .*")
    async def send_doc(message: types.Message):
        text = message.text
        await db.add_new_doc(text[6:])

    @dp.message_handler(regexp="/send_answer \d{1,3} .*")
    async def send_answer(message: types.Message):
        text = message.text
        id = re.match(r'.*\d{1,3}', text[12:15])
        text = text[12 + len(id[0]):]
        await db.add_new_answer(text, int(id[0]))

    @dp.message_handler(regexp="/delete_doc \d{1,3}")
    async def delete_doc(message: types.Message):
        text = message.text
        id = re.match(r'\d{1,3}', text[11:])
        await db.delete_doc(int(id[0]))

    @dp.message_handler(regexp="/delete_answer \d{1,3}")
    async def delete_answer(message: types.Message):
        text = message.text
        id = re.match(r'.*\d{1,3}', text[14:])
        await db.delete_answer(int(id[0]))

    @dp.message_handler(regexp="/get_doc \d{1,3}")
    async def get_doc(message: types.Message):
        text = message.text
        chat_id = message.from_user.id
        id = re.match(r'.*\d{1,3}', text[8:])
        text = await db.get_doc(int(id[0]))
        await bot.send_message(chat_id, text)

    @dp.message_handler(regexp="/get_answer \d{1,3}")
    async def get_doc(message: types.Message):
        text = message.text
        chat_id = message.from_user.id
        id = re.match(r'.*\d{1,3}', text[11:])
        text = await db.get_answer(int(id[0]))
        await bot.send_message(chat_id, text)

    @dp.message_handler(regexp="/get_doc_list")
    async def get_doc_list(message: types.Message):
        chat_id = message.from_user.id
        result = await db.get_doc_list()
        text = ""
        for row in result:
            text += f"id: {str(row[0])} | author: {str(row[1])} | text: {str(row[2])[:25]}...\n"

        await bot.send_message(chat_id, text)

    @dp.message_handler(regexp="/get_answer_list")
    async def get_doc_list(message: types.Message):
        chat_id = message.from_user.id
        result = await db.get_doc_list()
        text = ""
        for row in result:
            text += f"id: {str(row[0])} | answer: {str(row[3])[:30]}...\n"

        await bot.send_message(chat_id, text)
