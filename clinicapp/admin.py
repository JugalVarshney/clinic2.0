from django.contrib import admin
from .models import User, Doctor, Drug, Prescription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience', 'fees')
    list_filter = ('specialization',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')
    ordering = ('user__username',)

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('drug_name',)
    search_fields = ('drug_name',)
    ordering = ('drug_name',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'doctor', 'patient', 'date', 'prescription_type')
    list_filter = ('date', 'prescription_type', 'doctor__specialization')
    search_fields = ('patient__username', 'doctor__user__username', 'diagnosis')
    ordering = ('-date',)
    date_hierarchy = 'date'
