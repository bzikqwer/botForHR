import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

# Replace YOUR_TOKEN with your bot token obtained from BotFather
bot = Bot(token='6246911614:AAHByp-PFMlNViFPP3TznxNQkToiAPTVBVo')

# Initialize dispatcher and storage
dp = Dispatcher(bot, storage=MemoryStorage())

# States
class HRQuestions(StatesGroup):
    Q1 = State()  # First question state
    Q2 = State()  # Second question state
    Q3 = State()  # Third question state
    Q4 = State()
    Q5 = State()
    Q6 = State()
# Start command handler
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Conversation's entry point
    """
    # Set state to Q1

    await HRQuestions.Q1.set()

    # Create keyboard markup for first question
    q1_choices = ReplyKeyboardMarkup(resize_keyboard=True)
    # q1_choices.add(KeyboardButton('Choice A'), KeyboardButton('Choice B'))

    await message.answer("Здравствуйте! Я HR-бот компании alma+.\n\nНапишите , пожалуйста , Ваше полное ФИО? ", reply_markup=q1_choices)

# First question handler
@dp.message_handler(state=HRQuestions.Q1)
async def answer_q2(message: types.Message, state: FSMContext):
    # Save answer to state
    await state.update_data(q2_answer=message.text)

    # Create keyboard markup for second question
    q2_choices = ReplyKeyboardMarkup(resize_keyboard=True)
    q2_choices.add(KeyboardButton('да , естественно'), KeyboardButton('нет, я просто проходил(-а) мимо '))

    # Set state to Q2
    await HRQuestions.Q2.set()

    await message.answer("""Со мной будет очень интересно и информативно 😊. А самое главное, я никогда не отдыхаю, не сплю и  не обедаю. Согласны пройти со мной это увлекательное путешествие по вакансиям компании ? 
""", reply_markup=q2_choices)

@dp.message_handler(state=HRQuestions.Q2)
async def answer_q3(message: types.Message, state: FSMContext):
    # Save answer to state
    await state.update_data(q3_answer=message.text)

    # Create keyboard markup for second question
    q3_choices = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    q3_choices.add(KeyboardButton('мне нет 18 лет'), KeyboardButton('18-19'), KeyboardButton('20-29'), KeyboardButton('30-40'), KeyboardButton('41 и более'))

    # Set state to Q2
    await HRQuestions.Q3.set()

    await message.answer("""Укажите Ваш возвраст ?""", reply_markup=q3_choices)
#
@dp.message_handler(state=HRQuestions.Q3)
async def answer_q4(message: types.Message, state: FSMContext):
    # Save answer to state
    await state.update_data(q4_answer=message.text)

    # Set state to Q3
    await HRQuestions.Q4.set()

    await message.answer("А теперь Ваш мобильный телефон: ")

@dp.message_handler(state=HRQuestions.Q4)
async def answer_q5(message: types.Message, state: FSMContext):
    # Save answer to state
    await state.update_data(q5_answer=message.text)

    # Create keyboard markup for second question
    q5_choices = ReplyKeyboardMarkup(resize_keyboard=True)
    q5_choices.add(KeyboardButton('WhatsApp'), KeyboardButton('Telegram'), KeyboardButton('Обратный звонок от HR'))

    # Set state to Q2
    await HRQuestions.Q5.set()

    await message.answer("Предпочитаемый способ связи: ", reply_markup=q5_choices)

#Third question handler
@dp.message_handler(state=HRQuestions.Q5)
async def answer_q6(message: types.Message, state: FSMContext):
    # Save answer to state
    await state.update_data(q6_answer=message.text)

    # Get all answers from state
    data = await state.get_data()
    # q1_answer = data.get('q1_answer')
    q2_answer = data.get('q2_answer')
    q3_answer = data.get('q3_answer')
    q4_answer = data.get('q4_answer')
    q5_answer = data.get('q5_answer')
    q6_answer = data.get('q6_answer')
    # Format all answers as text
    answers_text = f"1. Имя: {q2_answer}\n2. Можно?: {q3_answer}\n3. Возраст: {q4_answer}\n4. Телефон: {q5_answer}\n5. Связь: {q6_answer}"

    # Send answers to user
    await message.answer(f"Thank you for answering the questions!\n\n{answers_text}")

    # End conversation
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
