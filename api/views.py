from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from api import utils

from .models import Participant
from .serializers import ParticipantSerializer


class ParticipantView(generics.ListCreateAPIView):
    queryset = Participant.objects.all_fitting_participants()
    serializer_class = ParticipantSerializer
    permission_classes = []

    def post(self, request):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, _):
        reg_status = utils.registration_status()
        response = {
            "invited_start_date": settings.INVITED_START_DATE,
            "invited_end_date": settings.INVITED_END_DATE,
            "main_start_date": settings.ILMO_START_DATE,
            "main_end_date": settings.ILMO_END_DATE,
            "registration_status": reg_status.name,
            "all_count": Participant.objects.count(),
            "invited_count": Participant.objects.count_invited_participants(),
            "main_count": Participant.objects.count_main_participants(),
            "fitting_count": Participant.objects.count_fitting_participants(),
            "reserve_count": Participant.objects.count_reserve_participants(),
            "fitting_participants": [],
            "reserve_participants": [],
        }
        if reg_status in (
            utils.RegistrationStatus.MAIN_IN_PROGRESS,
            utils.RegistrationStatus.RESERVE_IN_PROGRESS,
            utils.RegistrationStatus.ENDED,
        ):
            main_queryset = self.get_queryset()
            reserve_queryset = Participant.objects.all_reserve_participants()
            response["fitting_participants"] = ParticipantSerializer(
                main_queryset, many=True
            ).data
            response["reserve_participants"] = ParticipantSerializer(
                reserve_queryset, many=True
            ).data
        return Response(response)
