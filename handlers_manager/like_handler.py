import aiogram
from ads_manager.ads_manager import load_ads, save_ads

from aiogram import F
from aiogram.types import (
    CallbackQuery,
)

router = aiogram.Router()


@router.callback_query(F.data.startswith("like:"))
async def like_ad(cb: CallbackQuery):
    if cb.data is None:
        return
    try:
        ad_id = int(cb.data.split(":")[1])
    except Exception:
        await cb.answer("Ошибка.")
        return

    ads = load_ads()
    for ad in ads:
        if ad.get("id") == ad_id:
            liked_by = ad.get("liked_by", [])
            if cb.from_user.id in liked_by:
                await cb.answer("Вы уже лайкали это объявление.")
                return
            liked_by.append(cb.from_user.id)
            ad["liked_by"] = liked_by
            ad["likes"] = len(liked_by)
            save_ads(ads)

            # Уведомление автору
            author_id = ad["user_id"]
            if cb.bot is None:
                return
            if author_id != cb.from_user.id:
                try:
                    await cb.bot.send_message(
                        author_id,
                        f"Ваше объявление ID {ad_id} получило новый лайк! "
                        f"Всего лайков: {ad['likes']}",
                    )
                except Exception:
                    pass

            await cb.answer("Лайк засчитан ❤️")
            # Обновлять сообщение с кнопками необязательно; можно оставить
            return

    await cb.answer("Объявление не найдено.")
