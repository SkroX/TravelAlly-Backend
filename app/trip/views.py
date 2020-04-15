from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from . import serializers
from core.models import Trip

# Create your views here.


class TripViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Trip.objects.all()
    serializer_class = serializers.TripSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user, votes=0)
