from django import forms
from django.contrib.auth.forms import UserCreationForm


from GEHM_app.models import Contractor, User, GuestEmployee, Regfee, Job, Chat, CHAT_CON, Enquiry, CHAT_GUE, CHAT_AD


class DateInput(forms.DateInput):
    input_type = 'date'
class UserReg(UserCreationForm):
    username=forms.CharField()
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username','password1','password2')

class ContractorForm(forms.ModelForm):
    class Meta:
        model=Contractor
        exclude=('user',)

class GuestForm(forms.ModelForm):
    DOB= forms.DateField(widget=DateInput)
    class Meta:
        model=GuestEmployee
        exclude=('user','approval_status')

class PaymentForm(forms.ModelForm):
    class Meta:
        model=Regfee
        exclude=('user','Amount')

class JobForm(forms.ModelForm):
    class Meta:
        model=Job
        fields="__all__"

class SearchForm(forms.Form):
    Skills = forms.CharField(max_length=100)

class ChatForm(forms.ModelForm):
    contractor_id = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False).values_list('id', flat=True))  # Query only IDs
    class Meta:
        model = Chat
        fields = ['contractor_id', 'message']

class ChatForm(forms.ModelForm):
    class Meta:
        model = CHAT_CON
        fields = ('desc',)

class ChatFormAD(forms.ModelForm):
    class Meta:
        model = CHAT_AD
        fields = ('desc',)

class FeedbackForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = Enquiry
        fields = ('user','subject', 'Enquiry', 'date')

class ChatFormGUE(forms.ModelForm):
    class Meta:
        model = CHAT_GUE
        fields = ('desc',)