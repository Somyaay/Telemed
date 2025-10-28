import os
import django
import random
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files.base import ContentFile

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')
django.setup()

from django.contrib.auth.models import User, Group
from hospital.models import Doctor

def generate_random_avatar(name):
    """Generate a unique avatar based on doctor's name"""
    # Create a new image with a random background color
    size = 200
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)

    # Generate random background color
    bg_color = (
        random.randint(100, 240),
        random.randint(100, 240),
        random.randint(100, 240)
    )
    
    # Generate contrasting text color
    text_color = (
        (bg_color[0] + 128) % 256,
        (bg_color[1] + 128) % 256,
        (bg_color[2] + 128) % 256
    )

    # Fill background
    draw.rectangle([(0, 0), (size, size)], fill=bg_color)

    # Draw a circle
    circle_color = (
        (bg_color[0] + 50) % 256,
        (bg_color[1] + 50) % 256,
        (bg_color[2] + 50) % 256
    )
    margin = size // 4
    draw.ellipse([(margin, margin), (size-margin, size-margin)], fill=circle_color)

    # Get initials from name
    initials = name[0].upper()
    if ' ' in name:
        initials += name.split()[1][0].upper()

    # Calculate text size and position (approximate since we don't have font size)
    text_x = size // 2 - 20
    text_y = size // 2 - 30

    # Draw text (initials)
    draw.text((text_x, text_y), initials, fill=text_color)

    # Add some random decorative elements
    for _ in range(3):
        x1 = random.randint(0, size)
        y1 = random.randint(0, size)
        x2 = random.randint(0, size)
        y2 = random.randint(0, size)
        draw.line([(x1, y1), (x2, y2)], fill=text_color, width=2)

    # Convert image to bytes
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_content = ContentFile(img_io.getvalue())
    
    return img_content

# Sample doctor data
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

def create_sample_doctors():
    # Get or create the DOCTOR group
    doctor_group, _ = Group.objects.get_or_create(name='DOCTOR')
    
    for doc_data in doctors_data:
        try:
            # Create User instance
            username = f"{doc_data['first_name'].lower()}.{doc_data['last_name'].lower()}"
            password = "doctor123"  # Default password
            
            # Check if user exists
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=doc_data['first_name'],
                    last_name=doc_data['last_name']
                )
                
                # Add user to DOCTOR group
                doctor_group.user_set.add(user)
                
                # Generate avatar
                full_name = f"{doc_data['first_name']} {doc_data['last_name']}"
                avatar = generate_random_avatar(full_name)
                
                # Create Doctor instance
                doctor = Doctor.objects.create(
                    user=user,
                    address=doc_data['address'],
                    mobile=doc_data['mobile'],
                    department=doc_data['department'],
                    status=True  # Automatically approve these sample doctors
                )
                
                # Save the generated avatar
                avatar_filename = f"doctor_{username}_avatar.png"
                doctor.profile_pic.save(avatar_filename, avatar, save=True)
                print(f"Created doctor: {doc_data['first_name']} {doc_data['last_name']} ({doc_data['department']})")
            else:
                print(f"Doctor {username} already exists, skipping...")
                
        except Exception as e:
            print(f"Error creating doctor {doc_data['first_name']} {doc_data['last_name']}: {str(e)}")

def run():
    print("Deleting existing doctors...")
    Doctor.objects.all().delete()
    User.objects.filter(groups__name='DOCTOR').delete()
    
    print("\nCreating new sample doctors...")
    create_sample_doctors()
    print("\nDoctors created successfully!")
    print("You can now log in with any of these usernames (firstname.lastname) and password 'doctor123'")