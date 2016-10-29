from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput())

class ContactForm(forms.Form):
    sender = forms.EmailField(
      required=True,
      label='',
      widget=forms.TextInput(
        attrs={'style': 'width:350px', 'placeholder': 'E-mail'}
        )
      )
    name = forms.CharField(
      label='',
      max_length=100,
      widget=forms.TextInput(
        attrs={'style': 'width:350px', 'placeholder': 'Name'}
        )
      )
    message = forms.CharField(
      label='',
      widget=forms.Textarea(
        attrs={'style': 'width:350px','placeholder': 'Please type your comments and suggestions here'}
        )
)