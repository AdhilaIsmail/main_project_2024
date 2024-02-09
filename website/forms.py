from django import forms

from .models import Donor

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['full_name', 'email', 'phone', 'blood_group', 'place', 'id_proof']
        

from .models import DonorResponse

class DonorForm(forms.ModelForm):
    class Meta:
        model = DonorResponse
        fields = '__all__'
       
    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        weight = cleaned_data.get('weight')
        # donorHistory = cleaned_data.get('donorHistory')
        difficulty = cleaned_data.get('difficulty')
        donated = cleaned_data.get('donated')
        allergies = cleaned_data.get('allergies')
        alcohol = cleaned_data.get('alcohol')
        jail = cleaned_data.get('jail')
        surgery = cleaned_data.get('surgery')
        diseased = cleaned_data.get('diseased')
        hivaids = cleaned_data.get('hivaids')
        pregnant = cleaned_data.get('pregnant')
        child = cleaned_data.get('child')
        feelgood = cleaned_data.get('feelgood')

        if not 18 <= age <= 65:
            raise forms.ValidationError("Age must be between 18 and 65.")
        
        if weight < 45:
            raise forms.ValidationError("Weight must be 45 or more.")

        # Add additional checks for other fields here
        # if donorHistory != 'yes' or donorHistory != 'no':
        #     raise forms.ValidationError("Donor history must be 'yes' or 'no'.")

        if difficulty != 'no':
            raise forms.ValidationError("Difficulty must be 'no'.")

        if donated != 'no':
            raise forms.ValidationError("Donated must be 'no'.")

        if allergies != 'no':
            raise forms.ValidationError("Allergies must be 'no'.")

        if alcohol != 'no':
            raise forms.ValidationError("Alcohol must be 'no'.")

        if jail != 'no':
            raise forms.ValidationError("Jail must be 'no'.")

        if surgery != 'no':
            raise forms.ValidationError("Surgery must be 'no'.")

        if diseased != 'no':
            raise forms.ValidationError("Diseased must be 'no'.")

        if hivaids != 'no':
            raise forms.ValidationError("HIV/AIDS must be 'no'.")

        if pregnant != 'no':
            raise forms.ValidationError("Pregnant must be 'no'.")

        if child != 'no':
            raise forms.ValidationError("Child must be 'no'.")

        if feelgood != 'no':
            raise forms.ValidationError("Feelgood must be 'no'.")
        
# from django import forms

# class UploadFileForm(forms.Form):
#     result_file = forms.FileField(
#         label='Select a file',
#         help_text='<small><br><br>Allowed file types: PDF, DOC, DOCX</small>',
       
#     )

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UploadFileForm(forms.Form):
    ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx']

    result_file = forms.FileField(
        label='Select a file',
        help_text='<small><br><br>Allowed file types: PDF, DOC, DOCX</small>',
    )

    def clean_result_file(self):
        uploaded_file = self.cleaned_data['result_file']
        extension = uploaded_file.name.split('.')[-1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValidationError(_('Invalid file type. Please upload a PDF, DOC, or DOCX file.'))

        return uploaded_file

# from django import forms
# from .models import HospitalRegister

# class HospitalForm(forms.ModelForm):
#     class Meta:
#         model = HospitalRegister
#         fields = '__all__'  # You can specify fields explicitly if needed
# from django import forms
# from .models import HospitalRegister

# class HospitalRegisterForm(forms.ModelForm):
#     class Meta:
#         model = HospitalRegister
#         fields = '__all__'  # Include all fields from the model


# forms.py

from django import forms
from .models import BloodType

class BloodTypeForm(forms.ModelForm):
    class Meta:
        model = BloodType
        fields = ['blood_type']



