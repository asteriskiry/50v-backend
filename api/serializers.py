from django.conf import settings
from rest_framework import serializers

from api import utils

from .models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    starting_year = serializers.IntegerField(
        min_value=1950, max_value=2022, allow_null=False, required=False
    )
    email = serializers.EmailField()

    class Meta:
        model = Participant
        fields = [
            "first_name",
            "last_name",
            "starting_year",
            "email",
            "is_asteriski_member",
            "is_alcohol_free",
            "is_vege",
            "excretory_diets",
            "is_attending_sillis",
            "avecs_name",
            "other_info",
            "is_greeting",
            "party_representing",
            "is_consenting",
            "dont_show_name",
        ]

    def validate(self, data):
        if utils.registration_status() in (
            utils.RegistrationStatus.NOT_STARTED,
            utils.RegistrationStatus.INVITED_ENDED,
            utils.RegistrationStatus.ENDED,
        ):
            raise serializers.ValidationError("Ilmoittautuminen ei ole auki")

        return data

    def create(self, validated_data):
        if utils.registration_status() == utils.RegistrationStatus.INVITED_IN_PROGRESS:
            validated_data["is_invited"] = True

        if utils.registration_status() == utils.RegistrationStatus.RESERVE_IN_PROGRESS:
            validated_data["is_in_reserve"] = True

        return Participant.objects.create(**validated_data)

    def to_representation(self, instance):
        get_fields = ["first_name", "last_name"]
        ret = super().to_representation(instance)
        if ret["dont_show_name"]:
            ret["first_name"] = "***"
            ret["last_name"] = "***"
        data = {k: v for k, v in ret.items() if k in get_fields}
        return data
