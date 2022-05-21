from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
      

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     ''' remove any labels here if desired
    #     '''
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)

    #     # remove the label of a non-linked/calculated field (txt01 added at top of form)
    #     self.fields['txt01'].label = ''

    #     # you can also remove labels of built-in model properties
    #     self.fields['name'].label = ''