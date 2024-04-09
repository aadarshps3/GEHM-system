import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from GEHM_app.forms import PaymentForm, JobForm, ContractorForm, SearchForm, ChatForm, PaymentFormEmp
from GEHM_app.models import Regfee, Job, Contractor, GuestEmployee, CHAT_CON, Enquiry, Jobs, JobApplication, Payment


def con_base(request):
    return render(request,'con_base.html')
def pay_reg_fee(request):
    form=PaymentForm()
    if request.method=='POST':
        form=PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('conctracor_index')
    return render(request,'pay_reg_fee.html',{'form':form})

def payment_view(request):
    data=Regfee.objects.all()
    return render(request,'payment_view.html',{'data':data})

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Registration Fee',
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': '500',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def job_view(request):
    return render(request,'job_base.html')

def add_jobpref(request):
    form=JobForm()
    if request.method=='POST':
        form=JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_view')
    return render(request,'add_jobpref.html',{'form':form})

def view_job(request):
    data=Job.objects.all()
    return render(request,'view_job.html',{'data':data})

def view_profile(request):
    data=Contractor.objects.get(user=request.user)
    return render(request,'view_profile.html',{'data':data})

def edit_profile(request):
    profile = Contractor.objects.get(user=request.user)
    if request.method == 'POST':
        form = ContractorForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ContractorForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


# def search_emp(request):
#     data=GuestEmployee.objects.all()
#     if request.method == 'GET':
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             search_query = form.cleaned_data['search_query']
#             Employee = GuestEmployee.objects.filter(name__icontains=search_query)
#             return render(request, 'EmpView_Con.html', {'Employee': Employee, 'query': search_query,'data':data})
#     else:
#         form = SearchForm()
#     return render(request, 'EmpView_Con.html', {'form': form,'data':data})

# views.py


# def search_emp(request):
#     data=GuestEmployee.objects.all()
#     if 'skills' in request.GET:
#         skills_query = request.GET['skills']
#         employees = GuestEmployee.objects.filter(Skills__icontains=skills_query)
#     else:
#         employees = GuestEmployee.objects.all()
#
#     return render(request, 'EmpView_Con.html', {'employees': employees,'data':data})

def search_emp(request):
    Skills=request.GET.get('Skills')
    employee=GuestEmployee.objects.all()
    if Skills:
        employee=employee.filter(Skills__icontains=Skills)
    context={
        'form':SearchForm(),
        'data':employee
    }
    return render(request,'EmpView_Con.html', context)

def chat_base(request):
    return render(request,'chatpage.html')

def chat_add_con(request):
    form = ChatForm()
    u = request.user
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view_con')
    else:
        form = ChatForm()
    return render(request,'chat_add_con.html',{'form':form})

def chat_view_con(request):
    u= request.user
    print(u)
    chat = CHAT_CON.objects.exclude(user=u)
    chat1=CHAT_CON.objects.filter(user=u)
    print(chat1)
    return render(request,'chat_view_con.html',{'chat':chat,'chat1':chat1})

def Enquiry_contractor(request):
    f = Enquiry.objects.all()
    return render(request, 'Enquiry_contractor.html', {'feedback': f})

def reply_enquiry(request, id):
    f = Enquiry.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        messages.info(request, 'Reply send for complaint')
        return redirect('Enquiry_contractor')
    return render(request, 'reply_enquiry.html', {'feedback': f})

def Sort_Employee(request,id):
    emp = GuestEmployee.objects.get(user_id=id)
    emp.approval_status = True
    emp.save()
    messages.info(request,'approved')
    return redirect('search_emp')



def add_job_con(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.contractor = request.user.contractor
            job.save()
            return redirect('con_base')  # Redirect to the job list page
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})

def sented_job(request):
    user = request.user
    if hasattr(user, 'contractor'):
        try:
            contractor_jobs = Jobs.objects.filter(contractor=user.contractor)
            job_applications = JobApplication.objects.filter(job__in=contractor_jobs,approval_status=1)
            return render(request, 'sented_job.html', {'job_applications': job_applications})
        except Jobs.DoesNotExist:
            # Handle case where no jobs are found for the contractor
            return render(request, 'sented_job.html', {'job_applications': None})
    else:
        # Handle case where user is not a Contractor
        return render(request, 'error.html', {'message': 'You are not a Contractor'})


def pay_emp_fee(request):
    form=PaymentFormEmp()
    if request.method=='POST':
        form=PaymentFormEmp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_viewemp')
    return render(request,'pay_emp_fee.html',{'form':form})

def payment_viewemp(request):
    data=Payment.objects.all()
    return render(request,'payment_viewemp.html',{'data':data})