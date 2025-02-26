from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Veriffication email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]                      # We make username itself, by taking email first_value only it is username for user.

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number          # yaha alag se isleye add kara kyuki create_user function me phone number field nahi h.
            user.save()

            # USER MAIL ACTIVATION
            current_site = get_current_site(request)                           # here is to check user is in which domain.
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {   # -> settings.py(SMTP Configuration) -> 32-44  
                'user': user,                                                          # -> import function at top -> account_verification_email.html
                'domain': current_site,                                                # -> activate() handle the logic.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),          # Here we encode our primary key with the help of 'urlsafe_base64_encode' this function.
                'token': default_token_generator.make_token(user),            # default_token_generator --> it generate the token, and it make the token for specified user
            })
            to_email = email                                                  # Here we extract user mail where we need to send activation link.
            send_email = EmailMessage(mail_subject, message, to=[to_email])   # Here we describe what should be send in email.
            send_email.send()                                                 # Here w send it.
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)  # ye check kar raha h ki user verification karke a raha h toh ye check karega ki request verification emal se he a rhi h.
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)                               # simple it login.
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)                                            # simple it logout.
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)                        # Get the user
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):    # Here we check receive token is avlid or not.
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    

@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            # Reset password email
            current_site = get_current_site(request)                                  # here is to check user is in which domain.
            mail_subject = 'Please reset your Password.'
            message = render_to_string('accounts/reset_password_email.html', {   # -> settings.py(SMTP Configuration) -> 32-44  
                'user': user,                                                          # -> import function at top -> reset_password_email.html
                'domain': current_site,                                                # -> activate() handle the logic.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),          # Here we encode our primary key with the help of 'urlsafe_base64_encode' this function.
                'token': default_token_generator.make_token(user),            # default_token_generator --> it generate the token, and it make the token for specified user
            })
            to_email = email                                                  # Here we extract user mail where we need to send activation link.
            send_email = EmailMessage(mail_subject, message, to=[to_email])   # Here we describe what should be send in email.
            send_email.send()                                                 # Here we send it

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
        
    else:
        return render(request, 'accounts/resetPassword.html')
   