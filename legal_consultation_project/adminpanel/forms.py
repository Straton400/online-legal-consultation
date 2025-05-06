from django import forms
from consultation_app.models import LegalArticle

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Password'
    }))


class LegalArticleForm(forms.ModelForm):
    class Meta:
        model = LegalArticle
        fields = ['title', 'slug', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }