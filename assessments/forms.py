from django import forms
from .models import Log, Comment
from accounts.models import Student, Contact, User, WorkSupervisor



class LogForm(forms.ModelForm):
    document = forms.FileInput(
        attrs={
            'class': 'form-control file-upload-info',
        }
    )

    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control html-editor',
            'rows': "10"

        }
    ))

    class Meta:
        model = Log
        fields = ('document', 'description')


class CommentForm(forms.ModelForm):

    body = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'border-0 flex-1 w-100',
            'placeholder': "Type your message here"
        }
    ))

    class Meta:
        model = Comment
        fields = ('body',)


class AddStudentForm(forms.Form):
    students = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        student = cl_data.get('students')

        return student

    def send(self):
        # Cleaned data
        cl_data = super().clean()

        student = cl_data.get('students')


        print(student)


class AddWRLSupervisorForm(forms.Form):
    supervisor = forms.ModelChoiceField(queryset=WorkSupervisor.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Add Work Supervisor'
        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        supervisor = cl_data.get('supervisor')

        return supervisor

    def send(self):
        # Cleaned data
        cl_data = super().clean()

        supervisor = cl_data.get('supervisor')


        print(student)


class UpdateProgForm(forms.Form):
    programme = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Add programme',
            'name': 'programme'
        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        programme = cl_data.get('programme')

        return programme

