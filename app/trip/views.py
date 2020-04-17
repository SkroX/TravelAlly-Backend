from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from . import serializers
from core.models import Trip, UserModel

# Create your views here.


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = serializers.TripSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user, votes=None)


class VotesViewSet(APIView):

    def post(self, request):

        trip = Trip.objects.get(pk=request.data['trip_id'])
        user = UserModel.objects.get(pk=request.data['user_id'])

        if not trip or not user:
            return Response({'msg': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        if user in trip.voters.all():
            trip.voters.remove(user)
        else:
            trip.voters.add(user)

        fin = serializers.TripSerializer(trip)
        return Response({'trip': fin.data}, status=status.HTTP_200_OK)
