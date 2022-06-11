from enum import Enum

from django.conf import settings
from django.utils.timezone import now

from api.models import Participant


def is_invited_registration() -> bool:
    day_ok = settings.INVITED_START_DATE <= now() <= settings.INVITED_END_DATE
    return not Participant.objects.is_full() and day_ok


def is_main_registration() -> bool:
    day_ok = settings.ILMO_START_DATE <= now() <= settings.ILMO_END_DATE
    return not Participant.objects.is_full() and day_ok


def is_reserve_registration() -> bool:
    day_ok = settings.ILMO_START_DATE <= now() <= settings.ILMO_END_DATE
    return Participant.objects.is_full() and day_ok


class RegistrationStatus(Enum):
    NOT_STARTED = 0
    INVITED_IN_PROGRESS = 1
    INVITED_ENDED = 2
    MAIN_IN_PROGRESS = 3
    RESERVE_IN_PROGRESS = 4
    ENDED = 5


def registration_status() -> RegistrationStatus:
    if now() < settings.INVITED_START_DATE:
        return RegistrationStatus.NOT_STARTED

    if is_invited_registration():
        return RegistrationStatus.INVITED_IN_PROGRESS

    if settings.INVITED_END_DATE < now() < settings.ILMO_START_DATE:
        return RegistrationStatus.INVITED_ENDED

    if is_main_registration():
        return RegistrationStatus.MAIN_IN_PROGRESS

    if is_reserve_registration():
        return RegistrationStatus.RESERVE_IN_PROGRESS

    if now() > settings.ILMO_END_DATE:
        return RegistrationStatus.ENDED

    return RegistrationStatus.NOT_STARTED
