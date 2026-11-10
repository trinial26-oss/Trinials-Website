"""
Context processors for the website app.
Exposes global configuration variables (such as direct contact options and SEO defaults)
to templates without modifying view logic.
"""
import os
from django.conf import settings


def contact_settings(request):
    """
    Expose configured WhatsApp, phone, direct email, and SEO metadata to templates.
    Returns defaults if not explicitly configured in Django settings.
    """
    site_url = getattr(settings, 'SITE_URL', 'https://trinial.in').rstrip('/')
    path = getattr(request, 'path', '/')
    canonical_url = f"{site_url}{path}"

    return {
        'contact_email': getattr(settings, 'CONTACT_EMAIL', 'trinial26@gmail.com'),
        'contact_phone_number': getattr(settings, 'CONTACT_PHONE_NUMBER', '+91 85908 21155'),
        'contact_phone_number_secondary': getattr(settings, 'CONTACT_PHONE_NUMBER_SECONDARY', '+91 94003 25570'),
        'contact_whatsapp_url': getattr(settings, 'CONTACT_WHATSAPP_URL', 'https://wa.me/918590821155'),
        'site_url': site_url,
        'site_name': 'Trinials',
        'canonical_url': canonical_url,
        'google_site_verification': os.environ.get('GOOGLE_SITE_VERIFICATION', getattr(settings, 'GOOGLE_SITE_VERIFICATION', '')),
    }


