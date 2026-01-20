from django import forms
from .models import Complaint, DocumentRequest, Announcement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# -------------------- USER REGISTRATION --------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

# -------------------- COMPLAINT FORM --------------------
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter complaint subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your complaint'}),
        }

# -------------------- DOCUMENT REQUEST FORM --------------------
class DocumentRequestForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ['document_type', 'purpose']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),  # Dropdown from model choices
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'State the purpose of your request'}),
        }

# -------------------- ANNOUNCEMENT FORM --------------------
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Announcement content'}),
        }
