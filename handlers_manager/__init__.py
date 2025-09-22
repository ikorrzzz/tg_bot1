from aiogram import Router
from .audio_handler import router as _audio_handler
from .text_handler import router as _text_router
from .delete_handler import router as _delete_handler
from .like_handler import router as _like_handler
from .photo_handler import router as _photo_handler
from .command_handler import router as _command_handler

router = Router()

router.include_routers(
    _command_handler,
    _photo_handler,
    _audio_handler,
    _text_router,
    _delete_handler,
    _like_handler,
)
