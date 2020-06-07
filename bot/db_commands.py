from dataclasses import dataclass
from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError


@dataclass
class DBCommands:
    pool: Connection
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
