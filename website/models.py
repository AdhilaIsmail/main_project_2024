from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, email, role=None, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    DONOR = 1
    HOSPITAL = 2
    STAFF = 3
    REGISTEREDDONOR = 4
    LABSTAFF = 5

    ROLE_CHOICE = (
        (DONOR, 'DONOR'),
        (HOSPITAL, 'HOSPITAL'),
        (STAFF, 'STAFF'),
        (REGISTEREDDONOR, 'REGISTEREDDONOR'),
        (LABSTAFF, 'LABSTAFF'),
    )

    username=None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)
    role = models.IntegerField(choices=ROLE_CHOICE,default='1')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def set_hospital_role(self):
        self.role = CustomUser.HOSPITAL
        self.save()

#donor model
from django.utils import timezone
class Donor(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    place = models.CharField(max_length=100)
    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    
#donor response model
from django.db import models
class DonorResponse(models.Model):
    name = models.CharField(max_length=255)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, default=None)
    age = models.IntegerField()
    bloodType = models.CharField(max_length=5)
    weight = models.FloatField()
    donorHistory = models.CharField(max_length=3)
    difficulty = models.CharField(max_length=3)
    donated = models.CharField(max_length=3)
    allergies = models.CharField(max_length=3)
    alcohol = models.CharField(max_length=3)
    jail = models.CharField(max_length=3)
    surgery = models.CharField(max_length=3)
    diseased = models.CharField(max_length=3)
    hivaids = models.CharField(max_length=3)
    pregnant = models.CharField(max_length=3, null=True, blank=True)
    child = models.CharField(max_length=3, null=True, blank=True)
    feelgood = models.CharField(max_length=3, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)



#hospital registration model
class HospitalRegister(models.Model):
    hospitalName = models.CharField(max_length=100,unique=True)
    contactPerson = models.CharField(max_length=100)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    location = models.TextField()
    ownership = models.CharField(max_length=100)
    hospitalURL = models.URLField(blank=True)
    status = models.CharField(max_length=20, default='Active')
    # password = models.CharField(max_length=128)

    def __str__(self):
        return self.hospitalName



    
from django.db import models

class BloodType(models.Model):
    blood_type = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.blood_type

    
    
from django.db import models
from django.core.exceptions import ValidationError

class BloodInventory(models.Model):
    blood_type = models.OneToOneField(BloodType, on_delete=models.CASCADE, primary_key=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.blood_type} - {self.quantity} units available"

    def update_quantity(self, units):
        if self.quantity >= units:
            self.quantity -= units
            self.save()
        else:
            raise ValidationError("Not enough blood units available.")




#blood request model
from datetime import datetime 
class BloodRequest(models.Model):

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, default=None)
    blood_group = models.CharField(max_length=5)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    purpose = models.TextField()
    is_immediate = models.BooleanField(default=False)
    requested_date = models.DateField(default=datetime.now)
    requested_time = models.TimeField(default=datetime.now)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user} - Requested on {self.requested_date} at {self.requested_time}"

#staff registration model
class Staff(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    dob = models.DateField()
    role = models.CharField(max_length=20, choices=CustomUser.ROLE_CHOICE,blank=True,null=True)

    def __str__(self):
        return self.name



#add gramapanchayats
#..................................
class Grampanchayat(models.Model):
    
    name_of_grampanchayat = models.CharField(max_length=255, unique=True)
    grampanchayat_id = models.CharField(max_length=10, unique=True)
   
    def __str__(self):
        return self.name_of_grampanchayat
    
#.................................

#assign grampanchayat
from django.db import models
from django.db.models import UniqueConstraint
from .models import Staff, Grampanchayat

class AssignGrampanchayat(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    grampanchayat1 = models.ForeignKey(Grampanchayat, on_delete=models.CASCADE, related_name='assignment1')
    grampanchayat2 = models.ForeignKey(Grampanchayat, on_delete=models.CASCADE, related_name='assignment2')
    grampanchayat3 = models.ForeignKey(Grampanchayat, on_delete=models.CASCADE, related_name='assignment3')
    grampanchayat4 = models.ForeignKey(Grampanchayat, on_delete=models.CASCADE, related_name='assignment4')
    grampanchayat5 = models.ForeignKey(Grampanchayat, on_delete=models.CASCADE, related_name='assignment5')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['staff', 'grampanchayat1'],
                name='unique_assignment1',
            ),
            UniqueConstraint(
                fields=['staff', 'grampanchayat2'],
                name='unique_assignment2',
            ),
            UniqueConstraint(
                fields=['staff', 'grampanchayat3'],
                name='unique_assignment3',
            ),
            UniqueConstraint(
                fields=['staff', 'grampanchayat4'],
                name='unique_assignment4',
            ),
            UniqueConstraint(
                fields=['staff', 'grampanchayat5'],
                name='unique_assignment5',
            ),
        ]

    def __str__(self):
        return f"Assignments for {self.staff.name}"


#laboratory
from django.db import models
class Laboratory(models.Model):
    laboratoryName = models.CharField(max_length=255)

    def __str__(self):
        return self.laboratoryName

#labselection  
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
class LabSelection(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.donor.username} - {self.selected_lab}"

  



from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class UploadedFile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='media/uploads/')
    approval_status = models.CharField(max_length=50, default='Pending')
    timestamp = models.DateTimeField(null=True)


from django.db import models
User = get_user_model()
class BloodCamp(models.Model):
    campDate = models.DateField()
    campName = models.CharField(max_length=255)
    campAddress = models.TextField()
    campDistrict = models.CharField(max_length=100, default='Kottayam')
    # campContact = models.CharField(max_length=15)  # Assuming a phone number can be up to 15 characters
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,default=None)
    conductedBy = models.CharField(max_length=255)
    organizedBy = models.ForeignKey(Staff, on_delete=models.CASCADE)
    gramPanchayat = models.CharField(max_length=100, default='DefaultPanchayat',null=True, blank=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    startTime2 = models.TimeField(null=True)
    endTime2 = models.TimeField(null=True)

    def __str__(self):
        return self.campName


class Appointment(models.Model):
    camp = models.ForeignKey(BloodCamp, on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=50)  # You may want to choose a more appropriate data type
    booked_by_donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('donated', 'Donated'), ('not_donated', 'Not Donated')],  null=True, blank=True)
    # Add other fields for the Appointment model as needed

    def is_expired(self):
        current_date = timezone.now().date()
        return self.camp.campDate < current_date

    def save(self, *args, **kwargs):
        if self.is_expired():
            self.status = 'expired'
        super(Appointment, self).save(*args, **kwargs)

    def get_donor_name(self):
        return self.booked_by_donor.full_name if self.booked_by_donor else 'Anonymous'

    def __str__(self):
        donor_name = self.get_donor_name()
        return f"{self.camp.campName} - {self.time_slot} - Booked by: {donor_name}"

    

from django.db import models
from .models import Appointment, Donor  # Import your Appointment and Donor models here

class DonorDetails(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    date_of_donation = models.DateField()
    expiry_date = models.DateField()
    sample_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()  # Add the quantity field
    
    # Add other fields as needed

    def __str__(self):
        return self.donor.full_name



from django.db import models
from .models import Appointment, Donor  # Import your Appointment and Donor models here

class NotDonatedReason(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return self.donor.full_name
    




class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    razorpay_order_id = models.CharField(max_length=255,default='')  # Razorpay order ID
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True, null=True)  # Use auto_now_add=True for initial creation


    def _str_(self):
        return f"Payment ID: {self.id}, Status: {self.payment_status}"



from django.db import models

class LaboratoryTest(models.Model):
    test_name = models.CharField(max_length=255)
    test_price = models.DecimalField(max_digits=10, decimal_places=2)
    package_details = models.JSONField()

    def __str__(self):
        return self.test_name
    


# models.py
from django.db import models

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField()
    selected_test = models.ForeignKey(LaboratoryTest, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Booking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    booked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.patient.full_name} on {self.booked_date}"
