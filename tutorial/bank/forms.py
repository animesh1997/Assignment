from django.contrib.auth.models import User
from django import forms

class UserFormUp(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirmpassword=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=["username","password","confirmpassword","email"]



class UserFormIn(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=["username","password"]