import strawberry
import strawberry_django
from strawberry.types import Info

from garage.models import Car, FuelFillUp

from .models import MaintenancePlan, MaintenanceRecord


@strawberry_django.type(Car)
class CarType:
    id: strawberry.auto
    vin: strawberry.auto
    make: strawberry.auto
    model: strawberry.auto


@strawberry_django.type(MaintenanceRecord)
class MaintenanceRecordType:
    id: strawberry.auto
    service_type: strawberry.auto
    date: strawberry.auto
    odometer_km: strawberry.auto
    cost: strawberry.auto
    notes: strawberry.auto


@strawberry.type
class MaintenancePlanStatus:
    service_type: str
    interval_km: int
    last_done_km: int
    next_due_km: int
    current_km: int | None
    remaining_km: int | None
    due_soon: bool
    overdue: bool


@strawberry.type
class MaintenanceHistory:
    car: CarType
    current_km: int | None
    records: list[MaintenanceRecordType]
    plans: list[MaintenancePlanStatus]


def _get_current_km(car: Car) -> int | None:
    last = (
        FuelFillUp.objects.filter(car=car)
        .order_by("-odometer_km", "-date", "-id")
        .only("odometer_km")
        .first()
    )
    return int(last.odometer_km) if last else None


@strawberry.type
class Query:
    @strawberry.field
    def maintenance_history(self, info: Info, vin: str, due_soon_threshold_km: int = 500) -> MaintenanceHistory:
        user = getattr(getattr(info, "context", None), "request", None)
        user = getattr(user, "user", None)
        if not user or not user.is_authenticated:
            raise PermissionError("Authentication required.")

        car = Car.objects.get(vin=vin, owner=user)
        current_km = _get_current_km(car)

        records = MaintenanceRecord.objects.filter(car=car).order_by("-odometer_km", "-date", "-id")
        plans_qs = MaintenancePlan.objects.filter(car=car).order_by("service_type")

        plans: list[MaintenancePlanStatus] = []
        for p in plans_qs:
            next_due = p.next_due_km
            remaining = None
            due_soon = False
            overdue = False
            if current_km is not None:
                remaining = next_due - current_km
                overdue = remaining <= 0
                due_soon = (not overdue) and remaining <= due_soon_threshold_km

            plans.append(
                MaintenancePlanStatus(
                    service_type=p.service_type,
                    interval_km=int(p.interval_km),
                    last_done_km=int(p.last_done_km),
                    next_due_km=int(next_due),
                    current_km=current_km,
                    remaining_km=remaining,
                    due_soon=due_soon,
                    overdue=overdue,
                )
            )

        return MaintenanceHistory(
            car=car,
            current_km=current_km,
            records=list(records),
            plans=plans,
        )

