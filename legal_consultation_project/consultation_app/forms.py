from django import forms
from .models import Lawyer
from .models import LawyerProfile, Client

class LawyerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = Lawyer
        fields = ['username', 'first_name', 'last_name',  'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")


class LawyerLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
    )


class LawyerProfileForm(forms.ModelForm):
    class Meta:
        model = LawyerProfile
        fields = [
            'full_name',
            'specialization',
            'experience',
            'education',
            'bio',
            'phone',
            'location',
            'professional_certificate',
            'profile_picture',
            'is_available'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 2}),
        }

class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']