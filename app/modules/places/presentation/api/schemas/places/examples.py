from datetime import time

from app.core.enums import LanguageEnum
from app.modules.places.shared.enums import PlacePhoneTypeEnum

DISPLAY_ADDRESS_EXAMPLE = "Saint-Petersburg, 2 Murinskiy Prospekt, 3"
TAXI_ADDRESS_EXAMPLE = "Россия, Санкт-Петербург, 2-й Муринский проспект, 3"
TAXI_COMMENT_EXAMPLE = "Подъезд сразу узнаете, там короче табличка массажки"
UUID_EXAMPLE = "123e4567-e89b-12d3-a456-426614174000"
NAME_EXAMPLE = "What they don't talk about in polite society"
ICON_KEY_EXAMPLE = "unknown"
MARKER_COLOR_EXAMPLE = "#F59E0B"
LATITUDE_EXAMPLE = 60.002598
LONGITUDE_EXAMPLE = 30.330861
TITLE_EXAMPLE = 'Massage parlor "У Димасика"'
DESCRIPTION_EXAMPLE = "A cozy massage parlor located in the Vyborgsky district of St. Petersburg, offering a variety of massage services to help you relax and rejuvenate. Our experienced therapists use high-quality oils and techniques to provide a personalized massage experience tailored to your needs. Whether you're looking for a deep tissue massage, a relaxing Swedish massage, or a therapeutic sports massage, we have the perfect treatment for you. Visit us today and let us help you unwind and feel your best!"
SHORT_DESCRIPTION_EXAMPLE = "A cozy massage parlor located in the Vyborgsky district of St. Petersburg, offering a variety of massage services to help you relax and rejuvenate."
TIMEZONE_EXAMPLE = "Europe/Moscow"
START_TIME_EXAMPLE = time(20, 24, 0)
END_TIME_EXAMPLE = time(22, 24, 53)
WORKING_HOURS_INTERVAL_EXAMPLE = {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE}
NUMBER_EXAMPLE = "+79999991984"
PHONE_TYPE_EXAMPLE = PlacePhoneTypeEnum.MOBILE
PHOTO_URL_EXAMPLE = "https://example.com/photo.jpg"
PHOTO_THUMBNAIL_URL_EXAMPLE = "https://example.com/photo_thumbnail.jpg"
AVERAGE_EXAMPLE = 5.0
REVIEWS_COUNT_EXAMPLE = 1984
LANGUAGE_CODE_EXAMPLE = LanguageEnum.RU
