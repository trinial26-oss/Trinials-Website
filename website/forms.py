from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Form for validating and creating ContactMessage instances.
    Includes honeypot protection against spam bots and trims whitespace.
    """
    website_hp = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none !important;',
            'tabindex': '-1',
            'autocomplete': 'off',
            'aria-hidden': 'true',
        }),
        label="Leave empty (anti-spam honeypot)"
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'contact-name',
                'placeholder': 'Your full name',
                'autocomplete': 'name',
                'maxlength': '100',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'id': 'contact-email',
                'placeholder': 'you@company.com',
                'autocomplete': 'email',
                'maxlength': '254',
                'required': 'required',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'contact-phone',
                'placeholder': '+1 (555) 000-0000',
                'autocomplete': 'tel',
                'type': 'tel',
                'maxlength': '30',
                'required': 'required',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'contact-subject',
                'placeholder': 'What are you working on?',
                'maxlength': '150',
                'required': 'required',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'id': 'contact-message',
                'placeholder': 'Tell us about your project or idea...',
                'rows': '4',
                'maxlength': '3000',
                'required': 'required',
            }),
        }
        error_messages = {
            'name': {
                'required': 'Please provide your full name.',
                'max_length': 'Name cannot exceed 100 characters.',
            },
            'email': {
                'required': 'Please provide a valid email address.',
                'invalid': 'Please enter a valid email address (e.g. you@company.com).',
                'max_length': 'Email address cannot exceed 254 characters.',
            },
            'phone': {
                'required': 'Please provide your phone number.',
                'max_length': 'Phone number cannot exceed 30 characters.',
            },
            'subject': {
                'required': 'Please provide an inquiry subject.',
                'max_length': 'Subject cannot exceed 150 characters.',
            },
            'message': {
                'required': 'Please enter your message.',
                'max_length': 'Message cannot exceed 3000 characters.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Please provide your full name.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("Please provide a valid email address.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError("Please provide your phone number.")
        import re
        if not re.match(r'^[0-9+\-\s().]{6,30}$', phone):
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject:
            raise forms.ValidationError("Please provide an inquiry subject.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise forms.ValidationError("Please enter your message.")
        return message

    def clean(self):
        cleaned_data = super().clean()
        # Honeypot field inspection
        if cleaned_data.get('website_hp'):
            raise forms.ValidationError("Spam submission rejected.")
        return cleaned_data
