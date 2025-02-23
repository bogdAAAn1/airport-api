from django.db.models import F, Count
from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Crew,
    Country,
    City,
    Order
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    FlightSerializer,
    CrewSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    CountrySerializer,
    CitySerializer,
    CityListSerializer,
    AirportListSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    OrderSerializer,
    OrderListSerializer,
    FlightRetrieveSerializer
)


@extend_schema_view(
    list=extend_schema(tags=["Country"]),
    create=extend_schema(tags=["Country"])
)
class CountryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


@extend_schema_view(
    list=extend_schema(tags=["City"]),
    create=extend_schema(tags=["City"])
)
class CityViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CityListSerializer
        return self.serializer_class

@extend_schema_view(
    list=extend_schema(tags=["Airport"]),
    create=extend_schema(tags=["Airport"])
)
class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Airport.objects.select_related("closest_big_city__country")
    serializer_class = AirportSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirportListSerializer
        return self.serializer_class

@extend_schema_view(
    list=extend_schema(tags=["Route"]),
    retrieve=extend_schema(tags=["Route"]),
    create=extend_schema(tags=["Route"]),
    update=extend_schema(tags=["Route"]),
    partial_update=extend_schema(tags=["Route"]),
    destroy=extend_schema(tags=["Route"]),
)
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source__closest_big_city__country",
        "destination__closest_big_city__country"
    )
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        return self.serializer_class

@extend_schema_view(
    list=extend_schema(tags=["Airplane Type"]),
    create=extend_schema(tags=["Airplane Type"])
)
class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

@extend_schema_view(
    list=extend_schema(tags=["Airplane"]),
    create=extend_schema(tags=["Airplane"])
)
class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer
        return self.serializer_class

@extend_schema_view(
    list=extend_schema(tags=["Flight"]),
    retrieve=extend_schema(tags=["Flight"]),
    create=extend_schema(tags=["Flight"]),
    update=extend_schema(tags=["Flight"]),
    partial_update=extend_schema(tags=["Flight"]),
    destroy=extend_schema(tags=["Flight"]),
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "route__source__closest_big_city__country",
        "route__destination__closest_big_city__country",
        "airplane__airplane_type",
    ).prefetch_related("crew")
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.annotate(
                free_seats=
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("ticket")
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightRetrieveSerializer
        return self.serializer_class

@extend_schema_view(
    list=extend_schema(tags=["Crew"]),
    create=extend_schema(tags=["Crew"])
)
class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

@extend_schema_view(
    list=extend_schema(tags=["Order"]),
    create=extend_schema(tags=["Order"])
)
class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source__closest_big_city__country",
        "tickets__flight__route__destination__closest_big_city__country",
        "tickets__flight__crew",
        "tickets__flight__airplane__airplane_type"
    )
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
