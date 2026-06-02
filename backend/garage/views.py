from rest_framework import viewsets

from .models import Car, FuelFillUp, SparePartOrder
from .serializers import CarSerializer, FuelFillUpSerializer, SparePartOrderSerializer


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FuelFillUpViewSet(viewsets.ModelViewSet):
    serializer_class = FuelFillUpSerializer

    def get_queryset(self):
        return (
            FuelFillUp.objects.select_related("car")
            .filter(car__owner=self.request.user)
            .order_by("-date", "-odometer_km", "-id")
        )


class SparePartOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SparePartOrderSerializer

    def get_queryset(self):
        return (
            SparePartOrder.objects.select_related("car")
            .filter(car__owner=self.request.user)
            .order_by("-created_at", "-id")
        )
