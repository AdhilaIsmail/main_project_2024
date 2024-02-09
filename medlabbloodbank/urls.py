"""
URL configuration for medlabbloodbank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from website import views
from django.http import HttpResponse
from website.views import index, about,  service, testimonial, contact, loginn, register_donor, donatenow, registerasdonor
from website.views import registereddonorresponse, registereddonortodonatenow, notificationfordonation, send_sms, uploadresult, uploadresult2
from website.views import homebloodbank, register, loggout
from django.contrib.auth import views as auth_views
from website.views import adminindex, activities, appointments, donors, departments, employees, profile1, editprofile,requestsent,campschedulesfordonor,confirmpage,donorappointments,bloodinventorystaff,registeredstafftablelab
from website.views import registereddonortable, search_by_name, search_by_place, search_by_blood_group, addhospitals, hospitalregistration,waitforemail,view_uploaded_files,viewlabresults
from website.views import hospital_registration, registeredhospitaltable, bloodrequest, registeredstafftable, staff_registration,getlaboratories,send_confirmation_email,download_file, get_assigned_gram_panchayats
from website.views import addnewgroup, addblood, requests, requestblood,donorappointments,hospitalhome, bloodavailability, hospitalabout, blood_request_list, verify_hospital, staffindex,validate_assign_grampanchayat,blood_inventory
from website.views import registereddonortablestaff, bloodbankcamps, assign_staff, listgps, addgps, grampanchayat_registration, grampanchayat_list,addlab,update_status,create_blood_camp,view_camp_schedules,update_approval_status
from website.views import homelab,upload_prescription_view,download_report_view,find_lab_view,laboratory,laboratory_test_package_registration,special_package_registration,save_laboratory_test,show_lab_tests,show_test_details,book_now,submit_booking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',index, name='index'),
    path('about',about, name='about'),
    path('service',service, name='service'),
    path('testimonial',testimonial, name='testimonial'),
    path('contact',contact, name='contact'),
    path('loginn', loginn, name='loginn'),
    path('registerasdonor',registerasdonor, name='registerasdonor'),
    path('register_donor/', register_donor, name='register_donor'),
    path('donatenow',donatenow, name='donatenow'),
    path('homebloodbank',homebloodbank, name='homebloodbank'),
    path('homelab/',homelab,name='homelab'),
    path('show_lab_tests/', show_lab_tests, name='show_lab_tests'),
    path('show_lab_tests/', show_lab_tests, name='show_lab_tests'),
    path('show_test_details/<int:test_id>/', show_test_details, name='show_test_details'),
    path('booking_form/', views.submit_booking, name='booking_form'),
    path('book_now/<str:test_name>/<test_price>/', views.book_now, name='book_now'),
    path('submit_booking/', submit_booking, name='submit_booking'),
    path('test/', lambda request: HttpResponse("Test view"), name='test_view'),
    path('registration',register, name='registration'),
    path('register/', register_donor, name='register_donor'),
    path('registereddonortodonatenow', registereddonortodonatenow, name='registereddonortodonatenow'),
    path('registereddonorresponse/', registereddonorresponse, name='registereddonorresponse'),
    path('notificationfordonation', notificationfordonation, name='notificationfordonation'),
    path('getlaboratories',getlaboratories,name='getlaboratories'),
    path('send_sms/', send_sms, name='send_sms'),
    path('uploadresult', uploadresult, name='uploadresult'),
    path('uploadresult2/<str:lab_selection_timestamp>/', uploadresult2, name='uploadresult2'),
    path('waitforemail',waitforemail,name='waitforemail'),
    path('confirmpage', confirmpage, name='confirmpage'),
    path('upload_prescription_view',upload_prescription_view, name='upload_prescription_view'),
    path('download_report_view', download_report_view,name='download_report_view'),
    path('find_lab_view',find_lab_view,name='find_lab_view'),
    path('labtestbookings',views.labtestbookings, name='labtestbookings'),
    path('labstaffindex',views.labstaffindex,name='labstaffindex'),
   

    # path('uploadresult2/<path:lab_selection_timestamp>/', uploadresult2, name='uploadresult2'),
    path('loggout', loggout, name='loggout'),
    path("",include("allauth.urls")),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    


    #admindashboard
    path('adminindex', adminindex, name='adminindex'),
    path('activities', activities, name='activities'),
    path('appointments', appointments, name='appointments'),
    path('departments', departments, name='departments'),
    path('donors', donors, name='donors'),
    path('employees', employees, name='employees'), 
    path('profile1', profile1, name='profile1'),
    path('editprofile', editprofile, name='editprofile'),
    path('registereddonortable', registereddonortable, name='registereddonortable'),
    path('registeredstafftablelab', registeredstafftablelab, name='registeredstafftablelab'),
    path('addhospitals', addhospitals, name='addhospitals'),
    path('hospitalregistration', hospitalregistration, name='hospitalregistration'),
    path('hospital-registration/', hospital_registration, name='hospital_registration'),
    path('registeredstafftable/', registeredstafftable, name='registeredstafftable'),
    path('search-by-name/', search_by_name, name='search_by_name'),
    path('search-by-place/', search_by_place, name='search_by_place'),
    path('search-by-blood-group/', search_by_blood_group, name='search_by_blood_group'),
    path('registeredhospitaltable/', registeredhospitaltable, name='registeredhospitaltable'),
    path('bloodinventory/', blood_inventory, name='blood_inventory'),
    path('view_detailed_details/<str:blood_type>/', views.view_detailed_details, name='view_detailed_details'),
    path('view_detailed_details/', views.handle_empty_blood_type, name='handle_empty_blood_type'),
    path('campviewadmin', views.campviewadmin, name='campviewadmin'),

    path('laboratory', laboratory, name='laboratory'),
    path('save_laboratory_test/', save_laboratory_test, name='save_laboratory_test'),
    path('laboratory_test_package_registration',laboratory_test_package_registration,name='laboratory_test_package_registration'),
    path('special_package_registration',special_package_registration,name='special_package_registration'),
    # path('add_test_details',add_test_details,name='add_test_details'),
    path('addnewgroup', addnewgroup, name='addnewgroup'),
    path('addblood/', addblood, name='addblood'),
    path('requests', requests, name='requests'),
    path('blood_request_list', blood_request_list, name='blood_request_list'),
    path('staff_registration', staff_registration, name='staff_registration'),
    path('assign_staff', assign_staff, name='assign_staff'),
    path('listgps', listgps, name='listgps' ),
    path('addgps', addgps, name='addgps' ),
    path('grampanchayat_registration', grampanchayat_registration, name='grampanchayat_registration' ),
    path('validate-assign-grampanchayat/', validate_assign_grampanchayat, name='validate_assign_grampanchayat'),
    path('api/grampanchayats/', grampanchayat_list, name='grampanchayat_list'),
    path('edit_grampanchayat/<int:pk>/', views.edit_grampanchayat, name='edit_grampanchayat'),
    path('addlab',addlab,name='addlab'),
    path('update_status/', update_status, name='update_status'),
    path('send_confirmation_email',send_confirmation_email,name='send_confirmation_email'),
    path('uploaded_files/', view_uploaded_files, name='view_uploaded_files'),
    path('download_file/<int:file_id>/', download_file, name='download_file'),
    path('viewlabresults', viewlabresults, name='viewlabresults'),
    path('update_approval_status',update_approval_status,name='update_approval_status'),

   
    
    #hospital
    path('hospitalhome', hospitalhome, name='hospitalhome'),
    path('requestblood', requestblood, name='requestblood'),  
    path('bloodavailability', bloodavailability, name='bloodavailability'),
    path('hospitalabout', hospitalabout, name='hospitalabout'),
    path('bloodrequest/<str:is_immediate>/', bloodrequest, name='bloodrequest'),
    path('verify_hospital/<int:blood_request_id>/', verify_hospital, name='verify_hospital'),

    path('requestsent/<int:blood_request_id>/', requestsent, name='requestsent'),
    path('get_blood_quantity/', views.get_blood_quantity, name='get_blood_quantity'),
  
    #staff

    path('staffindex', staffindex, name='staffindex'),
    path('donorsstaff',views.donorsstaff,name='donorsstaff'),
    path('activities', activities, name='activities'),
    path('donorappointments', donorappointments, name='donorappointments'),
    path('bloodbankcamps', bloodbankcamps, name='bloodbankcamps'),
    path('bloodinventorystaff',bloodinventorystaff,name="bloodinventorystaff"),
    # path('blood_inventory/', views.blood_inventory_view, name='blood_inventory'),
    path('staffliat', views.stafflist, name='stafflist'),
    path('profile1', profile1, name='profile1'),
    path('editprofile', editprofile, name='editprofile'),
    path('registereddonortablestaff', registereddonortablestaff, name='registereddonortablestaff'),
    path('addhospitals', addhospitals, name='addhospitals'),
    path('search-by-name/', search_by_name, name='search_by_name'),
    path('search-by-place/', search_by_place, name='search_by_place'),
    path('search-by-blood-group/', search_by_blood_group, name='search_by_blood_group'),
    path('registeredstafftable/', registeredstafftable, name='registeredstafftable'),
    path('addnewgroup', addnewgroup, name='addnewgroup'),
    path('addblood/', addblood, name='addblood'),
    path('blood_request_list', blood_request_list, name='blood_request_list'),
    path('create_blood_camp',create_blood_camp,name='create_blood_camp'),
    path('view_camp_schedules', view_camp_schedules, name='view_camp_schedules'),
    path('campschedulesfordonor', campschedulesfordonor, name='campschedulesfordonor'),
    path('get_assigned_gram_panchayats', get_assigned_gram_panchayats, name='get_assigned_gram_panchayats'),
    path('donorappointments',donorappointments, name='donorappointments'),
    path('paymenthandler/<int:blood_request_id>/', views.paymenthandler, name='paymenthandler'),
    path('donateddetails/<int:appointment_id>/', views.donateddetails, name='donateddetails'),
    path('notdonated/<int:appointment_id>/', views.notdonated, name='notdonated'),
    path('check-appointment-status/<int:appointment_id>/', views.check_appointment_status, name='check_appointment_status'),
    
    path('view_profile/', views.view_profile, name='view_profile'),
]
