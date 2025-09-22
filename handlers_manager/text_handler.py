from ads_manager.ads_manager import load_ads, next_ad_id, save_ads, Ad

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from datetime import datetime

from buttons_manager.buttons_manager import save_cancel_kb
from aiogram import F
from aiogram.types import (
    CallbackQuery,
)
from handlers_manager.command_handler import cmd_add, cmd_list
from handlers_manager.photo_handler import photo_caption_entered
from states import AddAdStates

router = Router()


@router.message(F.text == "Создать объявление")
async def menu_create(message: Message, state: FSMContext):
    await cmd_add(message, state)


@router.message(F.text == "Список объявлений")
async def menu_list(message: Message):
    await cmd_list(message)


# Обработка текстов в состоянии добавления
@router.message(AddAdStates.waiting_for_content, F.text)
async def handle_text_for_ad(message: Message, state: FSMContext):
    await state.update_data(pending_text=message.text)
    await message.answer(
        f"Вы отправили текст:\n\n{message.text}\n\nСохранить как объявление?",
        reply_markup=save_cancel_kb()
    )


@router.callback_query(F.data == "save_text")
async def save_text_cb(cb: CallbackQuery, state: FSMContext):
    if cb.message is None:
        return
    data = await state.get_data()
    text = data.get("pending_text")
    if not text:
        await cb.message.answer("Нет текста для сохранения. Попробуйте /add")
        await state.clear()
        await cb.answer()
        return

    ads = load_ads()
    ad: Ad = {
        "id": next_ad_id(ads),
        "user_id": cb.from_user.id,
        "type": "text",
        "content": text,
        "likes": 0,
        "liked_by": [],
        "created_at": datetime.utcnow().isoformat(),
        "extra": {}
    }
    ads.append(ad)
    save_ads(ads)

    await cb.message.answer("Объявление сохранено!")
    await state.clear()
    await cb.answer("Сохранено")


@router.callback_query(F.data == "cancel_text")
async def cancel_text_cb(cb: CallbackQuery, state: FSMContext):
    if cb.message is None:
        return
    await state.clear()
    await cb.message.answer("Отменено.")
    await cb.answer("Отменено")


@router.message(F.text)
async def any_text(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is None:
        # предложить перейти к созданию
        await state.set_state(AddAdStates.waiting_for_content)
        await state.update_data(pending_text=message.text)
        await message.answer(
            f"Вы отправили текст:\n\n{message.text}\n\n"
            "Сохранить как объявление?",
            reply_markup=save_cancel_kb()
        )
    elif current == 'AddAdStates:waiting_for_photo_caption':
        await photo_caption_entered(message, state)
