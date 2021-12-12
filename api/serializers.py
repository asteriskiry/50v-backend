from rest_framework import serializers
from django.conf import settings

from .models import Participant
from api import utils


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
            "is_in_reserve",
            "party_representing",
            "is_consenting",
        ]

    def validate(self, data):
        if not utils.is_main_registration() and not utils.is_reserve_registration():
            raise serializers.ValidationError("Ilmoittautuminen ei ole auki")

        if self.is_registration_full():
            raise serializers.ValidationError("Ilmoittautuminen on täynnä")

        return data

    def create(self, validated_data):
        if utils.is_main_registration():
            validated_data["is_in_reserve"] = False
        else:
            validated_data["is_in_reserve"] = True
        return Participant.objects.create(**validated_data)

    def to_representation(self, instance):
        get_fields = ["first_name", "last_name"]
        ret = super().to_representation(instance)
        return {k: v for k, v in ret.items() if k in get_fields}

    def is_registration_full(self):
        if utils.is_main_registration():
            return Participant.objects.is_main_full()
        return Participant.objects.is_reserve_full()
