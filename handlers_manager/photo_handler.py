from ads_manager.ads_manager import Ad, load_ads, next_ad_id, save_ads
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from buttons_manager.buttons_manager import photo_caption_choice_kb
from states import AddAdStates

router = Router()


@router.message(AddAdStates.waiting_for_content, F.photo)
async def handle_photo_for_ad(message: Message, state: FSMContext):
    if message.photo is None:
        return
    # Берём фото наибольшего размера
    photo = message.photo[-1]
    await state.update_data(pending_photo_id=photo.file_id)
    await message.answer(
        "Добавить описание к фото?", reply_markup=photo_caption_choice_kb()
    )


@router.callback_query(F.data == "photo_add_caption")
async def photo_add_caption(cb: CallbackQuery, state: FSMContext):
    if cb.message is None:
        return
    await cb.message.answer("Напишите описание для фото:")
    await state.set_state(AddAdStates.waiting_for_photo_caption)
    await cb.answer()


@router.message(AddAdStates.waiting_for_photo_caption, F.text)
async def photo_caption_entered(message: Message, state: FSMContext):
    if message.from_user is None:
        return
    data = await state.get_data()
    file_id = data.get("pending_photo_id")
    if not file_id:
        await message.answer("Не найдено фото. Начните заново: /add")
        await state.clear()
        return

    caption = message.text or None

    ads = load_ads()
    ad: Ad = {
        "id": next_ad_id(ads),
        "user_id": message.from_user.id,
        "type": "photo",
        "file_id": file_id,
        "caption": caption,
        "likes": 0,
        "liked_by": [],
        "created_at": datetime.utcnow().isoformat(),
        "extra": {},
    }
    ads.append(ad)
    save_ads(ads)

    await message.answer_photo(
        photo=file_id,
        caption=caption
    )

    await message.answer("Фото-объявление сохранено!")
    await state.clear()


@router.callback_query(F.data == "photo_no_caption")
async def photo_no_caption(cb: CallbackQuery, state: FSMContext):
    if cb.message is None:
        return
    data = await state.get_data()
    file_id = data.get("pending_photo_id")
    if not file_id:
        await cb.message.answer("Не найдено фото. Начните заново: /add")
        await state.clear()
        await cb.answer()
        return

    ads = load_ads()
    ad: Ad = {
        "id": next_ad_id(ads),
        "user_id": cb.from_user.id,
        "type": "photo",
        "file_id": file_id,
        "caption": None,
        "likes": 0,
        "liked_by": [],
        "created_at": datetime.utcnow().isoformat(),
        "extra": {},
    }
    ads.append(ad)
    save_ads(ads)

    # Отправим превью без подписи
    await cb.message.answer_photo(photo=file_id)

    await cb.message.answer("Фото-объявление сохранено!")
    await state.clear()
    await cb.answer()


@router.message(F.photo)
async def photo_outside_state(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is None:
        await state.set_state(AddAdStates.waiting_for_content)
        await handle_photo_for_ad(message, state)
