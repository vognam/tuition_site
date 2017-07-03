from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    form_message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
