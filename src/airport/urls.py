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
    CityViewSet
)

router = DefaultRouter()
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("flight", FlightViewSet)
router.register("crew", CrewViewSet)
router.register("country", CountryViewSet)
router.register("city", CityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
