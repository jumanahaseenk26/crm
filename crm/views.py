from django.shortcuts import render,redirect
from crm.forms import *
from django.views.generic import View
from django.contrib import messages
from crm.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmpoyeeModelForm()
        return render(request,"emp_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=EmpoyeeModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"new employee created")
           # Employee.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"An error on adding new employee")
            return render(request,"emp_add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        departments=Employee.objects.all().values_list("department",flat=True).distinct()
        print(departments)
        if "department" in request.GET:
            dept=request.GET.get("department")
            qs=qs.filter(department__iexact=dept)
        return render(request,"emp_list.html",{"data":qs,"departments":departments})
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employee.objects.filter(name__icontains=name)
        return render(request,"emp_list.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")    
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        return render(request,"emp_details.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employee.objects.get(id=id).delete()
        messages.success(request,"successfully deleted")
        return redirect("emp-all")

@method_decorator(signin_required,name="dispatch")    
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employee.objects.get(id=id)
        form=EmpoyeeModelForm(instance=obj)
        return render(request,"emp_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employee.objects.get(id=id)
        form=EmpoyeeModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"succesfully update employee")
            return redirect("emp-details",pk=id)
        else:
            messages.error(request,"failed to update employee")
            return render(request,"emp_edit.html",{"form":form})

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"created")
            return render(request,"register.html",{"form":form})
        else:
             messages.error(request,"failed")
             return render(request,"register.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(user_name,pwd)
            user_obj=authenticate(request,username=user_name,password=pwd)
            if user_obj:
                print("valid")
                login(request,user_obj)
                return redirect("emp-all")
        else:
             messages.error(request,"invalid credentil")
             return render(request,"login.html",{"form":form})

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


