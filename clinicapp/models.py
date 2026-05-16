from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    # Override the default username field to use email or custom ID
    # We'll keep the username for Django auth but add our custom fields
    
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Custom ID fields (keeping your original structure)
    adminID = models.CharField(max_length=20, unique=True, blank=True, null=True)
    patientID = models.CharField(max_length=20, unique=True, blank=True, null=True)
    docID = models.CharField(max_length=20, unique=True, blank=True, null=True)
    staffID = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    # Fix reverse accessor clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='clinicapp_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='clinicapp_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        db_table = 'users'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    experience = models.IntegerField(default=0)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.CharField(max_length=255, blank=True, null=True)  # Store path/URL
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        db_table = 'doctors'


class Drug(models.Model):
    drug_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.drug_name
    
    class Meta:
        db_table = 'drugs'


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    date = models.DateField()
    prescription_type = models.CharField(max_length=50)  # Renamed from 'type' to avoid Python keyword
    patient_name = models.CharField(max_length=255)
    patient_age = models.IntegerField()
    patient_address = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    tests = models.TextField(blank=True, null=True)
    additional_fields = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Prescription {self.prescription_id} for {self.patient_name}"
    
    class Meta:
        db_table = 'prescriptions'
