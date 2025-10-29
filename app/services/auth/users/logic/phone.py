from __future__ import annotations

from dataclasses import dataclass

from django.core.exceptions import ValidationError

PHONE_VALIDATION_ERROR = "Invalid phone"


@dataclass(frozen=True, slots=True)
class NormalizedPhone:
    number: str
    extension: str | None = None


def normalize_phone_number(raw_phone: str | None) -> NormalizedPhone:
    """Normalize Russian phone numbers to E.164 (+7XXXXXXXXXX).

    Accepts inputs like +7XXXXXXXXXX, 8XXXXXXXXXX, 7XXXXXXXXXX, or 10-digit numbers.
    """
    if raw_phone is None:
        raise ValidationError(PHONE_VALIDATION_ERROR)

    s = "".join(ch for ch in raw_phone if ch.isdigit())
    if not s:
        raise ValidationError(PHONE_VALIDATION_ERROR)

    # если начинается с 8 или 7 и имеет длину 11 -> местная часть последние 10 цифр
    if len(s) == 11 and s[0] in ("7", "8"):
        local = s[1:]
    elif len(s) == 10:
        local = s
    else:
        # уже с кодом страны, но неожиданной длиной
        raise ValidationError(PHONE_VALIDATION_ERROR)

    # проверить местную часть (10 цифр)
    if not (local.isdigit() and len(local) == 10):
        raise ValidationError(PHONE_VALIDATION_ERROR)

    # запретить все нулевые или явно недействительные местные номера
    if set(local) == {"0"}:
        raise ValidationError(PHONE_VALIDATION_ERROR)

    e164 = "+7" + local
    return NormalizedPhone(number=e164, extension=None)
