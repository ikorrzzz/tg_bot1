from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ads_manager.ads_manager import Ad, load_ads, next_ad_id, save_ads
from aiogram import F

from states import AddAdStates


router = Router()


@router.message(AddAdStates.waiting_for_content, F.audio)
async def handle_audio_for_ad(message: Message, state: FSMContext):
    if message.from_user is None or message.audio is None:
        # Нечего обрабатывать — безопасно выйти или логировать
        return

    ads = load_ads()
    ad: Ad = {
        "id": next_ad_id(ads),
        "user_id": message.from_user.id,
        "type": "audio",
        "file_id": message.audio.file_id,
        "caption": message.caption if message.caption else None,
        "likes": 0,
        "liked_by": [],
        "created_at": datetime.utcnow().isoformat(),
        "extra": {},
    }
    ads.append(ad)
    save_ads(ads)
    await message.answer("🎶 Аудио-объявление добавлено")
    await state.clear()


# Обработка голосовых
@router.message(AddAdStates.waiting_for_content, F.voice)
async def handle_voice_for_ad(message: Message, state: FSMContext):
    if (message.from_user is None) or (message.voice is None):
        # Нечего обрабатывать — безопасно выйти или логировать
        return

    ads = load_ads()
    ad: Ad = {
        "id": next_ad_id(ads),
        "user_id": message.from_user.id,
        "type": "voice",
        "file_id": message.voice.file_id,
        "caption": None,
        "likes": 0,
        "liked_by": [],
        "created_at": datetime.utcnow().isoformat(),
        "extra": {},
    }
    ads.append(ad)
    save_ads(ads)
    await message.answer("🎶 Аудио-объявление добавлено")
    await state.clear()


@router.message(F.audio)
async def audio_outside_state(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is None:
        await state.set_state(AddAdStates.waiting_for_content)
        await handle_audio_for_ad(message, state)
