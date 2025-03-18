from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.test import APIClient
from rest_framework import status
from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Crew,
    Order,
    Ticket
)
from airport.serializers import (
    AirportListSerializer,
)

User = get_user_model()


def sample_country(**params):
    defaults = {
        "name": f"Test Country {Country.objects.count() + 1}",
    }
    defaults.update(params)
    return Country.objects.create(**defaults)


def sample_city(**params):
    country = sample_country()
    defaults = {
        "name": f"Test City {City.objects.count() + 1}",
        "country": country
    }
    defaults.update(params)
    city, _ = City.objects.get_or_create(**defaults)
    return city


def sample_airport(**params):
    city = sample_city()
    defaults = {
        "name": f"Test Airport {Airport.objects.count() + 1}",
        "closest_big_city": city
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport()
    destination = sample_airport()
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 100
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "name": "Test Type"
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {
        "name": "Test Airplane",
        "airplane_type": airplane_type,
        "rows": 10,
        "seats_in_row": 6
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2023-10-01T10:00:00Z",
        "arrival_time": "2023-10-01T12:00:00Z"
    }
    defaults.update(params)
    flight = Flight.objects.create(**defaults)
    crew = Crew.objects.create(first_name="John", last_name="Doe")
    flight.crew.add(crew)
    return flight


def sample_order(**params):
    user = User.objects.create_user(
        email="test@example.com",
        password="testpass123"
    )
    flight = sample_flight()
    ticket = Ticket.objects.create(
        row=1,
        seat=1,
        flight=flight
    )
    defaults = {
        "user": user
    }
    defaults.update(params)
    order = Order.objects.create(**defaults)
    order.tickets.add(ticket)
    return order


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(reverse("airport:airport-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.pagination = PageNumberPagination()
        self.pagination.page_size = None

    def test_list_airports(self):
        sample_airport()
        sample_airport()

        res = self.client.get(reverse("airport:airport-list"))

        airports = Airport.objects.order_by("id")
        serializer = AirportListSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "New Airport",
            "closest_big_city": sample_city().id
        }
        res = self.client.post(reverse("airport:airport-list"), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        payload = {
            "name": "New Airport",
            "closest_big_city": sample_city().id
        }
        res = self.client.post(reverse("airport:airport-list"), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(id=res.data["id"])
        for key, value in payload.items():
            if key == "closest_big_city":
                self.assertEqual(value, airport.closest_big_city.id)
            else:
                self.assertEqual(value, getattr(airport, key))
