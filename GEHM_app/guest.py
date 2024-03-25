from django.contrib import messages
from django.shortcuts import render, redirect

from GEHM_app.forms import FeedbackForm, ChatFormGUE
from GEHM_app.models import Contractor, Job, Enquiry, CHAT_GUE


def view_contra(request):
    data = Contractor.objects.all()
    return render(request,'view_contra.html',{'data':data})

def view_job_guest(request):
    data = Job.objects.all()
    return render(request,'view_job_guest.html',{'data':data})

def Enquiry_add(request):
    form = FeedbackForm()
    u = request.user
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('Enquiry_view')
    return render(request, 'Enquiry_add.html', {'form': form})

def Enquiry_view(request):
    f = Enquiry.objects.filter(user=request.user)
    return render(request, 'Enquiry_view.html', {'feedback': f})

def chat_add_gue(request):
    form = ChatFormGUE()
    u = request.user
    if request.method == 'POST':
        form = ChatFormGUE(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view_gue')
    else:
        form = ChatFormGUE()
    return render(request,'chat_add_gue.html',{'form':form})

def chat_view_gue(request):
    u= request.user
    print(u)
    chat = CHAT_GUE.objects.exclude(user=u)
    chat1=CHAT_GUE.objects.filter(user=u)
    print(chat1)
    return render(request,'chat_view_gue.html',{'chat':chat,'chat1':chat1})