from django.conf import settings
from django.utils.timezone import now
from enum import Enum
from api.models import Participant


def is_main_registration() -> bool:
    return settings.ILMO_START_DATE <= now() <= settings.ILMO_END_DATE


def is_reserve_registration() -> bool:
    return settings.RESERVE_START_DATE <= now() <= settings.RESERVE_END_DATE


class RegistrationStatus(Enum):
    NOT_STARTED = 0
    MAIN_IN_PROGRESS = 1
    MAIN_FULL = 2
    MAIN_ENDED = 3
    RESERVE_IN_PROGRESS = 4
    RESERVE_FULL = 5
    RESERVE_ENDED = 6


def registration_status() -> RegistrationStatus:
    if now() <= settings.ILMO_START_DATE:
        return RegistrationStatus.NOT_STARTED

    if is_main_registration():
        if Participant.objects.is_main_full():
            return RegistrationStatus.MAIN_FULL
        return RegistrationStatus.MAIN_IN_PROGRESS

    if settings.ILMO_END_DATE <= now() <= settings.RESERVE_START_DATE:
        return RegistrationStatus.MAIN_ENDED

    if is_reserve_registration():
        if Participant.objects.is_reserve_full():
            return RegistrationStatus.RESERVE_FULL
        return RegistrationStatus.RESERVE_IN_PROGRESS

    if settings.RESERVE_END_DATE <= now():
        return RegistrationStatus.RESERVE_ENDED

    return RegistrationStatus.RESERVE_ENDED

