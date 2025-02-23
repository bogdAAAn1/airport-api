from django.urls import path, include
from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
    CrewViewSet,
    CountryViewSet,
    CityViewSet,
    OrderViewSet
)

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)
router.register("crews", CrewViewSet)
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
