import random
import re
from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from load_all import bot, dp, db


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    ADD_NEW_DOC = "INSERT INTO document(document_text,document_creator) VALUES ($1, $2) RETURNING id"
    ADD_NEW_ANSWER = "UPDATE document SET document_answer= $1 WHERE id =$2"
    DELETE_ANSWER = "UPDATE document SET document_answer= $1 WHERE id =$2"
    DELETE_DOC = "DELETE FROM document WHERE id=$1"
    GET_DOC = "SELECT * FROM document WHERE id=$1"
    GET_ANSWER = "SELECT * FROM document WHERE id=$1"
    GET_DOC_LIST = "SELECT * FROM document"
    GET_DOC_LIST_BY_USER = "SELECT * FROM document WHERE document_creator =$1"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"

    async def add_new_user(self):
        user = types.User.get_current()
        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name
        command = self.ADD_NEW_USER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def add_new_doc(self, doc_text):
        user = types.User.get_current()
        doc_creator = user.full_name
        args = doc_text, doc_creator
        command = self.ADD_NEW_DOC
        await self.pool.fetchval(command, *args)

    async def delete_doc(self, id):
        command = self.DELETE_DOC
        await self.pool.fetchval(command, id)

    async def get_doc(self, id):
        command = self.GET_DOC
        row = await self.pool.fetchrow(command, id)
        return row["document_text"]

    async def get_doc_list(self):
        command = self.GET_DOC_LIST
        row = await self.pool.fetch(command)
        return row

    async def get_doc_list_by_user(self, username):
        command = self.GET_DOC_LIST_BY_USER
        row = await self.pool.fetch(command, username)
        return row

    async def get_answer(self, id):
        command = self.GET_ANSWER
        row = await self.pool.fetchrow(command, id)
        return row["document_answer"]

    async def add_new_answer(self, doc_answer, id):
        args = doc_answer, id
        command = self.ADD_NEW_ANSWER
        await self.pool.fetchval(command, *args)

    async def delete_answer(self, id):
        args = "", id
        command = self.ADD_NEW_ANSWER
        await self.pool.fetchval(command, *args)

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record


db = DBCommands()


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    id = await db.add_new_user()
    count_users = await db.count_users()
    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Новый пользователь создан. Добро пожаловать"
    text += f"""
Сейчас в базе {count_users} человек
"""

    await bot.send_message(chat_id, text)


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    chat_id = message.from_user.id
    text = "Доступные команды" + "\n" + "(вводить без звездочек)" \
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
        text += "id : " + str(row[0]) + " | " + "author : " + str(row[1]) + " | " + "text : " + str(row[2])[
                                                                                                :25] + "..." + "\n"

    await bot.send_message(chat_id, text)


@dp.message_handler(regexp="/get_answer_list")
async def get_doc_list(message: types.Message):
    chat_id = message.from_user.id
    result = await db.get_doc_list()
    text = ""
    for row in result:
        text += "id : " + str(row[0]) + " | " + "answer : " + str(row[3])[:30] + "..." + "\n"

    await bot.send_message(chat_id, text)
