from django import forms
from crm.models import Employee
from django.contrib.auth.models import User

class EmployeeForm(forms.Form):
    name=forms.CharField()
    department=forms.CharField()
    salary=forms.IntegerField()
    email=forms.EmailField()
    age=forms.IntegerField()
    contact=forms.CharField()
    
class EmpoyeeModelForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields="__all__"

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "department":forms.TextInput(attrs={"class":"form-control"}),
            "salary":forms.NumberInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "age":forms.NumberInput(attrs={"class":"form-control"}),
            "contact":forms.Textarea(attrs={"class":"form-control","row":5}),
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-conrol"})
        }


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

