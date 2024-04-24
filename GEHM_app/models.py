from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_guestemp=models.BooleanField(default=False)
    is_contractors=models.BooleanField(default=False)

class Contractor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='contractor')
    Name=models.CharField(max_length=100)
    Phone_No=models.CharField(max_length=10)
    Company_Name=models.CharField(max_length=150)
    Registration_ID=models.CharField(max_length=10)
    Home_Address=models.CharField(max_length=255)
    Company_Address=models.CharField(max_length=255)
    Profile_photo=models.ImageField(upload_to='profile_contractor')
    reg_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.Name

class GuestEmployee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='GuestEmployee')
    Name=models.CharField(max_length=100)
    DOB=models.DateField()
    Address=models.CharField(max_length=255)
    Mobile_No=models.CharField(max_length=10)
    Photo=models.ImageField(upload_to='emp_pics')
    Adhar=models.FileField(upload_to='CV')
    Experiance=models.CharField(max_length=2)
    Skills=models.TextField()
    Job_Preference=models.CharField(max_length=200)
    reg_date = models.DateField(auto_now=True)
    approval_status = models.BooleanField(default=0)

    def __str__(self):
        return self.Name

AMOUNT=(
    ('500','500'),
    ('1000','1000'),
    ('1500','1500'),
)
class Regfee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Payment',null=True)
    Card_Number=models.CharField(max_length=100)
    MM_YY=models.CharField(max_length=50)
    CVV=models.CharField(max_length=50)
    Name_on_the_card=models.CharField(max_length=50)
    Amount=models.CharField(max_length=100,choices=AMOUNT)
    date=models.DateField(auto_now=True)

class Job(models.Model):
    Job_Preference=models.CharField(max_length=100)
    Sector=models.CharField(max_length=100)
    Qualifications=models.CharField(max_length=100)
    Required_Positions=models.CharField(max_length=100)

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class CHAT_CON(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat',null=True)
    desc = models.TextField()
    date = models.DateField(auto_now=True)

class Enquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=200)
    Enquiry = models.TextField()
    date = models.DateField()
    reply = models.TextField(null=True, blank=True)

class CHAT_GUE(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='guest_chat',null=True)
    desc = models.TextField()
    date = models.DateField(auto_now=True)

class CHAT_AD(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_chat',null=True)
    desc = models.TextField()
    date = models.DateField(auto_now=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Jobs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary_scale = models.CharField(max_length=100)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    applicant = models.ForeignKey(GuestEmployee, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.applicant.name} applied for {self.job.title}"

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CON')
    Employee=models.ForeignKey(GuestEmployee,on_delete=models.CASCADE,related_name='PaymentEmp',null=True)
    Card_Number=models.CharField(max_length=100)
    MM_YY=models.CharField(max_length=50)
    CVV=models.CharField(max_length=50)
    Name_on_the_card=models.CharField(max_length=50)
    Amount=models.CharField(max_length=100,choices=AMOUNT)
    date=models.DateField(auto_now=True)

class chats(models.Model):
    user=models.CharField(max_length=100)
    chat_id=models.CharField(max_length=100)
    desc = models.TextField()
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.user