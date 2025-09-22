from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Создать объявление")
    kb.button(text="Список объявлений")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def ad_inline_kb(ad_id: int, is_author: bool) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="❤️ Нравится", callback_data=f"like:{ad_id}")
    if is_author:
        b.button(text="🗑 Удалить", callback_data=f"del:{ad_id}")
    b.adjust(2)
    return b.as_markup()


def save_cancel_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Сохранить", callback_data="save_text")
    b.button(text="❌ Отменить", callback_data="cancel_text")
    b.adjust(2)
    return b.as_markup()


def photo_caption_choice_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Добавить описание", callback_data="photo_add_caption")
    b.button(text="Без описания", callback_data="photo_no_caption")
    b.adjust(2)
    return b.as_markup()
