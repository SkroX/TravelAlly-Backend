from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from . import serializers
from core.models import Trip, UserModel, TripRequest

# Create your views here.


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = serializers.TripSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user, votes=None)


class VotesView(APIView):

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


class RequestTripView(APIView):
    def get_object(self, pk):
        if Trip.objects.filter(pk=pk).exists():
            return Trip.objects.get(pk=pk)
        else:
            return None

    def get(self, request, pk):
        trip = self.get_object(pk)
        if trip:
            if self.request.user == trip.organizer:
                if TripRequest.objects.filter(trip=trip).exists():
                    tripRequest = TripRequest.objects.get(trip=trip)
                    ser = serializers.TripRequestSerializer(tripRequest)
                    print(TripRequest.requesters)
                    return Response(ser.data, status=status.HTTP_200_OK)
                else:
                    return Response({})
            else:
                return Response({'msg': 'not your trip'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'msg': 'trip does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        trip = self.get_object(pk)
        if trip:
            if self.request.user != trip.organizer:
                tripRequest = None
                if TripRequest.objects.filter(trip=trip).exists():
                    tripRequest = TripRequest.objects.get(trip=trip)
                    tripRequest.requesters.add(self.request.user)
                else:
                    tripRequest = TripRequest(trip=trip)
                    tripRequest.save()
                    tripRequest.requesters.add(self.request.user)
                ser = serializers.TripRequestSerializer(tripRequest)

                return Response(ser.data, status=status.HTTP_200_OK)

            else:
                return Response({'msg': 'can not request in own trip'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'no such trip'}, status=status.HTTP_400_BAD_REQUEST)
