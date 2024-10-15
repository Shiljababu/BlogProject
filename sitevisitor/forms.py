from django import forms
from adminpanel.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# This form is used to register a new user.
class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your Name'
        }))
    
     # Create a field for the email address
    email = forms.EmailField(label='email',widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your email'
        }))
    
    # Create a field for the first password
    password1 = forms.CharField(label='password1',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your password'
        }))
    
    # Create a field for the 2nd password
    password2 = forms.CharField(label='password2',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm your password'
        }))
    
    #Tell the form which model it should use.
    class Meta:
        model = User
       # Include these fields in the form.
        fields = ['username','email','password1','password2']
        
class ProfileForm(forms.ModelForm):
   

    # Field for the phone number
    phone = forms.IntegerField(label='Phone Number', widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    # Field for the profile description (not required)
    profile_description = forms.CharField(label='Description', widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Say about you'
        }), 
        required=False
    )

    # Field for the email (not required)
    

    # Field for the profile image (not required)
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your profile image'
        }), 
        required=False
    )

    # Field for the ID proof image (not required)
    id_proof = forms.ImageField(label='ID Proof', widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your ID proof image'
        }), 
        required=False
    )

    # Connected to the Profile model and choose which fields to use
    class Meta:
        model = Profile
        fields = [ 'phone', 'profile_description', 'profile_image', 'id_proof']



# This form is used for users to log in
class LoginForm(forms.Form):
    # Create a field for the username
    username = forms.CharField(label = 'Username', max_length = 100, required = True, widget = forms.TextInput(attrs = {
        'class':'form-control', 'placeholder':'Enter the username'
    }))

    # Create a field for the password
    password = forms.CharField(label = 'password', max_length = 100, required =True, widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':'Enter the password'
    }))

    # Tell the form which model it should use.
    class Meta:
        model = User
        # Include these fields in the form
        fields = ['username','email','password']

# This form is used if a user forgets their password and needs to get a new one.
class ForgotForm(forms.Form):
    # Create a field for the email address
    email = forms.EmailField(label = 'Email', max_length = 100, required = True, widget = forms.TextInput(attrs={
        'class':'form-control','placeholder':'Enter the Email address'
    }))

    # Tell the form which model it should use.
    class Meta:
        model = User
        # Include the email field in the form.
        fields = ['email']

# This form is used to reset a forgotten password.
class ResetForm(forms.Form):
    # Create a field for the username
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))

    # Create a field for the password 1
    password3 = forms.CharField(label='password3',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your new password'
        }))
    
    # Create a field for the password2
    password4 = forms.CharField(label='password4',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm your password'
        }))
    

    class Meta:
         # Include these fields in the form.
        fields = ['username','password3', 'password4']

# This form is used to handle phone numbers 
class Forgot_otp_Form(forms.Form):
    # Create a field for the phone number
    phone_number = forms.CharField(label = 'phone_number', max_length = 10, required = True, widget = forms.TextInput(attrs={
        'class':'form-control','placeholder':'Enter the Phone Number'
    }))

     # Tell the form which model it should use
    class Meta:
        model = Profile
        # Include the phone number field in the form.
        fields = ['phone_number']

# This form is used to enter an OTP
class OtpForm(forms.Form):
     # Create a field for the OTP
    otp = forms.CharField(label='Enter OTP', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter OTP'
    }))

    # Tell the form which model it should use.
    class Meta:
        model = Profile
        # Include the phone number field in the form.
        fields = ['phone_number']









