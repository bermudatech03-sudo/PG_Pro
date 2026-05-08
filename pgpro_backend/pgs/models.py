from django.db import models
from accounts.models import User
import uuid

class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    receptionist = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_property')
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    amenities = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    RENT_TYPE = [('per_room', 'Per Room'), ('per_bed', 'Per Bed')]
    STATUS = [('available', 'Available'), ('partially_occupied', 'Partially Occupied'),
              ('fully_occupied', 'Fully Occupied'), ('maintenance', 'Maintenance')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=[
        ('single', 'Single'), ('double', 'Double'),
        ('triple', 'Triple'), ('dormitory', 'Dormitory')
    ])
    rent_type = models.CharField(max_length=20, choices=RENT_TYPE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.name} - Room {self.room_number}"

class Bed(models.Model):
    STATUS = [('available', 'Available'), ('occupied', 'Occupied'),
              ('reserved', 'Reserved'), ('maintenance', 'Maintenance')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_label = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.bed_label}"