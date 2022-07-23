
from django import forms
from .models import Remark, StudentName, StudentRemark


class RemarkForm(forms.ModelForm):

    remarks = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control html-editor',
            'rows': "10"

        }
    ))

    class Meta:
        model = Remark
        fields = ('remarks',)


class StudentNameForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Student Name',
            'name': 'programme'
        }
    ))

    class Meta:
        model = StudentName
        fields = ('name',)


class StudentRemarkForm(forms.ModelForm):

    remarks = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control html-editor',
            'rows': "10"

        }
    ))

    class Meta:
        model = StudentRemark
        fields = ('remarks',)