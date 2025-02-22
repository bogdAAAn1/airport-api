from django.conf import settings
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        related_name="airplane",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.closest_big_city}"


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

    def __str__(self):
        return (f"Source: {self.source.name}, "
                f"Destination: {self.destination.name}")


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
