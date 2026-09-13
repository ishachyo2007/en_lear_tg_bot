from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
import asyncio
from bot_database import *
import random as rm
import os

session = AiohttpSession(proxy="")
bot = Bot(token="", session=session)
dp = Dispatcher()

start_quiz = False
answer_count = 0
word_now = ""
quiz_question = []

@dp.message(Command("start"))
async def start_hello(mess: types.Message):
    await mess.answer("Hello! This bot is designed to help you memorize English words. Add words with translations to this bot, and the bot will periodically give you quizzes with these words.\nFor a detailed description of the bot's commands, use /help.")

@dp.message(Command("help"))
async def echo_us_ans(mess: types.Message):
    await mess.answer("/add word translate - adds a new element to the bot's general vocabulary.\n/list - shows a list of all previously entered words.\n/delete word- removes a word from the list by its text (or translated text).\n/quiz - starts a quiz using words from the list.\n/reset - clears the current list of words.")

@dp.message(Command("add"))
async def us_add(mess: types.Message):
    sq_add_user(mess.from_user.id)
    try:
        word = mess.text.split(" ")[1]
        trans = mess.text.split(" ")[2]
        await mess.answer(sq_add_word(mess.from_user.id, word, trans))
    except:
        await mess.answer("Error!\n/add word translate\nonly in this order. neither the word itself nor its translation should be a combination of words. also, try to avoid adding special characters to words.")

@dp.message(Command("delete"))
async def del_word(mess: types.Message):
    try:
        await mess.answer(sq_del_word(mess.from_user.id, mess.text.split(" ")[1]))
    except:
        await mess.answer("Error!\n/delete word\nonly in this order. the word should not be a combination of words. also, try to avoid adding special characters to words.")

@dp.message(Command("list"))
async def list_all_words(mess: types.Message):
    string_words = ""
    for i in sq_word_list(mess.from_user.id):
        string_words += ("  " + i + "\n")
    await mess.answer(f"Here are all your words:\n{string_words}")

@dp.message(Command("quiz"))
async def main_quiz(mess: types.Message):
    global start_quiz, word_now, answer_count, quiz_question
    quiz_question, _ = quiz(mess.from_user.id)
    if len(quiz_question) == 0:
        await mess.answer("All the words have been learned, or there are no words.")
        return 0
    if start_quiz:
        await mess.answer("A quiz is underway. If you want to end it, press - /stop")
        return
    start_quiz = True
    word_now = quiz_question[rm.randrange(0, len(quiz_question))]
    answer_count = len(quiz_question)
    await mess.answer(f"Enter the translation of this word: {word_now}")

@dp.message()
async def check_quiz(mess: types.Message):
    global start_quiz, word_now, answer_count, quiz_question
    if start_quiz:
        if answer_count > 0:
            if mess.text.lower() == true_answer(mess.from_user.id)[word_now]["translation"]:
                await mess.answer(f"Right! Word knowledge level +1")
                upgrade_level(mess.from_user.id, word_now, 1)
            else:
                await mess.answer("Incorrect! Word knowledge level -1")
                upgrade_level(mess.from_user.id, word_now, -1)
            answer_count -= 1
            quiz_question.remove(word_now)
            if len(quiz_question) > 0:
                word_now = quiz_question[rm.randrange(0, len(quiz_question))]
                await mess.answer(f"Enter the translation of this word: {word_now}")
            else:
                await mess.answer("The quiz is completed.")
                start_quiz = False
        return 0
    await mess.answer("what?")



async def main():
    await dp.start_polling(bot)

asyncio.run(main())