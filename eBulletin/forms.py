from django import forms
from django.contrib.auth.models import User

class UserRegForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    re_password = forms.CharField(label='RePassword',
                                 widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_re_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['re_password']:
            raise forms.ValidationError('Two passwords does not match!')
        return cd['re_password']
