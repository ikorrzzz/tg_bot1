from typing import Optional, TypedDict, List
import os
import json

ADS_FILE = os.getenv("ADS_FILE", "ads.json")


class Ad(TypedDict, total=False):
    id: int
    user_id: int
    type: str
    file_id: str
    caption: Optional[str]
    content: Optional[str]
    likes: int
    liked_by: List[int]
    created_at: str
    extra: dict


def load_ads() -> List[Ad]:
    if not os.path.exists(ADS_FILE):
        return []
    try:
        with open(ADS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def save_ads(ads: List[Ad]):
    with open(ADS_FILE, "w", encoding="utf-8") as f:
        json.dump(ads, f, ensure_ascii=False, indent=2)


def next_ad_id(ads: List[Ad]) -> int:
    if not ads:
        return 1
    return max(ad.get("id", 0) for ad in ads) + 1


def format_ad(ad: Ad) -> str:
    parts = []
    parts.append(f"ID: {ad['id']}")
    parts.append(f"Тип: {ad['type']}")
    if ad["type"] == "text":
        parts.append(f"Текст: {ad.get('content','')}")
    elif ad["type"] == "photo":
        parts.append("Фото: file_id сохранён")
        if ad.get("caption"):
            parts.append(f"Описание: {ad['caption']}")
    elif ad["type"] in ("audio", "voice"):
        parts.append("Аудио: file_id сохранён")
        if ad.get("caption"):
            parts.append(f"Описание: {ad['caption']}")
    parts.append(f"Лайков: {ad.get('likes', 0)}")
    return "\n".join(parts)
