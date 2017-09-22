from django import forms
from .models import Student, QuestionDone, Question, Class
from django.contrib.auth.models import User


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
        fields = ('first_name', 'last_name', 'classID',)


class StudentChoiceForm(forms.Form):

    students = forms.ModelChoiceField(queryset=Student.objects.filter(classID__tutor=0))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(StudentChoiceForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.filter(classID__tutor=self.user.id)


class InputScoreForm(forms.ModelForm):

    class Meta:
        model = QuestionDone
        fields = ('student', 'question', 'score',)

    # TODO validate score is between -1 and out_of


class ClassChoiceForm(forms.Form):
    classes = forms.ModelChoiceField(queryset=Class.objects.filter())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ClassChoiceForm, self).__init__(*args, **kwargs)
        self.fields['classes'].queryset = Class.objects.filter(tutor=self.user.id)


class CategoryChoiceForm(forms.Form):
    choice_field = forms.ChoiceField(choices=Question.CATEGORIES)
