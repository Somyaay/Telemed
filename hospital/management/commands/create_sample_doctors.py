from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from hospital.models import Doctor
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates 10 sample doctors with different specializations'

    def handle(self, *args, **kwargs):
        doctors_data = [
            {
                'first_name': 'James',
                'last_name': 'Wilson',
                'department': 'Cardiologist',
                'mobile': '9876543210',
                'address': '123 Medical Center Dr'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'department': 'Dermatologists',
                'mobile': '9876543211',
                'address': '456 Health Ave'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Chen',
                'department': 'Emergency Medicine Specialists',
                'mobile': '9876543212',
                'address': '789 Hospital Blvd'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Brown',
                'department': 'Allergists/Immunologists',
                'mobile': '9876543213',
                'address': '321 Care Street'
            },
            {
                'first_name': 'David',
                'last_name': 'Martinez',
                'department': 'Anesthesiologists',
                'mobile': '9876543214',
                'address': '654 Wellness Road'
            },
            {
                'first_name': 'Lisa',
                'last_name': 'Anderson',
                'department': 'Colon and Rectal Surgeons',
                'mobile': '9876543215',
                'address': '987 Healing Path'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Taylor',
                'department': 'Cardiologist',
                'mobile': '9876543216',
                'address': '147 Medicine Lane'
            },
            {
                'first_name': 'Jennifer',
                'last_name': 'Garcia',
                'department': 'Dermatologists',
                'mobile': '9876543217',
                'address': '258 Doctor Drive'
            },
            {
                'first_name': 'William',
                'last_name': 'Lee',
                'department': 'Emergency Medicine Specialists',
                'mobile': '9876543218',
                'address': '369 Clinic Court'
            },
            {
                'first_name': 'Maria',
                'last_name': 'Rodriguez',
                'department': 'Allergists/Immunologists',
                'mobile': '9876543219',
                'address': '741 Health Park'
            }
        ]

        # Get or create the DOCTOR group
        doctor_group, _ = Group.objects.get_or_create(name='DOCTOR')
        
        try:
            with transaction.atomic():
                for doc_data in doctors_data:
                    # Create User instance
                    username = f"{doc_data['first_name'].lower()}.{doc_data['last_name'].lower()}"
                    password = "doctor123"  # Default password
                    
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=doc_data['first_name'],
                        last_name=doc_data['last_name']
                    )
                    
                    # Add user to DOCTOR group
                    doctor_group.user_set.add(user)
                    
                    # Create Doctor instance
                    doctor = Doctor.objects.create(
                        user=user,
                        address=doc_data['address'],
                        mobile=doc_data['mobile'],
                        department=doc_data['department'],
                        status=True  # Automatically approve these sample doctors
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created doctor: {doc_data["first_name"]} {doc_data["last_name"]} ({doc_data["department"]})'
                        )
                    )
                    
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created 10 sample doctors\nUsernames are firstname.lastname (all lowercase)\nDefault password for all: doctor123'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating doctors: {str(e)}')
            )