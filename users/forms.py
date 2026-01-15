from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
            user.profile.role = self.cleaned_data['role']
            user.profile.save()
        return user

