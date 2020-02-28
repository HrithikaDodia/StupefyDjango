from django import forms
from django.conf import settings
from .models import TwoFAUser

class BootstrapInput(forms.TextInput):
    def __init__(self, placeholder, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapInput, self).__init__(attrs={
            'class': 'form-control input-sm',
            'placeholder': placeholder
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapInput, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class BootstrapPasswordInput(BootstrapInput):
    input_type = 'password'
    template_name = 'django/forms/widgets/password.html'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = TwoFAUser
        fields = ('username', 'email', 'password','phonenumber')
        widgets = {
            'username': BootstrapInput('User Name'),
            'email': BootstrapInput('Email Address'),
            'phonenumber': BootstrapInput('Phone Number'),
            'password': BootstrapPasswordInput('Password', size=6),
        }

    
    def clean_username(self):
        username = self.cleaned_data['username']
        if TwoFAUser.objects.filter(username=username).exists():
            self.add_error('username', 'Username is already taken')
        return username



        