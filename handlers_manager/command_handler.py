from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ads_manager.ads_manager import format_ad, load_ads
from buttons_manager.buttons_manager import ad_inline_kb, main_menu_kb
from aiogram.filters import CommandStart

from states import AddAdStates

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = "Привет! Я бот-объявления.\n\n" "Что будем делать?"
    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Инструкция:\n"
        "• /add — создать новое объявление (текст, фото, аудио/голос)\n"
        "• /list — показать все объявления\n"
        "• Напишите текст — я предложу сохранить его как объявление\n"
        "• Отправьте фото — спрошу про описание\n"
        "• Отправьте аудио или голос — сохраню как аудио-объявление\n"
        "• У объявлений есть кнопки: ❤️ Нравится и 🗑 Удалить (для автора)\n"
        "• Каждый пользователь может лайкнуть объявление только 1 раз\n"
        "• Автор получает уведомление о лайках его объявлений"
    )
    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddAdStates.waiting_for_content)
    await message.answer(
        "Отправьте текст, фото, аудио или голос для объявления.\n"
        "Для фото будет предложено добавить описание.",
        reply_markup=main_menu_kb(),
    )


@router.message(Command("list"))
async def cmd_list(message: Message):
    ads = load_ads()
    if not ads:
        await message.answer("Пока нет объявлений.",
                             reply_markup=main_menu_kb())
        return
    if message.from_user is None:
        # Нечего обрабатывать — безопасно выйти или логировать
        return

    # Показываем по одному (простая версия)
    for ad in ads:
        is_author = ad["user_id"] == message.from_user.id
        kb = ad_inline_kb(ad["id"], is_author)
        if ad["type"] == "text":
            await message.answer(format_ad(ad), reply_markup=kb)
        elif ad["type"] == "photo":
            await message.answer_photo(
                ad["file_id"],
                caption=(ad.get("caption") or "") + f"\n\n{format_ad(ad)}",
                reply_markup=kb,
            )
        elif ad["type"] == "audio":
            await message.answer_audio(
                ad["file_id"],
                caption=(ad.get("caption") or "") + f"\n\n{format_ad(ad)}",
                reply_markup=kb,
            )
        elif ad["type"] == "voice":
            await message.answer_voice(
                ad["file_id"],
                caption=(ad.get("caption") or "") + f"\n\n{format_ad(ad)}",
                reply_markup=kb,
            )
