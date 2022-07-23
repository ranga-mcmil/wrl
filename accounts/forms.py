from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

ACCOUNT_TYPE =(
    ("STUDENT", "STUDENT"),
    ("SUPERVISOR", "SUPERVISOR"),
    ("WORK_SUPERVISOR", "WORK SUPERVISOR"),
)
class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control ', 'placeholder': 'Reg No / EC No / WRL ID'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'form-control', 'placeholder': 'Password'}
    )


class LoginForm(forms.Form):
   username = forms.CharField()
   password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Reg No / EC No / WRL ID',
            'name': 'usernameeee'
        }
    ))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'name': 'first_name'
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'name': 'last_name'
        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'name': 'email'
        }
    ))

    pic = forms.ImageField(widget=forms.FileInput(
        attrs={
            'name': 'photo',
            'class': 'form-control pt-1'
        }
    ))

    type = forms.ChoiceField(choices=ACCOUNT_TYPE, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'type',
            'placeholde': 'What are you joining as: '

        }
    ))



    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'name': 'password'
        }
    ))


    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'name': 'password'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'type', 'pic')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match')

