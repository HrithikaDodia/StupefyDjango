from django.conf import settings
from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail

from .forms import RegistrationForm
from .models import TwoFAUser

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            twofa_user = TwoFAUser.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['phonenumber'],
                form.cleaned_data['password']
                )
            login(request, twofa_user)
            # subject = 'Thank You For Signing Up'
            # from_email = settings.EMAIL_HOST_USER
            # message = 'Thank You {} for joining our holiday club'.format(twofa_user.username)
            # mail_sent = send_mail(subject,message,from_email,[twofa_user.email],fail_silently=False)
            return redirect('index')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


