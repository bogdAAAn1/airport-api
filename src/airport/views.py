from django.db.models import F, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
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
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
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

SCHEMA_TAGS = {
    "Country": ["Country"],
    "City": ["City"],
    "Airport": ["Airport"],
    "Route": ["Route"],
    "AirplaneType": ["Airplane Type"],
    "Airplane": ["Airplane"],
    "Flight": ["Flight"],
    "Crew": ["Crew"],
    "Order": ["Order"],
}


def schema_tags(model_name):
    return extend_schema_view(
        list=extend_schema(tags=SCHEMA_TAGS[model_name]),
        create=extend_schema(tags=SCHEMA_TAGS[model_name])
    )


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class BaseFilterViewSet(viewsets.GenericViewSet):
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ()
    search_fields = ()
    ordering_fields = ()


@schema_tags("Country")
class CountryViewSet(CreateListViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@schema_tags("City")
class CityViewSet(CreateListViewSet, BaseFilterViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_fields = search_fields = ("name", "country__name")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CityListSerializer
        return self.serializer_class


@schema_tags("Airport")
class AirportViewSet(CreateListViewSet, BaseFilterViewSet):
    queryset = Airport.objects.select_related("closest_big_city__country")
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_fields = ("name", "closest_big_city__name")

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
class RouteViewSet(viewsets.ModelViewSet, BaseFilterViewSet):
    queryset = Route.objects.select_related(
        "source__closest_big_city__country",
        "destination__closest_big_city__country"
    )
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_fields = search_fields = ("source__name", "destination__name")
    ordering_fields = ("source__name", "destination__name", "distance")

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        return self.serializer_class


@schema_tags("AirplaneType")
class AirplaneTypeViewSet(CreateListViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@schema_tags("Airplane")
class AirplaneViewSet(CreateListViewSet, BaseFilterViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_fields = ("name", "airplane_type")
    ordering_fields = ("airplane_type",)

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
class FlightViewSet(viewsets.ModelViewSet, BaseFilterViewSet):
    queryset = Flight.objects.select_related(
        "route__source__closest_big_city__country",
        "route__destination__closest_big_city__country",
        "airplane__airplane_type",
    ).prefetch_related("crew")
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_fields = search_fields = ordering_fields = (
        "route__source__name",
        "route__destination__name",
        "departure_time",
        "arrival_time"
    )

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


@schema_tags("Crew")
class CrewViewSet(CreateListViewSet, BaseFilterViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    search_fields = ("first_name", "last_name")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


@schema_tags("Order")
class OrderViewSet(CreateListViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source__closest_big_city__country",
        "tickets__flight__route__destination__closest_big_city__country",
        "tickets__flight__crew",
        "tickets__flight__airplane__airplane_type"
    )
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
