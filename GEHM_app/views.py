from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from GEHM_app.forms import UserReg, ContractorForm, GuestForm


# Create your views here.

def home(request):
    return render(request,'index.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminindex')
            elif  user.is_contractors:
                return redirect('con_base')
            elif  user.is_guestemp:
                return redirect('guest_emp_index')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request,'login.html')

def registerpage(request):
    u_form=UserReg()
    c_form=ContractorForm()
    if request.method=='POST':
        u_form=UserReg(request.POST)
        c_form=ContractorForm(request.POST,request.FILES)
        if u_form.is_valid() and c_form.is_valid():
            user=u_form.save(commit=False)
            user.is_contractors=True
            user.save()
            contractor=c_form.save(commit=False)
            contractor.user=user
            contractor.save()
            messages.info(request,'Contractor Registered Succesfully')
            return redirect('loginpage')
    return render(request,'register.html',{'u_form':u_form,'c_form':c_form})

def guestreg(request):
    u_form=UserReg()
    g_form=GuestForm()
    if request.method=='POST':
        u_form=UserReg(request.POST)
        g_form=GuestForm(request.POST,request.FILES)
        if u_form.is_valid() and g_form.is_valid():
            user=u_form.save(commit=False)
            user.is_guestemp=True
            user.save()
            Guest=g_form.save(commit=False)
            Guest.user=user
            Guest.save()
            messages.info(request,'Guest Employee Registered Succesfully')
            return redirect('loginpage')
    return render(request,'guestreg.html',{'u_form':u_form,'g_form':g_form})


def adminindex(request):
    return render(request,'adminindex.html')

def conctracor_index(request):
    return render(request,'contractors.html')

def guest_emp_index(request):
    return render(request,'guest_emp.html')

def logout_view(request):
    logout(request)
    return redirect('loginpage')