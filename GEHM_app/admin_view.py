from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from GEHM_app.forms import ChatForm, ChatFormAD, ChatFormGUE
from GEHM_app.models import Contractor, GuestEmployee, Job, Chat, User, CHAT_CON, CHAT_GUE


def contractor_view(request):
    data=Contractor.objects.all()
    return render(request,'contractor_view.html',{'data':data})

def guestview(request):
    data=GuestEmployee.objects.all()
    return render(request,'guestview.html',{'data':data})

def job_openinigs(request):
    data = Job.objects.all()
    return render(request,'job_openinigs.html',{'data':data})

def del_jobopen(request,id):
    data = Job.objects.get(id=id)
    data.delete()
    return redirect('job_openinigs')

def chatpage(request):
    return render(request,'chatpage.html')

def view_contr(request):
    contractors = Contractor.objects.all()
    return render(request, 'view_contr.html', {'contractors': contractors})

def send_message(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            contractor_id = form.cleaned_data['contractor_id']
            message.recipient_id = contractor_id  # Set recipient_id directly
            message.save()
            return redirect('chat_view')
    else:
        form = ChatForm()
    return render(request, 'chat_add.html', {'form': form})

@login_required
def chat_view(request):
    chats = CHAT_CON.objects.all()
    return render(request, 'chat_view.html', {'chats': chats})

# def chat_view(request):
#     u= request.user
#     print(u)
#     chat = CHAT_CON.objects.exclude(user=u)
#     chat1=CHAT_CON.objects.filter(user=u)
#     print(chat1)
#     return render(request,'chat_view_con.html',{'chat':chat,'chat1':chat1})


# def send_message_gue(request):
#     if request.method == 'POST':
#         form = ChatForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             contractor_id = form.cleaned_data['contractor_id']
#             message.recipient_id = contractor_id  # Set recipient_id directly
#             message.save()
#             return redirect('chat_view')
#     else:
#         form = ChatForm()
#     return render(request, 'chat_add.html', {'form': form})

def chat_add_ad(request):
    form = ChatForm()
    u = request.user
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view')
    else:
        form = ChatFormAD()
    return render(request,'chat_add_ad.html',{'form':form})
def chat_view_gue_admin(request):
    chats = CHAT_GUE.objects.all()
    return render(request, 'chat_view_gue_admin.html', {'chats': chats})

def chat_add_ad_gu(request):
    form = ChatFormGUE()
    u = request.user
    if request.method == 'POST':
        form = ChatFormGUE(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view_gue_admin')
    else:
        form = ChatFormAD()
    return render(request,'chat_add_ad_gu.html',{'form':form})