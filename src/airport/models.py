from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country,
        related_name="city",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("name", "country"),
                name="unique_city_country"
            )
        ]

    def __str__(self):
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        related_name="airplane",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("name", "rows", "seats_in_row", "airplane_type"),
                name="unique_airplane"
            )
        ]

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    closest_big_city = models.ForeignKey(
        City,
        related_name="airport",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("name", "closest_big_city"),
                name="unique_airport"
            )
        ]

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        related_name="departure_route",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport,
        related_name="arrival_route",
        on_delete=models.CASCADE
    )
    distance = models.PositiveIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("source", "destination"),
                name="unique_route_source_destination"
            )
        ]

    def clean(self):
        if self.source == self.destination:
            raise ValidationError(
                "Source and destination cannot be the same."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Source - {self.source.name}, "
            f"Destination - {self.destination.name}"
        )


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        related_name="flight",
        on_delete=models.CASCADE
    )
    airplane = models.ForeignKey(
        Airplane,
        related_name="flight",
        on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=(
                    "route", "airplane", "departure_time", "arrival_time"
                ),
                name="unique_flight"
            )
        ]

    def __str__(self):
        departure = self.departure_time.strftime("%Y-%m-%d %H:%M")
        arrival = self.arrival_time.strftime("%Y-%m-%d %H:%M")
        return (
            f"Flight {self.airplane} | {self.route.source.name} "
            f"→ {self.route.destination.name} "
            f"| Departure: {departure} | Arrival: {arrival}"
        )

class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    flights = models.ManyToManyField(Flight, related_name="crew")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="order",
        on_delete=models.CASCADE
    )


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight,
        related_name="ticket",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        related_name="ticket",
        on_delete=models.CASCADE
    )
