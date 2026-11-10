"""
Context processors for the website app.
Exposes global configuration variables (such as direct contact options)
to templates without modifying view logic.
"""
from django.conf import settings


def contact_settings(request):
    """
    Expose configured WhatsApp, phone, and direct email contact details to templates.
    Returns defaults if not explicitly configured in Django settings.
    """
    return {
        'contact_email': getattr(settings, 'CONTACT_EMAIL', 'trinial26@gmail.com'),
        'contact_phone_number': getattr(settings, 'CONTACT_PHONE_NUMBER', '+91 85908 21155'),
        'contact_phone_number_secondary': getattr(settings, 'CONTACT_PHONE_NUMBER_SECONDARY', '+91 94003 25570'),
        'contact_whatsapp_url': getattr(settings, 'CONTACT_WHATSAPP_URL', 'https://wa.me/918590821155'),
    }

