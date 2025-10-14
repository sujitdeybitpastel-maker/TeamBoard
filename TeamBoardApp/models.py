from django.db import models
from django.utils import timezone

class Employees(models.Model):
    id = models.BigAutoField(primary_key=True)  # bigserial, auto-increment
    first_name = models.TextField(null=False, blank=False)  # mandatory
    last_name = models.TextField(null=True, blank=True)     # optional
    user_name = models.TextField(null=True, blank=True)     # optional
    email = models.CharField(max_length=255, unique=True, null=False, blank=False)  # mandatory + unique
    password = models.TextField(null=False, blank=False)   # mandatory, store hashed
    phone_number = models.TextField(null=False, blank=False)  # mandatory
    address = models.TextField(null=False, blank=False)    # mandatory
    profile_image_url = models.TextField(null=True, blank=True)  # optional
    system_creation_time = models.DateTimeField(default=timezone.now, null=False, blank=False)  # mandatory
    system_update_time = models.DateTimeField(null=True, blank=True)  # optional
    status = models.CharField(null=False,blank=False)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} ({self.get_status_display()})"



