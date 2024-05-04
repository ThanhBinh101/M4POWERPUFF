from django import forms

class UserForm(forms.Form):
    gmail = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    date = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=100)
    years = forms.DecimalField(max_digits=10)