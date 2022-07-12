from django.conf import settings
from django.db import models


class ParticipantManager(models.Manager):
    def all_invited_participants(self):
        return (
            super().get_queryset().filter(is_invited=True).filter(is_in_reserve=False)
        )

    def all_main_participants(self):
        return (
            super().get_queryset().filter(is_invited=False).filter(is_in_reserve=False)
        )

    def all_fitting_participants(self):
        return super().get_queryset().filter(is_in_reserve=False)

    def all_reserve_participants(self):
        return super().get_queryset().filter(is_in_reserve=True)

    def count_invited_participants(self) -> int:
        return self.all_invited_participants().count()

    def count_main_participants(self) -> int:
        return self.all_main_participants().count()

    def count_fitting_participants(self) -> int:
        return self.all_fitting_participants().count()

    def count_reserve_participants(self) -> int:
        return self.all_reserve_participants().count()

    def is_full(self) -> bool:
        return self.count_fitting_participants() >= settings.MAX_PARTICIPANTS


class Participant(models.Model):
    class Meta:
        verbose_name = "Ilmoittautuja"
        verbose_name_plural = "Ilmoittautuneet"

    class Menu(models.TextChoices):
        KASVIS = "VG", "Kasvis"
        LIHA = "LI", "Liha"
        KALA = "KA", "Kala"

    ctime = models.DateTimeField(
        auto_now_add=True, verbose_name="Ilmoittautuminen tehty"
    )
    mtime = models.DateTimeField(
        auto_now=True, verbose_name="Ilmoittautumista muokattu"
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name="Etunimi",
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name="Sukunimi",
    )

    starting_year = models.IntegerField(
        null=True,
        verbose_name="Opintojen aloitusvuosi",
    )

    email = models.CharField(
        max_length=255,
        verbose_name="Email",
    )

    is_asteriski_member = models.BooleanField(
        verbose_name="Asteriskin jäsen",
    )

    is_alcohol_free = models.BooleanField(
        verbose_name="Alkoholiton",
    )

    menu = models.CharField(
        max_length=2,
        verbose_name="Menu",
        choices=Menu.choices,
        default=Menu.LIHA,
    )

    excretory_diets = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name="Eritysruokavaliot ja allergiat",
    )

    is_attending_sillis = models.BooleanField(
        verbose_name="Osallistuu silliasiaamiaiselle",
    )

    avecs_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Avecin nimi",
    )

    other_info = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name="Pöytäseuruetoiveet ja muut terveiset",
    )

    is_invited = models.BooleanField(
        default=False,
        verbose_name="Kutsuvieras",
    )
    is_in_reserve = models.BooleanField(
        default=False,
        verbose_name="Varasijalla",
    )
    show_name = models.BooleanField(
        default=True,
        verbose_name="Nimi saa näkyä listalla",
    )

    # Invited guests

    is_greeting = models.BooleanField(
        verbose_name="Esittää tervehdyksen",
        default=False,
    )

    party_representing = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Tervehdyksessä edustetut tahot",
    )

    is_consenting = models.BooleanField(
        verbose_name="Hyväksyy tietosuojaselosteen yms.",
    )

    objects = ParticipantManager()

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            f"{' (Varasijalla)' if self.is_in_reserve else ''})"
        )
