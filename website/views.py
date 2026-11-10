import datetime
import logging
import sys
import threading
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import ContactForm
from .seo_data import SERVICES, INSIGHTS

logger = logging.getLogger(__name__)


def home(request):
    """
    Render the homepage containing all sections.
    Provides an unbound ContactForm instance for the contact section.
    """
    contact_form = ContactForm()
    return render(request, 'base.html', {'contact_form': contact_form})


def about_page(request):
    """
    Render the dedicated About Us page highlighting Trinials philosophy,
    story, core capabilities, leadership, and contact channels.
    """
    return render(request, 'pages/about.html')


def privacy_policy(request):
    """
    Render the formal Privacy Policy page for Trinials, detailing data collection,
    inquiry processing, security standards, and user privacy rights.
    """
    return render(request, 'pages/privacy_policy.html')


def terms_conditions(request):
    """
    Render the Terms and Conditions page for Trinials outlining studio services,
    intellectual property, project proposals, liability, and governance.
    """
    return render(request, 'pages/terms_conditions.html')


def design_preview(request):
    """
    Render the Phase 2 Global Design System preview.
    Demonstrates colors, typography, buttons, cards, containers, and responsive scaling.
    """
    return render(request, 'design_preview.html')


# -----------------------------------------------------------------------------
# SEO Service Landing Pages
# -----------------------------------------------------------------------------

def services_index(request):
    """
    Hub page listing all digital studio services with deep-links,
    benefits, and structured Service schemas for Google crawlers.
    """
    return render(request, 'pages/services_index.html', {
        'services': SERVICES,
        'contact_form': ContactForm(),
    })


def service_detail(request, slug):
    """
    Render an individual, highly-optimized service landing page.
    Includes target keywords, detailed explanations, capabilities,
    featured case studies, and accordion FAQs with Schema.org markup.
    """
    service = SERVICES.get(slug)
    if not service:
        raise Http404(f"Service '{slug}' was not found.")

    return render(request, 'pages/service_detail.html', {
        'service': service,
        'all_services': SERVICES,
        'contact_form': ContactForm(),
    })


def service_web_development(request):
    return service_detail(request, 'web-development')


def service_ui_ux_design(request):
    return service_detail(request, 'ui-ux-design')


def service_ecommerce_development(request):
    return service_detail(request, 'ecommerce-development')


def service_custom_software_development(request):
    return service_detail(request, 'custom-software-development')


def service_brand_identity_design(request):
    return service_detail(request, 'brand-identity-design')


# -----------------------------------------------------------------------------
# SEO Content Guides / Insights
# -----------------------------------------------------------------------------

def insights_index(request):
    """
    Knowledge Hub page showcasing all comprehensive client guides and
    technical articles to capture high-intent search traffic.
    """
    return render(request, 'pages/insights_index.html', {
        'insights': INSIGHTS,
        'contact_form': ContactForm(),
    })


def insight_detail(request, slug):
    """
    Render an in-depth, data-rich article targeting prospective client queries
    (such as Website Cost in Kerala or Custom vs WordPress).
    """
    insight = INSIGHTS.get(slug)
    if not insight:
        raise Http404(f"Insight '{slug}' was not found.")

    return render(request, f'pages/insights/{slug.replace("-", "_")}.html', {
        'insight': insight,
        'all_insights': INSIGHTS,
        'contact_form': ContactForm(),
    })


def insight_website_cost(request):
    return insight_detail(request, 'website-development-cost-in-kerala')


def insight_why_need_website(request):
    return insight_detail(request, 'why-businesses-need-professional-website')


def insight_custom_vs_wordpress(request):
    return insight_detail(request, 'custom-website-vs-wordpress')


def insight_ecommerce_guide(request):
    return insight_detail(request, 'ecommerce-website-development-guide')


def insight_choose_company(request):
    return insight_detail(request, 'how-to-choose-web-development-company-kerala')


# -----------------------------------------------------------------------------
# Technical SEO: sitemap.xml & robots.txt
# -----------------------------------------------------------------------------

def sitemap_xml(request):
    """
    Dynamically generates a 100% compliant XML sitemap covering all canonical
    pages, service landing pages, insight guides, and legal sections.
    """
    site_url = getattr(settings, 'SITE_URL', 'https://trinial.in').rstrip('/')
    today = datetime.date.today().isoformat()

    urls = [
        # Primary Pages
        {'loc': f"{site_url}/", 'lastmod': today, 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': f"{site_url}/about/", 'lastmod': today, 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{site_url}/services/", 'lastmod': today, 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{site_url}/insights/", 'lastmod': today, 'changefreq': 'weekly', 'priority': '0.8'},
    ]

    # Service Landing Pages (Priority 0.9)
    for slug in SERVICES.keys():
        urls.append({
            'loc': f"{site_url}/services/{slug}/",
            'lastmod': today,
            'changefreq': 'weekly',
            'priority': '0.9',
        })

    # Insight / Resource Guides (Priority 0.8)
    for slug, meta in INSIGHTS.items():
        urls.append({
            'loc': f"{site_url}/insights/{slug}/",
            'lastmod': meta.get('date_modified', today),
            'changefreq': 'weekly',
            'priority': '0.8',
        })

    # Legal & Utility Pages (Priority 0.3)
    urls.extend([
        {'loc': f"{site_url}/privacy-policy/", 'lastmod': today, 'changefreq': 'monthly', 'priority': '0.3'},
        {'loc': f"{site_url}/terms-and-conditions/", 'lastmod': today, 'changefreq': 'monthly', 'priority': '0.3'},
    ])

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for u in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f"    <loc>{u['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{u['priority']}</priority>")
        xml_lines.append('  </url>')
    xml_lines.append('</urlset>')

    return HttpResponse('\n'.join(xml_lines), content_type="application/xml; charset=utf-8")


def robots_txt(request):
    """
    Serves a search-engine compliant robots.txt with sitemap location and crawl directives.
    """
    site_url = getattr(settings, 'SITE_URL', 'https://trinial.in').rstrip('/')
    content = f"""# Robots.txt for Trinials Digital Studio
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /design-preview/

Sitemap: {site_url}/sitemap.xml
Host: {site_url}
"""
    return HttpResponse(content.strip() + "\n", content_type="text/plain; charset=utf-8")


def contact_submit(request):
    """
    Dedicated view to process contact form submissions.
    Supports both modern AJAX (JSON) requests for instant, seamless UX
    and traditional POST requests with POST-Redirect-GET fallback.
    Dispatches notifications and auto-responses asynchronously in production
    for near-instant (< 50ms) user response times.
    """
    if request.method != 'POST':
        return redirect(f"{reverse('website:home')}#contact")

    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('accept', '') or
        request.POST.get('is_ajax') == '1'
    )

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()

        # Dispatch emails (asynchronously in production/dev, synchronously in test runs)
        _dispatch_inquiry_emails(contact_message)

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': "Thanks for reaching out! Your message has been received, and we'll be in touch soon.",
                'inquiry': {
                    'id': contact_message.id,
                    'name': contact_message.name,
                    'email': contact_message.email,
                    'phone': contact_message.phone or '',
                    'subject': contact_message.subject,
                }
            })

        messages.success(
            request,
            "Thanks for reaching out. Your message has been received, and we'll be in touch soon."
        )
        return redirect(f"{reverse('website:home')}#contact")
    else:
        if is_ajax:
            errors_dict = {}
            for field, error_list in form.errors.items():
                errors_dict[field] = [str(e) for e in error_list]
            return JsonResponse({
                'success': False,
                'message': "Please check the form below and correct any errors.",
                'errors': errors_dict,
            }, status=400)

        messages.error(
            request,
            "Please check the form below and correct any errors."
        )
        return render(request, 'base.html', {
            'contact_form': form,
            'contact_errors': True,
        })


def _dispatch_inquiry_emails(contact_message):
    """
    Dispatch team notification and client confirmation emails.
    In testing environments with in-memory mail backend, executes synchronously
    so test assertions on mail.outbox succeed immediately.
    In live production / web requests, executes in a background daemon thread
    for ultra-fast, zero-blocking HTTP responses (< 50ms).
    """
    def _worker():
        _send_contact_notification(contact_message)
        _send_client_auto_response(contact_message)

    is_testing = (
        getattr(settings, 'TESTING', False) or
        'test' in sys.argv or
        str(getattr(settings, 'EMAIL_BACKEND', '')).endswith('locmem.EmailBackend')
    )

    if is_testing:
        _worker()
    else:
        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()


def _send_contact_notification(contact_message):
    """
    Dispatch an attractive HTML email notification to the company email(s) if configured.
    Supports single recipient or comma-separated list of recipients.
    Includes client name, email, phone number, subject, timestamp, and message.
    Fail-safe: handles any exceptions gracefully without disrupting user feedback or database record.
    """
    recipient_setting = getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', '')
    if not recipient_setting:
        return

    if isinstance(recipient_setting, (list, tuple)):
        recipients = [str(r).strip() for r in recipient_setting if str(r).strip()]
    else:
        recipients = [r.strip() for r in str(recipient_setting).split(',') if r.strip()]

    if not recipients:
        return

    submitted_time = (
        f"{contact_message.created_at:%Y-%m-%d %H:%M:%S UTC}"
        if contact_message.created_at
        else "Just now"
    )

    subject = f"New Inquiry from {contact_message.name}: {contact_message.subject}"

    # Plain text fallback
    plain_text = (
        f"You have received a new contact inquiry on Trinials.\n\n"
        f"Sender: {contact_message.name}\n"
        f"Email: {contact_message.email}\n"
        f"Phone: {contact_message.phone or 'Not provided'}\n"
        f"Subject: {contact_message.subject}\n"
        f"Submitted: {submitted_time}\n\n"
        f"Message:\n"
        f"{contact_message.message}\n"
    )

    context = {
        'name': contact_message.name,
        'email': contact_message.email,
        'phone': contact_message.phone,
        'subject': contact_message.subject,
        'message': contact_message.message,
        'submitted_time': submitted_time,
    }

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'Trinials <dummy11248@gmail.com>'

    try:
        html_content = render_to_string('emails/team_notification.html', context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=from_email,
            to=recipients,
            reply_to=[contact_message.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info(
            "Dispatched contact notification email for ContactMessage id=%s to %s",
            contact_message.id,
            recipients
        )
    except Exception as e:
        logger.error(
            "Failed to send contact notification email for ContactMessage id=%s: %s",
            contact_message.id,
            e,
            exc_info=False
        )


def _send_client_auto_response(contact_message):
    """
    Send an attractive branded confirmation email back to the client.
    Notice: Does NOT include a copy of the message, as requested by the client.
    Fail-safe: handles any exceptions gracefully without disrupting user feedback.
    """
    if not contact_message.email:
        return

    subject = f"Thank you for contacting Trinials — We've received your inquiry"

    # Plain text fallback (NO copy of the client message!)
    plain_text = (
        f"Hi {contact_message.name},\n\n"
        f"Thank you for reaching out to Trinials! We have received your inquiry regarding \"{contact_message.subject}\".\n\n"
        f"Our team is currently reviewing your project requirements and will get back to you within 24 to 48 business hours.\n\n"
        f"If you have any urgent questions, feel free to reply directly to this email.\n\n"
        f"Warm regards,\n"
        f"The Trinials Team\n"
        f"trinial26@gmail.com\n"
        f"+91 85908 21155 | +91 94003 25570\n"
    )

    context = {
        'name': contact_message.name,
        'subject': contact_message.subject,
        'contact_email': getattr(settings, 'CONTACT_EMAIL', 'trinial26@gmail.com'),
        'phone_number': getattr(settings, 'CONTACT_PHONE_NUMBER', '+91 85908 21155'),
        'phone_number_secondary': getattr(settings, 'CONTACT_PHONE_NUMBER_SECONDARY', '+91 94003 25570'),
    }

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'Trinials <dummy11248@gmail.com>'

    try:
        html_content = render_to_string('emails/client_auto_response.html', context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=from_email,
            to=[contact_message.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info(
            "Dispatched client auto-response confirmation to %s for ContactMessage id=%s",
            contact_message.email,
            contact_message.id
        )
    except Exception as e:
        logger.error(
            "Failed to send client auto-response for ContactMessage id=%s: %s",
            contact_message.id,
            e,
            exc_info=False
        )
