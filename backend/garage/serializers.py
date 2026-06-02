from rest_framework import serializers

from .models import Car, FuelFillUp, SparePartOrder


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "vin", "make", "model", "created_at"]
        read_only_fields = ["id", "created_at"]


class FuelFillUpSerializer(serializers.ModelSerializer):
    car_vin = serializers.CharField(source="car.vin", read_only=True)

    class Meta:
        model = FuelFillUp
        fields = [
            "id",
            "car",
            "car_vin",
            "date",
            "odometer_km",
            "liters",
            "total_cost",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "car_vin"]

    def validate_car(self, car: Car) -> Car:
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            if car.owner_id != request.user.id:
                raise serializers.ValidationError("Car does not belong to current user.")
        return car


class SparePartOrderSerializer(serializers.ModelSerializer):
    car_vin = serializers.CharField(source="car.vin", read_only=True)

    class Meta:
        model = SparePartOrder
        fields = [
            "id",
            "car",
            "car_vin",
            "part_name",
            "part_number",
            "quantity",
            "status",
            "vendor",
            "price",
            "ordered_at",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "car_vin"]

    def validate_car(self, car: Car) -> Car:
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            if car.owner_id != request.user.id:
                raise serializers.ValidationError("Car does not belong to current user.")
        return car
