from rest_framework.routers import DefaultRouter

from .views import CarViewSet, FuelFillUpViewSet, SparePartOrderViewSet

router = DefaultRouter()
router.register(r"cars", CarViewSet, basename="car")
router.register(r"fuel-fillups", FuelFillUpViewSet, basename="fuel-fillup")
router.register(r"spare-part-orders", SparePartOrderViewSet, basename="spare-part-order")

urlpatterns = router.urls

