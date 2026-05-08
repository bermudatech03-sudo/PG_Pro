from django.db import models
from pgs.models import Property, Room, Bed
import uuid

class Tenant(models.Model):
    STATUS = [('active', 'Active'), ('notice_period', 'Notice Period'), ('vacated', 'Vacated')]
    ID_PROOF = [('aadhaar', 'Aadhaar'), ('passport', 'Passport'),
                ('voter_id', 'Voter ID'), ('driving_license', 'Driving License')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='tenants')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tenants')
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenant')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=15)
    id_proof_type = models.CharField(max_length=30, choices=ID_PROOF)
    id_proof_number = models.CharField(max_length=50)
    id_proof_url = models.URLField(blank=True, null=True)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rent_due_day = models.IntegerField(default=1)
    joining_date = models.DateField()
    expected_leaving_date = models.DateField(null=True, blank=True)
    actual_leaving_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    police_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.property.name}"