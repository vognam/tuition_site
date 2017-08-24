from django import forms
from .models import Student, Tutor

class ContactForm(forms.Form):
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Smith'}),
                                   required=True)
    contact_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '07XXXXXXXXX'}),
                                   required=True)
    contact_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johnsmith@example.com'}), required=True)
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'tutor', 'classID',)


class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutor
        fields = ('first_name', 'last_name',)
