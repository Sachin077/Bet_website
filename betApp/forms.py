from django.forms import ModelForm
from betApp.models import *
from django.contrib.auth.models import User
from django.utils import timezone

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
            ]
