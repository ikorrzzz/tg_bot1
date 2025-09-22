from aiogram import Router
from ads_manager.ads_manager import load_ads, save_ads
from aiogram import F
from aiogram.types import (
    CallbackQuery,
)

router = Router()


@router.callback_query(F.data.startswith("del:"))
async def delete_ad(cb: CallbackQuery):
    if cb.data is None:
        return
    try:
        ad_id = int(cb.data.split(":")[1])
    except Exception:
        await cb.answer("Ошибка.")
        return

    ads = load_ads()
    for idx, ad in enumerate(ads):
        if ad.get("id") == ad_id:
            if ad["user_id"] != cb.from_user.id:
                await cb.answer("Удаление доступно только автору.",
                                show_alert=True)
                return
            ads.pop(idx)
            save_ads(ads)
            msg = cb.message
            if msg and hasattr(msg, "edit_text"):
                await msg.edit_text("Объявление удалено.")
            else:
                await cb.answer("Объявление удалено.", show_alert=True)
            await cb.answer("Удалено")
            return

    await cb.answer("Объявление не найдено.")
