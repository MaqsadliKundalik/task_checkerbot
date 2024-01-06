from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot("BOT_TOKEN")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
class comment_state(StatesGroup):
    comment = State()

class change_admin_state(StatesGroup):
    get_id = State()

def change_admin(id):
    with open("admin.txt", "w") as file:
        file.write(str(id))
change_admin(5165396993)
def get_admin():
    with open("admin.txt", "r") as file:
        for i in file:
            return i


@dp.message_handler(CommandStart())
async def start_command_answer(message: Message):
    if str(message.from_user.id) != get_admin():
        bot.send_message()
        await message.answer(
            "Assalomu alaykum, topshiriqni matn shaklida yoki fayl shaklida yuborishingiz mumkin.\n\n❗ Qaysi topshiriqni yuborayotganingizni bildirishni hohlasangiz kod ichida comment ichida topshiriq raqamini yozib yuboring.")
    else:
        await message.answer("Assalomu alaykum admin!")

@dp.message_handler(Command("change"))
async def change_admin_state_answer(message: Message):
    if str(message.from_user.id) == get_admin():
        await change_admin_state.get_id.set()
        await message.answer("Yangi admin id raqamini yuboring.")
    else: await task_text_answer(message)

@dp.message_handler(state=change_admin_state.get_id)
async def change_admin_answer(message: Message, state: FSMContext):
    user = await bot.get_chat(message.text)
    if user:
        change_admin(message.text)
        await message.answer("Admin o'zgartirildi!")
        await state.finish()
    else: await message.answer("Bunday foydalanuvchi topilmadi.")
@dp.message_handler(content_types="text")
async def task_text_answer(message: Message):
    response = f"task@%&{message.chat.id}@%&{message.from_user.full_name}@%&"
    response2 = f"Comment@%&{message.chat.id}@%&{message.from_user.full_name}@%&"
    inline_keyboard_button_markup = InlineKeyboardMarkup(row_width=5)
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="1", callback_data=response + "1"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="2", callback_data=response + "2"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="3", callback_data=response + "3"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="4", callback_data=response + "4"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="5", callback_data=response + "5"))

    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="Izoh yozish", callback_data=response2))

    await bot.send_message(get_admin(), f"<b>TOPSHIRIQQA JAVOB:</b>\n\n<b>O'quvchi nomi:</b> {message.from_user.full_name}\n{message.from_user.get_mention('Profilga havola', as_html=True)}\n\n{message.html_text}\n\nO'quvchini baholang.", reply_markup=inline_keyboard_button_markup, parse_mode="HTML")
    await message.answer("Ustozga xabar yetkazildi. 24 soat ichida javob olasiz.")

@dp.message_handler(content_types="document")
async def task_text_answer(message: Message):
    response = f"task@%&{message.chat.id}@%&{message.from_user.full_name}@%&"
    response2 = f"Comment@%&{message.chat.id}@%&{message.from_user.full_name}@%&"
    inline_keyboard_button_markup = InlineKeyboardMarkup(row_width=5)
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="1", callback_data=response + "1"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="2", callback_data=response + "2"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="3", callback_data=response + "3"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="4", callback_data=response + "4"))
    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="5", callback_data=response + "5"))

    inline_keyboard_button_markup.insert(InlineKeyboardButton(text="Izoh yozish", callback_data=response2))

    await bot.send_document(get_admin(), document=message.document.file_id, caption=f"<b>TOPSHIRIQQA JAVOB:</b>\n\n<b>O'quvchi nomi:</b> {message.from_user.full_name}\n{message.from_user.get_mention('Profilga havola', as_html=True)}\n\nO'quvchini baholang.", reply_markup=inline_keyboard_button_markup, parse_mode="HTML")
    await message.answer("Ustozga xabar yetkazildi. 24 soat ichida javob olasiz.")

@dp.message_handler(state=comment_state.comment)
async def comment_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data.get('user_id'), f"{data.get('full_name')}ga ustozdan baho uchun izoh:\n\n{message.html_text}", parse_mode="HTML")
    await message.answer("Izoh yetkazildi!")
    await state.finish()

@dp.callback_query_handler(lambda cb: cb.data)
async def cb_data_answer(cb_data: CallbackQuery, state= FSMContext):
    if cb_data.data.startswith("task"):
        data = cb_data.data.split("@%&")
        await bot.send_message(data[1], f"{data[2]} Ustoz sizga {data[3]} baho qo'ydi.", parse_mode='HTML')
        await cb_data.answer(f"O'quvchiga bahongiz yetkazildi! Qaysi topshiriqga {data[3]} baho qo'ygaingizni fikr bildirish tugmasiga bosib, yozib yuborsangiz yaxshi bo'lardi.\n\nMen izoh yuborganingizni unutgan bo'lsam uzr so'rayman.", show_alert=True)
    elif cb_data.data.startswith("Comment"):
        data = cb_data.data.split("@%&")
        await comment_state.comment.set()
        await state.update_data(user_id=data[1], full_name=data[2])
        await bot.send_message(cb_data.message.chat.id, "Marhamat, izohingizni yozing.")

executor.start_polling(dp)