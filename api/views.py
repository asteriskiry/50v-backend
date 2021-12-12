from rest_framework import generics
from django.utils.timezone import now
from rest_framework.response import Response
from django.conf import settings

from api import utils

from .models import Participant
from .serializers import ParticipantSerializer


class ParticipantView(generics.ListCreateAPIView):
    queryset = Participant.objects.all_main_participants()
    serializer_class = ParticipantSerializer
    permission_classes = []

    def list(self, _):
        response = {
            "main_start_date": settings.ILMO_START_DATE,
            "main_end_date": settings.ILMO_END_DATE,
            "reserve_start_date": settings.RESERVE_START_DATE,
            "reserve_end_date": settings.RESERVE_END_DATE,
            "registration_status": utils.registration_status().name,
            "all_count": Participant.objects.count(),
            "main_count": Participant.objects.count_main_participants(),
            "reserve_count": Participant.objects.count_reserve_participants(),
        }
        main_queryset = self.get_queryset()
        reserve_queryset = Participant.objects.all_reserve_participants()
        response["main_participants"] = ParticipantSerializer(main_queryset, many=True).data
        response["reserve_participants"] = ParticipantSerializer(reserve_queryset, many=True).data
        return Response(response)

