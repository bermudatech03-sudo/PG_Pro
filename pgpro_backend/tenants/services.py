from .models import Tenant
from pgs.models import Bed, Room
from rest_framework.exceptions import ValidationError

def assign_tenant(data):
    room = data['room']
    bed = None

    # If room is per_bed, validate bed
    if room.rent_type == 'per_bed':
        if not data.get('bed'):
            raise ValidationError("This room requires a bed selection.")
        
        bed = data['bed']
        
        if bed.status != 'available':
            raise ValidationError("This bed is already occupied.")
        
        # Check no active tenant on this bed already
        if Tenant.objects.filter(bed=bed, status='active').exists():
            raise ValidationError("This bed already has an active tenant.")

    # If room is per_room, validate room
    if room.rent_type == 'per_room':
        if Tenant.objects.filter(room=room, status='active').exists():
            raise ValidationError("This room already has an active tenant.")

    # Create tenant
    tenant = Tenant.objects.create(**data)

    # Update bed status
    if bed:
        bed.status = 'occupied'
        bed.save()

    # Update room status
    update_room_status(room)

    return tenant


def update_room_status(room):
    if room.rent_type == 'per_room':
        has_tenant = Tenant.objects.filter(room=room, status='active').exists()
        room.status = 'fully_occupied' if has_tenant else 'available'

    elif room.rent_type == 'per_bed':
        total_beds = room.beds.count()
        occupied_beds = room.beds.filter(status='occupied').count()

        if occupied_beds == 0:
            room.status = 'available'
        elif occupied_beds < total_beds:
            room.status = 'partially_occupied'
        else:
            room.status = 'fully_occupied'

    room.save()