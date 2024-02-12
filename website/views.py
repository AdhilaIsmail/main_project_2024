
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Donor,Staff
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST




# from django.core.mail import send_mail
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required

# from .models import Donor
User = get_user_model()

def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def service(request):
    return render(request, 'service.html')

def registerasdonor(request):
    return render(request, 'registerasdonor.html')
# def donatenow(request):
#     return render(request, 'donatenow.html')

def homebloodbank(request):
    Donor.objects.filter(user=request.user).exists()
        # User is already registered as a donor, you can redirect or render a different page

    return render(request, 'homebloodbank.html')
def testimonial(request):
    return render(request, 'testimonial.html')


##checking
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import CustomUser,LabSelection
from datetime import timedelta
from .models import CustomUser, LabSelection, UploadedFile
from django.utils import timezone

def loginn(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == CustomUser.REGISTEREDDONOR:
                lab_selection = LabSelection.objects.filter(donor=user).order_by('-timestamp').first()
                if lab_selection and lab_selection.timestamp + timedelta(days=3) > timezone.now():
                    return redirect('uploadresult2', lab_selection_timestamp=str(lab_selection.timestamp))
                else:
                    # Check if the user has already uploaded a file within the 3-day limit
                    if UploadedFile.objects.filter(user=user, timestamp__gte=timezone.now() - timedelta(days=3)).exists():
                        return redirect('waitforemail')
                    else:
                        messages.warning(request, 'The three-day window for uploading results has expired.')
                        return redirect('donatenow')

            if user.is_superadmin:  # Check if the user is a superuser (admin)
                return redirect('adminindex')  # Redirect to the admin dashboard
            elif user.role == CustomUser.HOSPITAL:
                return redirect('hospitalhome')
            elif user.role == CustomUser.STAFF:
                return redirect('staffindex')
            else:
                return redirect('index')  # Redirect to the custom dashboard for non-admin users
        else:
            # messages.error(request, "Invalid Login")
            # return redirect('loginn')
            error_message = "Invalid login credentials."
            return render(request,'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    



def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('pass', None)
        role=User.DONOR

        if email and phone and password and role:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'registration.html', {'error_message': error_message})
            
            else:
                print('Enydsgv')
                user = User(email=email, phone=phone, role=role)
                user.set_password(password)  # Set the password securely
                user.save()
                return redirect('loginn')  
            
    return render(request, 'registration.html')

#this is for normal registratio
def registration(request):
    messages=""
    if request.method == "POST":
        # fullName = request.POST['fullName']
        username = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            # if User.objects.filter(fullName=fullName).exists():
            #     return render(request, 'registration.html', {'fullName_exists': True})
            if User.objects.filter(username=username).exists():
                return render(request, 'registration.html', {'username_exists': True})


            # elif User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email already exists')
            #     return redirect('registration')
            
            else:
                
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # messages.success(request, 'Registration successful. You can now log in.')
                return redirect('loginn')

        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('registration')
    else:
        return render(request, 'registration.html')

def loggout(request):
    auth.logout(request)
    return redirect('/')

#this is for register as donor
from django.shortcuts import render, redirect
from .forms import DonorRegistrationForm




from .models import CustomUser

def donatenow(request):
    if request.user.is_authenticated and request.user.role == CustomUser.REGISTEREDDONOR:
        donor = Donor.objects.get(user=request.user)
        print(donor)
        last_submission = DonorResponse.objects.filter(user=request.user).order_by('-timestamp').first()
        if last_submission and (timezone.now() - last_submission.timestamp) < timedelta(days=3):
            # User has already submitted the form in the last 3 days
            return render(request, 'waitforemail.html')  # Replace with your template or redirect
        return render(request, 'donatenow.html', {'donor': donor})
    else:
        # Redirect or render the "Register as Donor" page for others
        return redirect('registerasdonor')
    
def registereddonortodonatenow(request):
    return render(request, 'registereddonortodonatenow.html')




def register_donor(request):
    if request.method == 'POST':
        # Handle form submission and validation here
        form = DonorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Update the user fields
            request.user.email = form.cleaned_data['email']
            request.user.phone = form.cleaned_data['phone']
            request.user.save(update_fields=['email', 'phone'])

            # Save the form data to create a new Donor record
            donor = form.save(commit=False)
            donor.user = request.user  # Automatically associates with CustomUser
            donor.save()

            # Update the user's role to "Registered Donor"
            if request.user.role == CustomUser.DONOR:
                request.user.role = CustomUser.REGISTEREDDONOR
                request.user.save()

            # Redirect to a success page or perform other actions
            return redirect('registereddonortodonatenow')  # Change to your actual success page URL

    else:
        form = DonorRegistrationForm()

    return render(request, 'registerasdonor.html', {'form': form})



from django.shortcuts import render, redirect
from .models import DonorResponse



def registereddonorresponse(request):
    donor = request.user.donor
    print(donor)
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        age = request.POST.get('age')
        bloodType = request.POST.get('bloodType')
        weight = request.POST.get('weight')
        donorHistory = request.POST.get('donorHistory')
        difficulty = request.POST.get('difficulty')
        donated = request.POST.get('donated')
        allergies = request.POST.get('allergies')
        alcohol = request.POST.get('alcohol')
        jail = request.POST.get('jail')
        surgery = request.POST.get('surgery')
        diseased = request.POST.get('diseased')
        hivaids = request.POST.get('hivaids')
        pregnant = request.POST.get('pregnant')
        child = request.POST.get('child')
        feelgood = request.POST.get('feelgood')

        # Create a DonorResponse instance and populate it with the data
        donor_response = DonorResponse(name=name,user=user,age=age,bloodType=bloodType,weight=weight,donorHistory=donorHistory,difficulty=difficulty,donated=donated,allergies=allergies,alcohol=alcohol,jail=jail,surgery=surgery,diseased=diseased,hivaids=hivaids,pregnant=pregnant,child=child,feelgood=feelgood)

        # Save the DonorResponse instance to the database
        donor_response.save()

        return redirect('notificationfordonation')
   

    return render(request, 'donatenow.html', {'donor': donor})

from django.shortcuts import render, redirect
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import LabSelection, Laboratory
from django.utils import timezone
from datetime import datetime
from django.contrib import messages

def send_sms(request):
    if request.method == 'POST':
        # Handle the form submission and extract necessary data
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        lab_id = request.POST.get('nearestLab')  # Assuming this is the lab ID
        nearest_lab_name = request.POST.get('nearestLabName')

        # Retrieve the Laboratory instance based on the lab ID
        selected_lab = get_object_or_404(Laboratory, id=lab_id)

        # Your logic to process the form data...
        lab_selection = LabSelection.objects.create(
            donor=request.user,
            selected_lab=selected_lab,
        )

        # Set session variable for lab selection timestamp
        request.session['lab_selection_timestamp'] = str(lab_selection.timestamp)
        
        # Compose the email content
        email_content = f"Greetings From Medlab Blood bank,\nFor proceeding with donation, get a sample blood test done and upload the result.\n\nSelected Lab: {nearest_lab_name}"

        # Send the email
        send_mail(
            'Blood Donation Instructions',
            email_content,
            'adhilaismail2@gmail.com',  # Sender's email address
            [email],  # Recipient's email address
            fail_silently=False,
        )

        # Your logic to handle the rest of the form submission...

        # Redirect to uploadresult and pass the timestamp of the lab selection
        return redirect('uploadresult2', lab_selection_timestamp=str(lab_selection.timestamp))

        # return redirect('uploadresult2', lab_selection_timestamp=lab_selection.timestamp)
    else:
        # Handle GET requests or other cases...
        return render(request, 'notificationfordonation.html')


from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import timedelta, datetime
from .forms import UploadFileForm
from django.contrib import messages
from .models import LabSelection
from urllib.parse import unquote




def uploadresult2(request, lab_selection_timestamp):
    # Convert the lab_selection_timestamp string to a datetime object
    lab_selection_timestamp = unquote(lab_selection_timestamp)
    print(lab_selection_timestamp)
    # Convert the lab_selection_timestamp string to a datetime object
    lab_selection_timestamp = datetime.strptime(lab_selection_timestamp, '%Y-%m-%d %H:%M:%S.%f%z')
    
    # Calculate the target date (3 days from the lab selection date)
    target_date = lab_selection_timestamp + timedelta(days=3)
    
    # Calculate the remaining time
    current_time = timezone.now()
    remaining_time = target_date - current_time
    
    if remaining_time.total_seconds() <= 0:
        messages.error(request, 'The three-day window for uploading results has expired.')
        return redirect('donatenow')

    # Check if the user has already submitted results
    user_has_submitted_results = UploadedFile.objects.filter(user=request.user).exists()

    # If the user has already submitted results, redirect or display a message
    if user_has_submitted_results:
        messages.info(request, 'You have already submitted your lab results.')
        return redirect('waitforemail')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['result_file']
            
            # Save the uploaded file to your database
            new_upload = UploadedFile(file=uploaded_file, user=request.user)
            new_upload.save()

            # Provide feedback to the user
            messages.success(request, 'File uploaded successfully.')

            # Redirect to a success page or do something else
            return redirect('waitforemail')

        else:
            # Provide feedback to the user about form validation errors
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = UploadFileForm()

    # Pass the timestamp, target date, and remaining time to the template
    context = {
        'lab_selection_timestamp': lab_selection_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        'target_date': target_date.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        'remaining_time_seconds': remaining_time.total_seconds(),
        'form': form,
    }
    
    return render(request, 'uploadresult.html', context)

def waitforemail(request):
    return render(request,'waitforemail.html')

# views.py
from django.http import JsonResponse
from .models import Laboratory

def getlaboratories(request):
    laboratories = Laboratory.objects.values('id', 'laboratoryName')
    return JsonResponse(list(laboratories), safe=False)


def notificationfordonation(request):
    return render(request, 'notificationfordonation.html')


from .forms import UploadFileForm
from .models import UploadedFile


def uploadresult(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['result_file']
            # Save the uploaded file to your database
            new_upload = UploadedFile(file=uploaded_file)
            new_upload.save()
            # Redirect to a success page or do something else
            return redirect('homebloodbank')
    else:
        form = UploadFileForm()

    return render(request, 'uploadresult.html', {'form': form})



#admin dashboard

def adminindex(request):
    donors = Donor.objects.all()
    Request=BloodRequest.objects.all()
    staffs=Staff.objects.all()
    donor_count = donors.count() 
    request_count= Request.count()
    staff_count= staffs.count()

    return render(request, 'mainuser/index.html',{'donors': donors, 'donor_count': donor_count,'request_count':request_count,'staff_count':staff_count})

def activities(request):
    return render(request, 'mainuser/activities.html')

def appointments(request):
    return render(request, 'mainuser/appointments.html')

def departments(request):
    return render(request, 'mainuser/departments.html')

def donors(request):
    return render(request, 'mainuser/donors.html')

def addhospitals(request):
    return render(request, 'mainuser/add-hospitals.html')

def hospitalregistration(request):
    return render(request, 'mainuser/hospitalregistration.html')



from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def addlab(request):
    return render(request, 'mainuser/addlab.html')



from django.shortcuts import render, redirect
from .models import Staff, Grampanchayat, AssignGrampanchayat

def assign_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staffName')
        grampanchayat1_id = request.POST.get('grampanchayat1')
        grampanchayat2_id = request.POST.get('grampanchayat2')
        grampanchayat3_id = request.POST.get('grampanchayat3')
        grampanchayat4_id = request.POST.get('grampanchayat4')
        grampanchayat5_id = request.POST.get('grampanchayat5')

        # Create AssignGrampanchayat objects
        staff = Staff.objects.get(pk=staff_id)
        grampanchayat1 = Grampanchayat.objects.get(pk=grampanchayat1_id)
        grampanchayat2 = Grampanchayat.objects.get(pk=grampanchayat2_id)
        grampanchayat3 = Grampanchayat.objects.get(pk=grampanchayat3_id)
        grampanchayat4 = Grampanchayat.objects.get(pk=grampanchayat4_id)
        grampanchayat5 = Grampanchayat.objects.get(pk=grampanchayat5_id)

        # Create AssignGrampanchayat instances
        assignment = AssignGrampanchayat.objects.create(
            staff=staff,
            grampanchayat1=grampanchayat1,
            grampanchayat2=grampanchayat2,
            grampanchayat3=grampanchayat3,
            grampanchayat4=grampanchayat4,
            grampanchayat5=grampanchayat5,
        )

        # Redirect to a success page or perform any other action
        return redirect('adminindex')  # Replace 'success_page' with the actual URL

    # If the request is not POST, render the form
    staff_members = Staff.objects.all()
    grampanchayats = Grampanchayat.objects.all()
    context = {
        'staff_members': staff_members,
        'grampanchayats': grampanchayats,
    }
    return render(request, 'mainuser/assigninggptostaff.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import AssignGrampanchayat, Grampanchayat
from django.db.models import Q
@csrf_exempt
@require_POST
def validate_assign_grampanchayat(request):
    grampanchayat_name = request.POST.get('grampanchayatName')

    # Check if the Grampanchayat exists in AssignGrampanchayat model
    try:
        AssignGrampanchayat.objects.get(
            Q(grampanchayat1__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat2__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat3__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat4__name_of_grampanchayat=grampanchayat_name) |
            Q(grampanchayat5__name_of_grampanchayat=grampanchayat_name)
        )
        
        exists = True
    except AssignGrampanchayat.DoesNotExist:
        exists = False

    return JsonResponse({'exists': exists})



from django.http import JsonResponse
from .models import Grampanchayat

def grampanchayat_list(request):
    grampanchayats = Grampanchayat.objects.all()
    data = [{'id': gp.id, 'name_of_grampanchayat': gp.name_of_grampanchayat} for gp in grampanchayats]
    return JsonResponse(data, safe=False)

#......................................................................................

def employees(request):
    return render(request, 'mainuser/employees.html')

def profile1(request):
    donor = Donor.objects.get(user=request.user)  # Adjust this based on your logic

    return render(request, 'mainuser/donorprofile.html', {'donor': donor})
    # return render(request, 'mainuser/donorprofile.html')

def editprofile(request):
    return render(request, 'mainuser/edit-profile.html')

def registereddonortable(request):
    donors = Donor.objects.all()
    donor_count = donors.count()  
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors, 'donor_count': donor_count})


def search_by_name(request):
    name = request.GET.get('name', '')
    donors = Donor.objects.filter(full_name__icontains=name)
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors})

def search_by_place(request):
    place = request.GET.get('place', '')
    donors = Donor.objects.filter(place__icontains=place)
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors})

def search_by_blood_group(request):
    blood_group = request.GET.get('blood_group', '')
    donors = Donor.objects.filter(blood_group__iexact=blood_group)
    return render(request, 'mainuser/registereddonortable.html', {'donors': donors})



from django.shortcuts import render
from .models import BloodType

def blood_inventory(request):
    blood_types = BloodType.objects.all()
    blood_data = []

    for blood_type in blood_types:
        try:
            blood_inventory = BloodInventory.objects.get(blood_type=blood_type)
            available_units = blood_inventory.quantity // 450
            blood_data.append({'blood_type': blood_type.blood_type, 'available_units': available_units})
        except BloodInventory.DoesNotExist:
            blood_data.append({'blood_type': blood_type.blood_type, 'available_units': 0})

    # Print debug statements
    print("Blood Types:", blood_types)
    print("Blood Data:", blood_data)

    context = {'blood_data': blood_data}
    return render(request, 'mainuser/bloodinventory.html', context)

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import BloodType, BloodInventory, DonorDetails

def view_detailed_details(request, blood_type):
    try:
        # Find the BloodType instance
        blood_type_obj = BloodType.objects.get(blood_type=blood_type)
        
        # Query DonorDetails based on the indirect relationship through Appointment and Donor
        donor_details = DonorDetails.objects.filter(appointment__booked_by_donor__blood_group=blood_type)

        # Try to get the BloodInventory instance
        try:
            blood_inventory = BloodInventory.objects.get(blood_type=blood_type_obj)
        except BloodInventory.DoesNotExist:
            # Handle case where BloodInventory does not exist for the given blood type
            blood_inventory = None

        context = {
            'blood_type': blood_type_obj.blood_type,
            'available_units': blood_inventory.quantity // 450 if blood_inventory else 0,
            'donor_details': donor_details,
        }

        return render(request, 'mainuser/view_detailed_details.html', context)
    except BloodType.DoesNotExist:
        # Handle case where blood type does not exist
        return HttpResponse("Blood type does not exist.")
    except ObjectDoesNotExist:
        # Handle other DoesNotExist exceptions
        return HttpResponse("Requested data not found.")



# In views.py

from django.http import HttpResponse

def handle_empty_blood_type(request):
    return HttpResponse("Handling empty blood type...")









from .models import Staff

def registeredstafftable(request):
    staff_list= Staff.objects.all()
    return render(request, 'mainuser/registeredstafftable.html',{'staff_list':staff_list})

def registeredstafftablelab(request):
    staff_list= Staff.objects.all()
    return render(request, 'mainuser/registeredlabstafftable.html',{'staff_list':staff_list})

# def listgps(request):
#     return render(request, 'mainuser/listgps.html')


from django.shortcuts import render
from .models import Grampanchayat

def listgps(request):
    grampanchayats = Grampanchayat.objects.all()
    return render(request, 'mainuser/listgps.html', {'grampanchayats': grampanchayats})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Grampanchayat

def edit_grampanchayat(request, pk):
    grampanchayat = get_object_or_404(Grampanchayat, pk=pk)

    if request.method == 'POST':
        grampanchayat.grampanchayat_id = request.POST.get('grampanchayat_id')
        grampanchayat.name_of_grampanchayat = request.POST.get('name_of_grampanchayat')
        # Update other fields as needed
        grampanchayat.save()
        return redirect('listgps')  # Redirect to the list view after successful edit

    return render(request, 'mainuser/edit-grampanchayat.html', {'grampanchayat': grampanchayat})



def addgps(request):
    return render(request, 'mainuser/add-grampanchayat.html')

from .models import Grampanchayat
from django.shortcuts import render, redirect

def grampanchayat_registration(request):
    error_message_id = ''
    error_message_name = ''
    
    if request.method == 'POST':
        grampanchayat_id = request.POST['grampanchayat_id']
        name_of_grampanchayat = request.POST['name_of_grampanchayat']
        
        # Check if a Grampanchayat with the given ID already exists
        if Grampanchayat.objects.filter(grampanchayat_id=grampanchayat_id).exists():
            error_message_id = 'Grampanchayat with this ID already exists'
        # Check if a Grampanchayat with the given name already exists
        if Grampanchayat.objects.filter(name_of_grampanchayat=name_of_grampanchayat).exists():
            error_message_name = 'Grampanchayat with this name already exists'
        # If no errors, create a new Grampanchayat
        if not error_message_id and not error_message_name:
            grampanchayat = Grampanchayat(
                grampanchayat_id=grampanchayat_id,
                name_of_grampanchayat=name_of_grampanchayat
            )
            grampanchayat.save()
            return redirect('listgps')  # Redirect to a success page or list view

    return render(request, 'mainuser/add-grampanchayat.html', {'error_message_id': error_message_id, 'error_message_name': error_message_name})


def addnewgroup(request):
    return render(request, 'mainuser/addnewgroup.html')


from django.core.mail import send_mail
from django.contrib.auth import get_user_model
def hospital_registration(request):
    if request.method == 'POST':
        hospitalName = request.POST.get('hospitalName')
        contactPerson = request.POST.get('contactPerson')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        # gpsCoordinates = request.POST.get('gpsCoordinates')
        ownership = request.POST.get('ownership')
        hospitalURL = request.POST.get('hospitalURL')
        password = request.POST.get('password')
        
        roles = CustomUser.HOSPITAL
        print(roles)
        if CustomUser.objects.filter(email=email,role=CustomUser.HOSPITAL).exists():
            return render(request, 'mainuser/hospitalregistration.html')
        else:
            user=CustomUser.objects.create_user(email=email,phone=phone,password=password)
            user.role = CustomUser.HOSPITAL
            user.save()
            hospitalRegister = HospitalRegister(user=user,hospitalName=hospitalName, contactPerson=contactPerson, location=location,ownership=ownership,hospitalURL=hospitalURL)
            hospitalRegister.save()


            subject = 'Medlab Blood Bank: Your Login Credentials'
            message = f'Hello,\n\nGreetings from Medlab Blood Bank. Below are your hospital login credentials:\n\nUsername: {email}\nPassword: {password}\n\nYou can use these credentials to log in to your hospital\'s account at Medlab Blood Bank.\n\nBest regards,\nThe Medlab Blood Bank Team'
            from_email = 'your_email@example.com'  # Change to your email address
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            return redirect('registeredhospitaltable')

        
    else:
        return render(request, 'mainuser/hospitalregistration.html')

from django.shortcuts import render
from .models import HospitalRegister

def registeredhospitaltable(request):
    hospitals = HospitalRegister.objects.all()
    return render(request, 'mainuser/registeredhospitaltable.html', {'hospitals': hospitals})




from .models import Staff  # Import the Staff model
def stafflist(request):
    # Retrieve the staff data from the database
    staff_list = Staff.objects.all()
    # Pass the staff data to the template
    context = {'staff_list': staff_list}
    return render(request, 'staff/stafflist.html', context)

#hospital
def hospitalhome(request):
    return render(request, 'hospital/hospitalhome.html')

def requestblood(request):
    return render(request, 'hospital/requestblood.html')



def bloodavailability(request):
    blood_types = BloodType.objects.all()
    blood_data = []

    for blood_type in blood_types:
        try:
            blood_inventory = BloodInventory.objects.get(blood_type=blood_type)
            available_units = blood_inventory.quantity // 450
            blood_data.append({'blood_type': blood_type.blood_type, 'available_units': available_units})
        except BloodInventory.DoesNotExist:
            blood_data.append({'blood_type': blood_type.blood_type, 'available_units': 0})

    # Print debug statements
    print("Blood Types:", blood_types)
    print("Blood Data:", blood_data)

    context = {'blood_data': blood_data}
    return render(request, 'hospital/bloodavailability.html', context)

def hospitalabout(request):
    return render(request, 'hospital/hospitalabout.html')


from django.core.mail import send_mail
from django.contrib.auth import get_user_model

def staff_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'mainuser/staffregistration.html', {'error_message': 'Email address already exists.'})
        
        if not name or not age or not gender or not dob or not email or not phone or not password or not role:
            return render(request, 'mainuser/staffregistration.html', {'error_message': 'Please fill in all required fields.'})
        
        try:
            role_mapping = {
                'LABSTAFF': CustomUser.LABSTAFF,
                'BLOODBANKSTAFF': CustomUser.STAFF,  # Assuming staff in CustomUser model is blood bank staff
            }
            # Create a CustomUser instance
            user = CustomUser.objects.create_user(email=email, phone=phone, password=password)
            user.role = role_mapping.get(role, CustomUser.STAFF)
            user.save()

            # Create a Staff instance and associate it with the user
            staff = Staff(name=name, age=age, user=user, gender=gender, dob=dob, role=role)
            staff.save()

            subject = 'Medlab Blood Bank : Your Login Credentials'
            message = f'Hello,\n\nGreetings from Medlab Blood Bank. Below are your login credentials:\n\nUsername: {email}\nPassword: {password}\n\nYou can use these credentials to log in to your account at Medlab Blood Bank.\n\nBest regards,\nThe Medlab Blood Bank Team'
            from_email = 'adhilaismail2@gmail.com'  # Change to your email address
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            

            return redirect('registeredstafftable')
        
        except IntegrityError as e:
            return render(request, 'mainuser/staffregistration.html', {'error_message': 'An error occurred during registration.'})
        
    else:
        return render(request, 'mainuser/staffregistration.html')


# from django.shortcuts import render, redirect
# from .forms import BloodTypeForm
# from django.db import IntegrityError  # Import IntegrityError

# def addblood(request):
#     if request.method == 'POST':
#         form = BloodTypeForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('bloodinventory')
#             except IntegrityError:
#                 form.add_error('blood_type', 'Blood type already exists.')  # Add a form error
#     else:
#         form = BloodTypeForm()
#     return render(request, 'mainuser/addnewgroup.html', {'form': form})

#new
from django.shortcuts import render, redirect
from .forms import BloodTypeForm
from django.db import IntegrityError
from .models import BloodInventory  # Import BloodInventory model

def addblood(request):
    if request.method == 'POST':
        form = BloodTypeForm(request.POST)
        if form.is_valid():
            try:
                blood_type = form.save()

                # Create a corresponding BloodInventory entry for the new blood type
                BloodInventory.objects.create(blood_type=blood_type)

                return redirect('bloodinventory')
            except IntegrityError:
                form.add_error('blood_type', 'Blood type already exists.')  # Add a form error

    else:
        form = BloodTypeForm()

    return render(request, 'mainuser/addnewgroup.html', {'form': form})




# views.py




from django.shortcuts import render
from .models import BloodInventory  # Import your BloodInventory model

def blood_inventory_view(request):
    blood_inventory = BloodInventory.objects.all()  # Fetch blood inventory data from the database
    return render(request, 'staff/bloodinventorystaff.html', {'blood_inventory': blood_inventory})



from django.shortcuts import render, redirect
from .models import BloodRequest  # Import your model
from datetime import datetime 

from django.contrib import messages
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Donor

@login_required
def view_profile(request):
    user_profile = request.user
    donor_profile = Donor.objects.get(user=user_profile)
    context = {
        'user_profile':user_profile,
        'donor_profile':donor_profile
    }

    return render(request, 'user_profile.html', context)

    
from django.shortcuts import render, redirect
from django.contrib import messages
# Assuming you have stored the OTP in the session as 'hospital_otp'
from django.shortcuts import render, redirect
from django.core.mail import send_mail  # Import send_mail
from django.utils.crypto import get_random_string

def verify_hospital(request,blood_request_id):
    blood_request = BloodRequest.objects.get(id=blood_request_id)
    if request.method == 'POST':
        # Get the entered OTP from the form
        entered_otp = request.POST.get('otp')
        
        # Get the OTP stored in the session
        stored_otp = request.session.get('hospital_otp')

        if entered_otp == stored_otp:
            # OTP is correct, clear it from the session
            del request.session['hospital_otp']

            # Redirect to the hospital home page
            url = reverse('requestsent', args=[blood_request_id])
            return redirect(url)
        else:
            # OTP is incorrect, display an error message
            messages.error(request, 'Invalid OTP. Please try again.')

    # Render the OTP verification page
    return render(request, 'hospital/verify_otp.html')





from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags  # Import the strip_tags function
from .models import BloodRequest

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('new_status')

        blood_request = get_object_or_404(BloodRequest, id=request_id)
        blood_request.status = new_status
        blood_request.save()

        # Send email to the user
        send_confirmation_email(blood_request.user.email, new_status)

        return JsonResponse({'requests': True})

    return JsonResponse({'requests': False})

def send_confirmation_email(to_email, status):
    subject = 'Blood Request Status Update'
    html_message = render_to_string('mainuser/email_template.html', {'status': status})
    plain_message = strip_tags(html_message)  # Create a plain text version of the email

    from_email = 'adhilaismail2@gmail.com'
    recipient_list = [to_email]

    # Set the content_type parameter to 'html'
    send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=html_message)




def requests(request):
    return render(request, 'mainuser/viewrequests.html')



from django.shortcuts import render
from .models import BloodRequest  # Import the BloodRequest model

def blood_request_list(request):
    blood_requests = BloodRequest.objects.all()  # Retrieve all BloodRequest objects from the database
    return render(request, 'mainuser/viewrequests.html', {'blood_requests': blood_requests})



#staff
def staffindex(request):
    donors = Donor.objects.all()
    Request=BloodRequest.objects.all()
    staffs=Staff.objects.all()
    donor_count = donors.count() 
    request_count= Request.count()
    staff_count= staffs.count()
    return render(request, 'staff/index.html',{'donors': donors, 'donor_count': donor_count,'request_count':request_count,'staff_count':staff_count})

def activities(request):
    return render(request, 'staff/activities.html')

# def donorappointments(request):
#     return render(request, 'staff/donorappointments.html')


from django.shortcuts import render, redirect
from .models import Appointment, DonorDetails
from django.http import JsonResponse
from django.utils import timezone

def donorappointments(request):
    # Retrieve the list of appointments
    appointments = Appointment.objects.all()

    # Update the status for each appointment
    for appointment in appointments:
        # Check if there is a DonorDetails entry for this appointment
        donor_details = DonorDetails.objects.filter(appointment=appointment).first()
        if donor_details:
            appointment.status = 'donated'
        else:
            appointment.status = 'not_donated'

    return render(request, 'staff/donorappointments.html', {'appointments': appointments})


def bloodbankcamps(request):
    return render(request, 'staff/bloodbankcamps.html')

def addhospitals(request):
    return render(request, 'staff/add-hospitals.html')

def employees(request):
    return render(request, 'staff/employees.html')

def profile(request):
    return render(request, 'staff/profile.html')

from django.shortcuts import render
from .models import BloodType

# def bloodinventorystaff(request):
#     blood_types = BloodType.objects.all()
#     return render(request, 'staff/bloodinventorystaff.html', {'blood_types': blood_types})
def bloodinventorystaff(request):
    blood_types = BloodType.objects.all()
    blood_data = []

    for blood_type in blood_types:
        try:
            blood_inventory = BloodInventory.objects.get(blood_type=blood_type)
            available_units = blood_inventory.quantity // 450
            blood_data.append({'blood_type': blood_type.blood_type, 'available_units': available_units})
        except BloodInventory.DoesNotExist:
            blood_data.append({'blood_type': blood_type.blood_type, 'available_units': 0})

    # Print debug statements
    print("Blood Types:", blood_types)
    print("Blood Data:", blood_data)

    context = {'blood_data': blood_data}
    return render(request, 'staff/bloodinventorystaff.html', context)



def editprofile(request):
    return render(request, 'staff/edit-profile.html')

def registereddonortablestaff(request):
    donors = Donor.objects.all()
    donor_count = donors.count()  
    return render(request, 'staff/registereddonortable.html', {'donors': donors, 'donor_count': donor_count})

def search_by_name(request):
    name = request.GET.get('name', '')
    donors = Donor.objects.filter(full_name__icontains=name)
    return render(request, 'staff/registereddonortable.html', {'donors': donors})

def search_by_place(request):
    place = request.GET.get('place', '')
    donors = Donor.objects.filter(place__icontains=place)
    return render(request, 'staff/registereddonortable.html', {'donors': donors})

def search_by_blood_group(request):
    blood_group = request.GET.get('blood_group', '')
    donors = Donor.objects.filter(blood_group__iexact=blood_group)
    return render(request, 'staff/registereddonortable.html', {'donors': donors})



from django.shortcuts import render
from .models import HospitalRegister


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import BloodCamp, Staff, AssignGrampanchayat, Grampanchayat
from django.contrib.auth.decorators import login_required

@login_required
def create_blood_camp(request):
    user = request.user
    staff_member = Staff.objects.get(user=user)
    
    # Query staff assignments for the logged-in staff member
    staff_assignments = AssignGrampanchayat.objects.filter(staff=staff_member)
    
    # Extract Gram Panchayats from staff assignments
    assigned_gram_panchayat = [
        getattr(staff_assignments, f'grampanchayat{i}', None)
        for i in range(1, 6)
    ]

    # Extract Gram Panchayats from the assignments in the list
    assigned_gram_panchayats = [
        getattr(assignment, f'grampanchayat{i}', None)
        for i in range(1, 6)
        for assignment in assigned_gram_panchayat
    ]

    # Remove None values from the list
    assigned_gram_panchayats = [panchayat for panchayat in assigned_gram_panchayats if panchayat]

    # Query Gram Panchayats based on the assignments
    gram_panchayats = Grampanchayat.objects.filter(pk__in=assigned_gram_panchayats)

    if request.method == 'POST':
        camp_date = request.POST.get('campDate')
        camp_name = request.POST.get('campName')
        camp_address = request.POST.get('campAddress')
        conducted_by = request.POST.get('conductedBy')
        gram_panchayat = request.POST.get('gramPanchayat')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        start_time_2 = request.POST.get('startTime2')
        end_time_2 = request.POST.get('endTime2')

        # Create a new BloodCamp object
        blood_camp = BloodCamp.objects.create(
            campDate=camp_date,
            campName=camp_name,
            campAddress=camp_address,
            user=user,
            conductedBy=conducted_by,
            organizedBy=staff_member,
            gramPanchayat=gram_panchayat,
            startTime=start_time,
            endTime=end_time,
            startTime2=start_time_2,
            endTime2=end_time_2,
        )
        blood_camp.save()

        # Redirect to the staffindex page
        return redirect('staffindex')

    gram_panchayats_list = [{'name_of_grampanchayat': p.name_of_grampanchayat} for p in gram_panchayats]

    context = {
        'staff_assignments': staff_assignments,
        'gramPanchayats': gram_panchayats,
        'gramPanchayatsJson': gram_panchayats_list,
    }

    return render(request, 'staff/bloodbankcamps.html', context)

from django.http import JsonResponse

@login_required
def get_assigned_gram_panchayats(request):
    user = request.user
    staff_member = Staff.objects.get(user=user)

    # Query staff assignments for the logged-in staff member
    staff_assignment = AssignGrampanchayat.objects.filter(staff=staff_member).first()

    # Extract Gram Panchayats from the staff assignment
    assigned_gram_panchayats = [
        getattr(staff_assignment, f'grampanchayat{i}_id')
        for i in range(1, 6)
        if getattr(staff_assignment, f'grampanchayat{i}', None) is not None
    ]

    # Query Gram Panchayats based on the assignments
    gram_panchayats = Grampanchayat.objects.filter(pk__in=assigned_gram_panchayats)

    # Convert Gram Panchayats to JSON format
    assigned_panchayats_json = [{'name_of_grampanchayat': p.name_of_grampanchayat} for p in gram_panchayats]

    return JsonResponse(assigned_panchayats_json, safe=False)




from django.shortcuts import render
from .models import BloodCamp
def view_camp_schedules(request):
    camps = BloodCamp.objects.all()
    BloodCamp.objects.all().count()
    return render(request, 'staff/viewcampschedules.html', {'schedules': camps})


from django.shortcuts import render
from .models import BloodCamp
from datetime import date

def campviewadmin(request):
    # Assuming you want to retrieve all BloodCamp instances
    camp_schedules = BloodCamp.objects.all()
    today = date.today()

    context = {
        'camp_schedules': camp_schedules,
        'today': today,
    }


    return render(request, 'mainuser/departments.html', context)




from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, DonorDetails, BloodInventory, BloodType
from django.contrib import messages
from django.db.models import Sum

from django.db import transaction

def donateddetails(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Retrieve donor details
        date_of_donation = request.POST.get('date_of_donation')
        expiry_date = request.POST.get('expiry_date')
        sample_name = request.POST.get('sample_name')
        quantity = request.POST.get('quantity')

        # Check if the provided data is valid (you can add your validation logic)
        if date_of_donation and expiry_date and sample_name and quantity:
            try:
                quantity_ml = int(quantity) * 450
                units_donated = quantity_ml // 450

                # Use atomic transaction to ensure consistency
                with transaction.atomic():
                    # Update the appointment status to "Donated"
                    appointment.status = "DONATED"
                    appointment.save()

                    # Retrieve the BloodType instance based on the donor's blood group
                    blood_group = appointment.booked_by_donor.user.donor.blood_group
                    blood_type_instance = BloodType.objects.get(blood_type=blood_group)

                    # Retrieve or create the BloodInventory
                    blood_inventory, created = BloodInventory.objects.get_or_create(blood_type=blood_type_instance)
                    blood_inventory.quantity += units_donated
                    blood_inventory.save()

                    # Optionally, create a DonorDetails instance and save it to the database
                    # Only if you want to store the donor details
                    donor_details = DonorDetails(
                        appointment=appointment,
                        donor=appointment.booked_by_donor,
                        date_of_donation=date_of_donation,
                        expiry_date=expiry_date,
                        sample_name=sample_name,
                        quantity=quantity_ml,
                        # Add other fields as needed
                    )
                    donor_details.save()

            except ValueError:
                # Handle invalid quantity (non-integer) entered by the user
                return render(request, 'staff/filldonordetails.html', {'appointment': appointment, 'error_message': 'Invalid quantity entered'})

            return redirect('donorappointments')  # Redirect to the "Donor Appointments" page
        else:
            # Handle validation errors or show an error message
            # You can customize this part to display error messages to the user
            return render(request, 'staff/filldonordetails.html', {'appointment': appointment, 'error_message': 'Please fill in all required fields'})

    return render(request, 'staff/filldonordetails.html', {'appointment': appointment})








#new
from django.shortcuts import render
from .models import BloodInventory

def view_blood_inventory(request):
    blood_inventory = BloodInventory.objects.all()
    return render(request, 'mainuser/bloodinventory.html', {'blood_inventory': blood_inventory})


def check_appointment_status(request, appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        status = appointment.status if appointment.status else "Not Donated"
        return JsonResponse({"status": status})
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found"}, status=404)


from django.shortcuts import get_object_or_404, redirect, render
from .models import Appointment, NotDonatedReason
# Update your view to match the form field name
def notdonated(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Retrieve the reason for not donating from the form field
        reason = request.POST.get('notdonatedreason')  # Update field name to match the form

        if reason:
            not_donated_reason = NotDonatedReason(
                appointment=appointment,
                donor=appointment.booked_by_donor,
                reason=reason
            )
            not_donated_reason.save()

            appointment.status = "NOT DONATED"
            appointment.save()

            return redirect('donorappointments')
        else:
            return render(request, 'staff/notdonateddetails.html', {'appointment': appointment, 'error_message': 'Please provide a reason for not donating'})

    return render(request, 'staff/notdonateddetails.html', {'appointment': appointment})





def viewlabresults(request):
    return render(request, 'mainuser/viewlabresults.html')


from django.shortcuts import render
from .models import UploadedFile

def view_uploaded_files(request):
    uploaded_files = UploadedFile.objects.all()
    context = {'uploaded_files': uploaded_files}
    return render(request, 'mainuser/viewlabresults.html', context)


from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import UploadedFile

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    file_path = uploaded_file.file.path
    response = FileResponse(open(file_path, 'rb'))
    return response

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UploadedFile

@csrf_exempt  # Use csrf_exempt for simplicity in this example; in a real project, use a proper csrf protection method
def update_approval_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_id = data.get('fileId')
        new_status = data.get('newStatus')

        try:
            uploaded_file = UploadedFile.objects.get(pk=file_id)
            uploaded_file.approval_status = new_status
            uploaded_file.save()

            # Send email notification
            user_email = uploaded_file.user.email
            subject = 'Medlab Blood Bank : Lab Results Update'
            if new_status == 'Approved':
                # Include a link for booking a camp
                booking_link = 'https://example.com/book-camp'
                message = (
                    f'Congratulations! Your lab results have been {new_status.lower()}. '
                    f'We invite you to book a camp using the following link: {booking_link}'
                )
            elif new_status == 'Rejected':
                message = f'We regret to inform you that your lab results have been {new_status.lower()}.'
            else:
                message = f'Your lab results have been updated to {new_status.lower()}.'

           

            send_mail(subject, message, 'your_email@example.com', [user_email])

            return JsonResponse({'message': 'Approval status updated successfully.'})
        except UploadedFile.DoesNotExist:
            return JsonResponse({'message': 'File not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request.'}, status=400)



from django.shortcuts import render
from .models import BloodCamp


def campschedulesfordonor(request):
    current_date = timezone.now().date()  # Get the current date
    camps = BloodCamp.objects.filter(campDate__gte=current_date)  # Filter camps with campDate >= current_date
    return render(request, 'campschedulesfordonor.html', {'schedules': camps})

# def confirmpage(request):
#     return render(request,'confirmpage.html')
   
from django.shortcuts import render, redirect
from .models import BloodCamp, Appointment
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BloodCamp, Appointment

@login_required
def confirmpage(request):
    if request.method == 'POST':
        camp_id = request.POST.get('camp_id')
        time_slot = request.POST.get('time_slot')
        print(time_slot)
        # Get the donor who is logged in
        donor = request.user.donor

        # Retrieve the BloodCamp instance
        blood_camp = BloodCamp.objects.get(id=camp_id)

        # Create an Appointment instance
        appointment = Appointment(camp=blood_camp, time_slot=time_slot, booked_by_donor=donor)
        appointment.save()

        return render(request, 'confirmpage.html',{'appointment':appointment})

    # Handle other cases or methods if needed
    return redirect('homebloodbank')  # Redirect to the appropriate URL




from django.shortcuts import render
from .models import Appointment

def donorappointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'staff/donorappointments.html', {'appointments': appointments})


def donorsstaff(request):
    return render(request, 'staff/donorsstaff.html')


from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Payment


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def requestsent(request,blood_request_id):
     # Retrieve the appointment instance
    blood_request = BloodRequest.objects.get(id=blood_request_id)
    user=request.user
    currency = 'INR'
    amount = blood_request.amount  # Get the subscription price
    amount_in_paise = int(amount * 100)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args = [blood_request_id])

    # Create a Payment for the appointment
    payment = Payment.objects.create(
        user=request.user,
        payment_amount=amount,  # Specify the payment amount
        payment_status='Pending',
        razorpay_order_id=razorpay_order_id,
    )
    
    # Render the success template with the necessary context
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }
    return render(request,'hospital/requestsent.html', context=context)

from .models import BloodInventory, BloodType

@csrf_exempt
def paymenthandler(request, blood_request_id):
    user=request.user
    # print(blood_request_id)
    # unit=BloodRequest.objects.filter(user=user.id)
    # quantity=unit.quantity
    
    if request.method == "POST":
        try:
            # Get the payment details from the POST request
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            amount=request.POST.get('razorpay_amount', '')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,

            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

            if result is not None:
                amount = int(payment.payment_amount*100)  # Rs. 200

                # Capture the payment
                razorpay_client.payment.capture(payment_id, amount)
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                payment.payment_status='Success'
                payment.save()
                blood_request=BloodRequest.objects.get(id=blood_request_id)
                
                blood_request.status='Accepted'
                blood_request.save()

                # Save payment details to the Payment model
                # Assuming you have a Payment model defined

                # Subtract the requested quantity from the blood inventory
                blood_group = blood_request.blood_group
                quantity_units = blood_request.quantity
                blood_type = BloodType.objects.get(blood_type=blood_group)
                blood_inventory = BloodInventory.objects.get(blood_type=blood_type)
                quantity_ml = quantity_units * 450  # Convert units to milliliters
                blood_inventory.quantity -= quantity_ml
                blood_inventory.save()

                # Redirect to a success page with payment details
                return redirect('hospitalhome')  # Replace 'orders' with your actual success page name or URL
            else:
                # Signature verification failed
                return HttpResponse("Payment signature verification failed", status=400)
        except Exception as e:
            # Handle exceptions gracefully
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        # Handle non-POST requests
        return HttpResponse("Invalid request method", status=405)




from django.http import JsonResponse
from .models import BloodInventory, BloodType
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import datetime
from .models import BloodRequest, BloodInventory, BloodType

# def get_blood_quantity(request):
#     blood_group = request.GET.get('blood_group', '')
#     try:
#         blood_type = BloodType.objects.get(blood_type=blood_group)
#         blood_inventory = BloodInventory.objects.get(blood_type=blood_type)
#         quantity_units = blood_inventory.quantity // 450  # Convert milliliters to units
       
#         return JsonResponse({'quantity': quantity_units})
#     except BloodType.DoesNotExist:
#         return JsonResponse({'error': 'Blood type not found'}, status=404)
#     except BloodInventory.DoesNotExist:
#         return JsonResponse({'error': 'Blood inventory not found'}, status=404)
from django.http import JsonResponse
from .models import BloodInventory, BloodType

def get_blood_quantity(request):
    blood_group = request.GET.get('blood_group', '')
    try:
        blood_type = BloodType.objects.get(blood_type=blood_group)
        blood_inventory = BloodInventory.objects.get(blood_type=blood_type)
        quantity_units = blood_inventory.quantity // 450  # Convert milliliters to units
        max_quantity = quantity_units  # Set the max_quantity to the available quantity
       
        return JsonResponse({'quantity': quantity_units, 'max_quantity': max_quantity})
    except BloodType.DoesNotExist:
        return JsonResponse({'error': 'Blood type not found'}, status=404)
    except BloodInventory.DoesNotExist:
        return JsonResponse({'error': 'Blood inventory not found'}, status=404)



from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import datetime
from .models import BloodRequest
@csrf_exempt  # Use csrf_exempt for simplicity; consider proper CSRF protection in production
@login_required
def bloodrequest(request, is_immediate):
    if request.method == 'POST':
        user = request.user
        blood_group = request.POST.get('blood_group')
        purpose = request.POST.get('purpose')

        otp = get_random_string(length=6, allowed_chars='1234567890')
        print(f"OTP: {otp}")

        request.session['hospital_otp'] = otp

          # Store the 'quantity' in the session

        subject = 'Your OTP for Blood Request: Medlab Blood Bank'
        message = f'Your OTP is: {otp}'
        from_email = 'adhilaismail2@gmail.com'  # Replace with your email
        recipient_list = [user.email]  # Assuming you want to send the OTP to the user's email address

        # Use send_mail to send the OTP email
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        requested_date = datetime.now().date()
        requested_time = datetime.now().time()

        is_immediate = is_immediate.lower() == 'true'
        # Calculate the amount based on the quantity (units) requested
        quantity_units = int(request.POST.get('quantity', 0))
       
        calculated_amount = 850 * quantity_units

        
        
        blood_request = BloodRequest(
            user=user,
            blood_group=blood_group,
            quantity=quantity_units,
            purpose=purpose,
            requested_date=requested_date,
            requested_time=requested_time,
            is_immediate=is_immediate,
            amount=calculated_amount
        )
        blood_request.save()

        blood_request_id = blood_request.id

        url = reverse('verify_hospital', args=[blood_request_id])
        return redirect(url)

    return render(request, 'hospital/requestblood.html', {'is_immediate': is_immediate})


#laboratory


from django.shortcuts import render
from .models import LaboratoryTest

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def homelab(request):
    print("View function executed!")
    # Retrieve all LaboratoryTest objects from the database
    lab_tests = LaboratoryTest.objects.all()
    print("Number of records:", lab_tests.count())

    # Split lab_tests into chunks of 3
    paginator = Paginator(lab_tests, 3)
    
    # Get the current page from the request's GET parameters
    page = request.GET.get('page', 1)

    try:
        # Get the specified page
        lab_tests_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        lab_tests_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        lab_tests_page = paginator.page(paginator.num_pages)

    # Pass the lab_tests_page data to the template context
    context = {
        'lab_tests_page': lab_tests_page,
    }

    # Render the HTML template with the data
    return render(request, 'labhome.html', context)



def upload_prescription_view(request):
    return render(request, 'labhome.html')

def download_report_view(request):
    return render(request, 'labhome.html')



def find_lab_view(request):
    return render(request, 'labhome.html')






# admin laboratory

def laboratory(request):
    return render(request,'mainuser/labmainpage.html')

def laboratory_test_package_registration(request):
    return render(request,'mainuser/labmainpage.html')

def special_package_registration(request):
    return render(request,'mainuser/labmainpage.html')


def laboratory_test_package_registration(request):
    return render(request,'mainuser/labmainpage.html')

def special_package_registration(request):
    return render(request,'mainuser/labmainpage.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LaboratoryTest

@csrf_exempt
def save_laboratory_test(request):
    if request.method == 'POST':
        # Retrieve form data
        
        test_name = request.POST.get('labTestName')
        test_price = request.POST.get('labTestPrice')
        package_details_json = request.POST.get('packageDetails')

        try:
            # Parse JSON data
            package_details = json.loads(package_details_json)

            # Create a LaboratoryTest object and save it to the database
            laboratory_test = LaboratoryTest(
                test_name=test_name,
                test_price=test_price,
                package_details=package_details
            )
            laboratory_test.save()

            # Return a JSON response indicating success
            return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    elif request.method == 'GET':
        # Handle GET requests to display laboratory test data
        lab_tests = LaboratoryTest.objects.all()
        context = {'lab_tests': lab_tests}
        return render(request, 'labhome.html', context)
    else:
        # Handle other request methods (e.g., PUT, DELETE) if needed
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



from django.shortcuts import render
from .models import LaboratoryTest

def show_lab_tests(request):
    # Retrieve all LaboratoryTest objects from the database
    lab_tests = LaboratoryTest.objects.all()
    print("Number of records:", lab_tests.count())  # Add this line to print the count

    # Pass the lab_tests data to the template context
    context = {
        'lab_tests': lab_tests,
    }

    # Render the HTML template with the data
    return render(request, 'labhome.html', context)


from django.shortcuts import render, get_object_or_404
from .models import LaboratoryTest

def show_test_details(request, test_id):
    # Retrieve the specific LaboratoryTest object using the test_id
    lab_test = get_object_or_404(LaboratoryTest, pk=test_id)

    # Pass the lab_test data to the template context
    context = {
        'lab_test': lab_test,
    }

    # Render the HTML template with the data
    return render(request, 'test_details.html', context)

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Patient, Booking, LaboratoryTest

def book_now(request, test_id, test_name, test_price):
    # Add any logic for the "Book Now" view

    # Pass the test details to the template context
    context = {
        'test_id': test_id,
        'test_name': test_name,
        'test_price': test_price,
    }
    # Render the book_now.html template with the test details
    return render(request, 'book_now.html', context)



# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Patient, Booking, LaboratoryTest


def submit_booking(request):
    if request.method == 'POST':
        user_id = request.user.id
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        selected_test_id = request.POST.get('selected_test') # Assuming the field name is 'selected_test' in the form

        # Save the patient details to the database
        patient = Patient.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            gender=gender,
            date_of_birth=date_of_birth,
            selected_test_id=selected_test_id,user_id=user_id
        )

        # Create a Booking object
        Booking.objects.create(patient=patient)

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # If the request method is not POST, render the booking form
    lab_tests = LaboratoryTest.objects.all()
    return render(request, 'booking_form.html', {'success': False, 'lab_tests': lab_tests})

from django.shortcuts import render
from .models import Patient, Booking

def labtestbookings(request):
    appointments = Booking.objects.all()
    test_name= Patient.objects

    # Pass data to the template
    context = {'appointments': appointments}
    
    # Render the template
    return render(request, 'labstaff/viewbookings.html', context)
    
def labstaffindex(request):
    return render(request,'labstaff/index.html')


import logging
from django.shortcuts import render
from .models import Booking, Patient
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

@login_required
def viewtestbookings(request):
    
    patient = request.user.id
        # Retrieve bookings for the patient
    bookings=[]
    variable=Patient.objects.filter(user_id=patient)
    print(variable)
    print("Hello")
    for i in variable:
        bookings.extend(Booking.objects.filter(patient_id=i.id))
    
    print(bookings)
    current_time = timezone.now()

        # Debugging: Log the bookings
    for booking in bookings:
        time_difference = booking.booked_date - current_time
        booking.is_cancelable = time_difference.total_seconds() > 0 and time_difference.total_seconds() < 86400

        # logger.debug(f"Booking for {booking.patient.full_name} on {booking.booked_date}")
        
        # Pass the bookings to the template context
    context = {'bookings': bookings}

        # Handle the case where there is no patient associated with the user

    return render(request, 'viewtestbookings.html', context)


# views.py



