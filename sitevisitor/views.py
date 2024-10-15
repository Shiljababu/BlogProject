from django.shortcuts import redirect, render
from adminpanel.models import Profile, User
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ForgotForm, ResetForm, Forgot_otp_Form, OtpForm, ProfileForm
from django.contrib.auth import authenticate, login


# create a function for sitehome
def sitehome(request):
    # Show the 'site_home.html' page to the user.
    return render(request, 'sitevisitor/site_home.html')

# create a function for user login
def site_login(request):
    # Check if the user has submitted the login form.
    if request.method =='POST':
        # Create a form with the submitted data.
        form = LoginForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the username and password from the form.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Check if the username and password match any user.
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_staff:  
                    # If the user is found, log them in.
                    login(request, user)
                    # Send the user to their home page.
                    return redirect('userhome')
                else:
                    # If the login details are wrong, show an error.
                    messages.error(request, 'This user is not authorized')
                
                    # Stay on the login page.
                    
                    return redirect('site_login')
            else:
                messages.error(request, 'Invalid Username or password!!!')
    else:
        # If it’s not a POST request, show the login form.
        form = LoginForm()
    # Show the 'site_login.html' page with the form.
    return render(request, 'sitevisitor/site_login.html', {'form':form})


# This function handles user registration.
def register(request):
    # Check if the request is a POST request (form submission).
    if request.method == 'POST':
        # Create forms with the data sent from the user.
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        # Check if both forms have valid data.
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user information from the user form.
            user = user_form.save()
            # Get the email from the form and save it to the user.
            user.email = user_form.cleaned_data.get('email')
            user.save()

            # Create the profile object but don't save it yet.
            profile = profile_form.save(commit=False)
            # Link the profile to the user.
            profile.user = user
            # Save the profile to the database.
            profile.save()

            # Log in the user after successful registration.
            login(request, user)
            # Show a success message.
            messages.success(request, 'Successfully registered')
            # Redirect to the login page.
            return redirect('site_login')
        else:
            # Show an error message if forms are not valid.
            messages.error(request, 'unsuccessful')
    else:
        # Create empty forms if not a POST request (initial page load).
        user_form = RegistrationForm()
        profile_form = ProfileForm()

    # Render the registration page with the forms.
    return render(request, 'sitevisitor/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# This function handles forgotten passwords.
def forgot(request):
    # Check if the user has submitted the forgot password form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = ForgotForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the email from the form.
            email = form.cleaned_data.get('email')
            # Check if a user with that email exists.
            if User.objects.filter(email=email).exists():
                # Show a success message if the email is found.
                messages.success(request, 'Instructions to reset your password has been sent to your email')
                # Send the user to the reset page.
                return redirect('reset')
            else:
                # Show an error if the email is not found.
                messages.error(request, 'This email id does not exist!!!')
                # Stay on the forgot password page.
                return redirect('forgot')
    else:
        # If it’s not a POST request, show the forgot password form.
        form = ForgotForm()
    # Show the 'forgot_pass.html' page with the form.
    return render(request, 'sitevisitor/forgot_pass.html', {'form':form})


# This function handles resetting passwords.
def reset(request):
    # Check if the user has submitted the reset password form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = ResetForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the username and new passwords from the form.
            username = form.cleaned_data.get('username')
            new_password3 = form.cleaned_data.get('password3')
            new_password4 = form.cleaned_data.get('password4')

            # Check if the new passwords match.
            if new_password3 != new_password4:
                # Show an error if the passwords don't match.
                form.add_error('password4', 'Passwords do not match.')
            else:
                try:
                    # Try to find the user with the given username.
                    user = User.objects.get(username=username)
                    # Set the new password for the user.
                    user.set_password(new_password3)
                    user.save()
                    # Show a success message.
                    messages.success(request, 'Your password has been updated successfully.')
                    # Send the user to the login page.
                    return redirect('site_login')
                except User.DoesNotExist:
                    # Show an error if the user is not found.
                    form.add_error('username', 'User does not exist.')
        else:
            # Show an error if the form has mistakes.
            messages.error(request, 'Please correct the errors below.')
    else:
        # If it’s not a POST request, show the reset form.
        form = ResetForm()
    # Show the 'reset.html' page with the form.
    return render(request, 'sitevisitor/reset.html', {'form': form})


# This function handles forgotten phone numbers.
def forgot_phone(request):
    # Check if the user has submitted the forgot phone form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = Forgot_otp_Form(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the phone number from the form.
            phone_number = form.cleaned_data.get('phone_number')
            # Check if a profile with that phone number exists.
            if Profile.objects.filter(phone=phone_number).exists():
                # Show a success message if the phone number is found.
                messages.success(request, 'Instructions to reset your password has been sent to your email')
                # Send the user to the reset page.
                return redirect('reset')
            else:
                # Show an error if the phone number is not found.
                messages.error(request, 'This phone number does not exist!!!')
                # Stay on the forgot phone page.
                return redirect('forgot_phone')
    else:
        # If it’s not a POST request, show the forgot phone form.
        form = Forgot_otp_Form()
    # Show the 'forgot_phone.html' page with the form.
    return render(request, 'sitevisitor/forgot_phone.html', {'form': form})


# This function handles OTP (One Time Password) verification.
def site_otp(request):
    # Check if the user has submitted the OTP form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = OtpForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the OTP from the form.
            otp = form.cleaned_data.get('otp')
            # Retrieve the stored OTP from the session.
            stored_otp = request.session.get('otp')
            # Check if the entered OTP matches the stored OTP.
            if otp == stored_otp:
                # Show a success message if the OTP is correct.
                messages.success(request, 'OTP verified successfully!')
                # Redirect to a desired page after successful verification.
                return redirect('desired_redirect_url')
            else:
                # Show an error if the OTP is incorrect.
                messages.error(request, 'Invalid OTP. Please try again.')
                # Stay on the OTP page.
                return redirect('site_otp')
    else:
        # If it’s not a POST request, show the OTP form.
        form = OtpForm()
    # Show the 'site_otp.html' page with the form.
    return render(request, 'sitevisitor/site_otp.html', {'form':form})


# This function shows an error page.
def error_page(request):
    # Show the '404.html' error page.
    return render(request, 'sitevisitor/404.html')