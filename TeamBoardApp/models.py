from django.db import models
from django.utils import timezone
from enumfields import Enum, EnumField
# This is the enum alter data format for enum values
"""CREATE TYPE statuses AS ENUM ('1','3','5');
ALTER TABLE employees
ALTER COLUMN status TYPE statuses USING status::text::statuses;"""

class Status(models.TextChoices):
    INACTIVE = "0", "Inactive"
    ACTIVE = "1", "Active"
    DELETED = "5", "Deleted"
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
    status = models.CharField(
        max_length=1,  # length should accommodate the ENUM labels
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} ({self.get_status_display()})"


class Status(models.IntegerChoices):
    INACTIVE = 0, "Inactive"
    ACTIVE = 1, "Active"
    DELETED = 5, "Deleted"
class Project(models.Model):

    status = models.IntegerField(
    choices=Status.choices,
    default=Status.ACTIVE,
    )
    
    id = models.BigAutoField(primary_key=True)  # bigserial
    title = models.TextField(null=False, blank=False)  # mandatory
    description = models.TextField(null=True, blank=True)  # optional
    banner_image_url = models.TextField(null=True, blank=True)  # optional
    system_creation_time = models.DateTimeField(
        auto_now_add=True, null=False, blank=False
    )  # default current timestamp
    system_update_time = models.DateTimeField(
        auto_now=False, null=True, blank=True
    )  # updated on save
    

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.title
    
class ProjectMembership(models.Model):

    status = models.IntegerField(
    choices=Status.choices,
    default=Status.ACTIVE,
    )

    id = models.BigAutoField(primary_key=True)  # bigserial
    project = models.ForeignKey(
        'Project',  # assumes a Project model exists
        on_delete=models.CASCADE,
        db_column='project_id',
        related_name='memberships',
        null=False,
        blank=False
    )
    employees = models.ForeignKey(
        'Employees',  # assumes an Employee model exists
        on_delete=models.CASCADE,
        db_column='member_id',
        related_name='project_memberships',
        null=False,
        blank=False
    )
    is_admin = models.BooleanField(default=False, null=False, blank=False)
    system_creation_time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    system_update_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'project_memberships'

    def __str__(self):
        return f"{self.member} → {self.project}"
    


class Message(models.Model):
    class Status(models.TextChoices):
        INACTIVE = '0', 'Inactive'
        ACTIVE = '1', 'Active'
        DELETED = '5', 'Deleted'

    id = models.BigAutoField(primary_key=True)  # bigserial
    project = models.ForeignKey(
        'Project',  # assumes Project model exists
        on_delete=models.CASCADE,
        db_column='project_id',
        related_name='messages',
        null=False,
        blank=False
    )
    employees = models.ForeignKey(
        'Employees',  # assumes Employee model exists
        on_delete=models.CASCADE,
        db_column='sender_id',
        related_name='sent_messages',
        null=False,
        blank=False
    )
    text_body = models.TextField(null=True, blank=True)  # optional
    has_media = models.BooleanField(default=False, null=False, blank=False)
    media_url = models.TextField(null=True, blank=True)  # optional
    system_creation_time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    system_update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.ACTIVE,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Message {self.id} by {self.sender}"


from django.db import models

class Status_1(models.IntegerChoices):
    INACTIVE = 2, "Inactive"
    ACTIVE = 1, "Active"
    DELETED = 5, "Deleted"
    
class TableTestingEnumData(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.IntegerField(
        choices=Status_1.choices,
        default=Status_1.ACTIVE,
        null=False
    )

    class Meta:
        db_table = 'tablefortest'

    def __str__(self):
        return f"Message {self.id} by {self.get_status_display()}"




