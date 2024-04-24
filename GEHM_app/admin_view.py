import calendar

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractMonth, TruncMonth
from django.shortcuts import render, redirect

from GEHM_app.forms import ChatForm, ChatFormAD, ChatFormGUE
from GEHM_app.models import Contractor, GuestEmployee, Job, Chat, User, CHAT_CON, CHAT_GUE, Jobs, JobApplication
from GEHM_app.models import chats as chats_db


def contractor_view(request):
    data = Contractor.objects.all()
    return render(request, 'contractor_view.html', {'data': data})


def guestview(request):
    data = GuestEmployee.objects.all()
    return render(request, 'guestview.html', {'data': data})


def job_openinigs(request):
    data = Job.objects.all()
    return render(request, 'job_openinigs.html', {'data': data})


def del_jobopen(request, id):
    data = Job.objects.get(id=id)
    data.delete()
    return redirect('job_openinigs')


def chatpage(request):
    return render(request, 'chatpage.html')


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
    data = Contractor.objects.all()
    return render(request, 'chat_view.html', {'data': data})


def view_chat_Contra(request, Name):
    print(Name)
    request.session['chat_name'] = Name
    data = Contractor.objects.all()
    chats = chats_db.objects.filter(chat_id="admin_" + Name)

    return render(request, 'chat_view.html', {'chats': chats, 'data': data})


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
            Name = request.session['chat_name']
            user_input = form.cleaned_data['desc']
            print(user_input, ">>>>>>>>>>>>>>>>>")
            chats_db.objects.create(user="admin", chat_id="admin_" + Name, desc=user_input)
            # obj = form.save(commit=False)
            # obj.user = u
            # obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view')
    else:
        form = ChatFormAD()
    return render(request, 'chat_add_ad.html', {'form': form})


def chat_view_gue_admin(request):
    data = GuestEmployee.objects.all()
    return render(request, 'chat_view_gue_admin.html', {'data': data})


def view_chat_Emp(request, Name):
    print(Name)
    request.session['chat_name'] = Name
    data = GuestEmployee.objects.all()
    chats = chats_db.objects.filter(chat_id="admin_" + Name)

    return render(request, 'chat_view_gue_admin.html', {'chats': chats, 'data': data})


def chat_add_ad_gu(request):
    form = ChatFormGUE()
    u = request.user

    if request.method == 'POST':
        form = ChatFormGUE(request.POST)
        if form.is_valid():
            Name = request.session['chat_name']
            user_input = form.cleaned_data['desc']
            print(user_input, ">>>>>>>>>>>>>>>>>")
            chats_db.objects.create(user="admin", chat_id="admin_" + Name, desc=user_input)
            # obj = form.save(commit=False)
            # obj.user = u
            # obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view_gue_admin')
    else:
        form = ChatFormAD()
    return render(request, 'chat_add_ad_gu.html', {'form': form})


def view_sorted(request):
    data = GuestEmployee.objects.all()
    return render(request, 'view_sorted.html', {'data': data})




def view_all_job_applications(request):
    # Get all job applications and sort them by applicant's experience level in descending order
    job_applications = JobApplication.objects.all().order_by('-applicant__Experiance')
    return render(request, 'view_all_job_applications.html', {'job_applications': job_applications})



def sent_job(request, id):
    a = JobApplication.objects.get(id=id)
    a.approval_status = 1
    a.save()
    messages.info(request, 'Job sented')
    return redirect('view_all_job_applications')


def join_report(request):
    # Get distinct months with count of employees joined each month
    distinct_months = GuestEmployee.objects.annotate(join_month=ExtractMonth('reg_date')).values_list('join_month', flat=True).distinct()

    # Filter out any invalid or empty month values
    distinct_months = [month for month in distinct_months if month is not None]

    # Map month numbers to month names
    month_map = {month: calendar.month_name[month] for month in distinct_months}

    return render(request, 'join_report.html', {'month_map': month_map})

def employee_details_by_month(request, month):
    # Get employee details for the specified month
    employees = GuestEmployee.objects.filter(reg_date__month=month)

    return render(request, 'employee_details.html', {'employees': employees})









def join_report_con(request):
    report_data = Contractor.objects.annotate(join_month=ExtractMonth('reg_date')).values('join_month').annotate(total=Count('user')).order_by('join_month')

    # Prepare report
    report = [{'month': entry['join_month'], 'total': entry['total']} for entry in report_data]

    # Get all employee details
    employee_details = Contractor.objects.all()

    return render(request, 'join_report_con.html', {'report': report, 'employee_details': employee_details})

def join_reportCon(request):
    # Get distinct months with count of employees joined each month
    distinct_months = Contractor.objects.annotate(join_month=ExtractMonth('reg_date')).values_list('join_month', flat=True).distinct()

    # Filter out any invalid or empty month values
    distinct_months = [month for month in distinct_months if month is not None]

    # Map month numbers to month names
    month_map = {month: calendar.month_name[month] for month in distinct_months}

    return render(request, 'join_report_con.html', {'month_map': month_map})

def con_details_by_month(request, month):
    # Get employee details for the specified month
    employees = Contractor.objects.filter(reg_date__month=month)

    return render(request, 'con_details.html', {'employees': employees})