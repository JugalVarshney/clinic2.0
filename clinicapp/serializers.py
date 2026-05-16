from rest_framework import serializers
from .models import User, Doctor, Drug, Prescription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'mobile', 'address')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Doctor
        fields = ('id', 'user', 'specialization', 'email', 'qualifications', 'experience', 'fees', 'image')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'drug_name')

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = UserSerializer(read_only=True)
    
    class Meta:
        model = Prescription
        fields = ('id', 'doctor', 'patient', 'date', 'prescription_type', 'patient_name', 
                 'patient_age', 'patient_address', 'diagnosis', 'treatment', 'tests', 
                 'additional_fields', 'signature')