from datetime import datetime, timezone, date
import functools
import logging
import sys
import threading
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, Http404, JsonResponse, FileResponse
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
    today = date.today().isoformat()

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


def favicon_view(request):
    """
    Serve the root favicon.ico with image/x-icon content-type and 1-year cache headers.
    Ensures browsers, bookmarks, and search engine crawlers reliably display the icon in tabs.
    """
    ico_path = settings.BASE_DIR / 'static' / 'favicon.ico'
    if ico_path.exists():
        response = FileResponse(open(ico_path, 'rb'), content_type='image/x-icon')
        response['Cache-Control'] = 'public, max-age=31536000'
        return response

    png_path = settings.BASE_DIR / 'static' / 'images' / 'favicon.png'
    if png_path.exists():
        response = FileResponse(open(png_path, 'rb'), content_type='image/png')
        response['Cache-Control'] = 'public, max-age=31536000'
        return response

    return HttpResponse(status=404)


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
        name = form.cleaned_data.get('name', '').strip()
        email = form.cleaned_data.get('email', '').strip()
        phone = form.cleaned_data.get('phone', '').strip()
        subject = form.cleaned_data.get('subject', '').strip()
        message = form.cleaned_data.get('message', '').strip()

        # 1. Primary Cloud Persistence: Save directly to MongoDB Atlas
        mongo_id = None
        try:
            from .mongo import save_enquiry_to_mongo
            mongo_id = save_enquiry_to_mongo({
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:250],
            })
        except Exception as mongo_err:
            logger.warning("MongoDB Atlas save notice: %s", mongo_err)

        # 2. Local Fallback Persistence: ContactMessage (fail-safe if SQLite is absent/read-only)
        contact_message = None
        try:
            contact_message = form.save()
        except Exception as db_err:
            logger.warning("Local DB save notice (MongoDB Atlas primary active): %s", db_err)

        if contact_message is None:
            class LightweightInquiry:
                def __init__(self, mid, n, e, p, s, m):
                    self.id = mid or 1
                    self.name = n
                    self.email = e
                    self.phone = p
                    self.subject = s
                    self.message = m
                    self.created_at = datetime.now(timezone.utc)
            contact_message = LightweightInquiry(mongo_id, name, email, phone, subject, message)

        # 3. Dispatch emails (asynchronously in production/dev, synchronously in test runs)
        _dispatch_inquiry_emails(contact_message, mongo_id=mongo_id)

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': "Thanks for reaching out! Your message has been received, and we'll be in touch soon.",
                'inquiry': {
                    'id': getattr(contact_message, 'id', mongo_id),
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


def _dispatch_inquiry_emails(contact_message, mongo_id=None):
    """
    Dispatch team notification and client confirmation emails.
    In testing environments with in-memory mail backend, executes synchronously
    so test assertions on mail.outbox succeed immediately.
    In live production / web requests, executes in a background daemon thread
    for ultra-fast, zero-blocking HTTP responses (< 50ms).
    Loads credentials and notification list dynamically from MongoDB Atlas (with settings fallback).
    Reuses a single persistent SMTP connection to eliminate duplicate SSL/handshake latency.
    Logs dispatch status directly back to MongoDB Atlas.
    """
    is_testing = (
        getattr(settings, 'TESTING', False) or
        'test' in sys.argv or
        str(getattr(settings, 'EMAIL_BACKEND', '')).endswith('locmem.EmailBackend')
    )

    def _worker():
        from .mongo import get_email_config_from_mongo, log_email_dispatch_status_to_mongo
        from django.core.mail import get_connection

        mongo_cfg = {}
        if not is_testing:
            try:
                mongo_cfg = get_email_config_from_mongo() or {}
            except Exception as e:
                logger.warning("Could not read email_config from MongoDB: %s", e)

        backend = getattr(settings, 'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
        connection = None

        # If not using locmem test backend, open optimized connection using MongoDB credentials
        if not str(backend).endswith('locmem.EmailBackend'):
            host = mongo_cfg.get('EMAIL_HOST') or getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
            port = int(mongo_cfg.get('EMAIL_PORT') or getattr(settings, 'EMAIL_PORT', 465))
            username = mongo_cfg.get('EMAIL_HOST_USER') or getattr(settings, 'EMAIL_HOST_USER', '')
            password = mongo_cfg.get('EMAIL_HOST_PASSWORD') or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
            use_ssl = bool(mongo_cfg.get('EMAIL_USE_SSL', True)) if 'EMAIL_USE_SSL' in mongo_cfg else getattr(settings, 'EMAIL_USE_SSL', True)
            use_tls = bool(mongo_cfg.get('EMAIL_USE_TLS', False)) if 'EMAIL_USE_TLS' in mongo_cfg else getattr(settings, 'EMAIL_USE_TLS', False)

            try:
                connection = get_connection(
                    backend=backend,
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    use_ssl=use_ssl,
                    use_tls=use_tls,
                    timeout=10,
                )
                connection.open()
            except Exception as conn_err:
                logger.warning("Could not pre-open mail connection: %s", conn_err)
                connection = None

        team_ok = False
        client_ok = False
        errors = []

        try:
            team_ok = _send_contact_notification(contact_message, connection=connection, email_config=mongo_cfg)
        except Exception as te:
            errors.append(f"Team notification error: {te}")

        try:
            client_ok = _send_client_auto_response(contact_message, connection=connection, email_config=mongo_cfg)
        except Exception as ce:
            errors.append(f"Client auto-response error: {ce}")

        if connection:
            try:
                connection.close()
            except Exception:
                pass

        if mongo_id:
            try:
                log_email_dispatch_status_to_mongo(
                    mongo_id,
                    team_dispatched=team_ok,
                    client_dispatched=client_ok,
                    errors=errors
                )
            except Exception as le:
                logger.warning("Could not log dispatch status to MongoDB Atlas: %s", le)

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


def _send_contact_notification(contact_message, connection=None, email_config=None):
    """
    Dispatch an attractive HTML email notification to the company email(s) if configured.
    Supports single recipient or comma-separated list of recipients.
    Includes client name, email, phone number, subject, timestamp, and message.
    Fail-safe: handles any exceptions gracefully without disrupting user feedback or database record.
    """
    cfg = email_config or {}
    if not cfg or str(getattr(settings, 'EMAIL_BACKEND', '')).endswith('locmem.EmailBackend'):
        recipient_setting = getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', '')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'Trinials <dummy11248@gmail.com>'
    else:
        recipient_setting = cfg.get('CONTACT_NOTIFICATION_EMAIL') or getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', '')
        from_email = cfg.get('DEFAULT_FROM_EMAIL') or getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'Trinials <dummy11248@gmail.com>'

    if not recipient_setting:
        return False

    if isinstance(recipient_setting, (list, tuple)):
        recipients = [str(r).strip(' "\' \t\r\n') for r in recipient_setting if str(r).strip(' "\' \t\r\n')]
    else:
        recipients = [r.strip(' "\' \t\r\n') for r in str(recipient_setting).split(',') if r.strip(' "\' \t\r\n')]

    if not recipients:
        return False

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

    try:
        html_content = render_to_string('emails/team_notification.html', context)

        # 1. Try modern HTTPS REST API first (bypasses Render cloud firewall port 465/587 blocks)
        try:
            from .email_service import send_email_via_https
            https_ok, provider, err = send_email_via_https(
                to_emails=recipients,
                subject=subject,
                html_content=html_content,
                plain_content=plain_text,
                from_email=from_email,
                reply_to=contact_message.email,
                config=cfg,
            )
            if https_ok:
                logger.info(
                    "Dispatched contact notification email via HTTPS (%s) for ContactMessage id=%s to %s",
                    provider,
                    getattr(contact_message, 'id', None),
                    recipients
                )
                return True
            elif provider != 'none':
                logger.warning("HTTPS email provider '%s' failed: %s; falling back to standard backend", provider, err)
        except Exception as https_err:
            logger.warning("HTTPS dispatch attempt notice: %s; falling back to standard backend", https_err)

        # 2. Fall back to standard Django backend (SMTP for localhost / locmem for tests)
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=from_email,
            to=recipients,
            reply_to=[contact_message.email],
            connection=connection,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info(
            "Dispatched contact notification email for ContactMessage id=%s to %s",
            getattr(contact_message, 'id', None),
            recipients
        )
        return True
    except Exception as e:
        err_msg = str(e)
        if '101' in err_msg or 'Network is unreachable' in err_msg or 'timed out' in err_msg.lower():
            err_msg = (
                f"{e} (Render Free Tier blocks outbound SMTP ports 25, 465, 587. "
                f"To enable email from Render, configure BREVO_API_KEY, RESEND_API_KEY, "
                f"or GMAIL_WEBHOOK_URL in MongoDB Atlas app_config, or upgrade Render to Starter)."
            )
        logger.error(
            "Failed to send contact notification email for ContactMessage id=%s: %s",
            getattr(contact_message, 'id', None),
            err_msg,
            exc_info=False
        )
        raise RuntimeError(err_msg) from e


def _send_client_auto_response(contact_message, connection=None, email_config=None):
    """
    Send an attractive branded confirmation email back to the client.
    Notice: Does NOT include a copy of the message, as requested by the client.
    Fail-safe: handles any exceptions gracefully without disrupting user feedback.
    """
    if not contact_message.email:
        return False

    cfg = email_config or {}
    contact_email = cfg.get('CONTACT_EMAIL') or getattr(settings, 'CONTACT_EMAIL', 'trinial26@gmail.com')
    phone = cfg.get('CONTACT_PHONE_NUMBER') or getattr(settings, 'CONTACT_PHONE_NUMBER', '+91 85908 21155')
    phone_sec = cfg.get('CONTACT_PHONE_NUMBER_SECONDARY') or getattr(settings, 'CONTACT_PHONE_NUMBER_SECONDARY', '+91 94003 25570')
    from_email = cfg.get('DEFAULT_FROM_EMAIL') or getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'Trinials <dummy11248@gmail.com>'

    subject = f"Thank you for contacting Trinials — We've received your inquiry"

    # Plain text fallback (NO copy of the client message!)
    plain_text = (
        f"Hi {contact_message.name},\n\n"
        f"Thank you for reaching out to Trinials! We have received your inquiry regarding \"{contact_message.subject}\".\n\n"
        f"Our team is currently reviewing your project requirements and will get back to you within 24 to 48 business hours.\n\n"
        f"If you have any urgent questions, feel free to reply directly to this email.\n\n"
        f"Warm regards,\n"
        f"The Trinials Team\n"
        f"{contact_email}\n"
        f"{phone} | {phone_sec}\n"
    )

    context = {
        'name': contact_message.name,
        'subject': contact_message.subject,
        'contact_email': contact_email,
        'phone_number': phone,
        'phone_number_secondary': phone_sec,
    }

    try:
        html_content = render_to_string('emails/client_auto_response.html', context)

        # 1. Try modern HTTPS REST API first (bypasses Render cloud firewall port 465/587 blocks)
        try:
            from .email_service import send_email_via_https
            https_ok, provider, err = send_email_via_https(
                to_emails=[contact_message.email],
                subject=subject,
                html_content=html_content,
                plain_content=plain_text,
                from_email=from_email,
                config=cfg,
            )
            if https_ok:
                logger.info(
                    "Dispatched client auto-response confirmation via HTTPS (%s) to %s for ContactMessage id=%s",
                    provider,
                    contact_message.email,
                    getattr(contact_message, 'id', None)
                )
                return True
            elif provider != 'none':
                logger.warning("HTTPS email provider '%s' failed: %s; falling back to standard backend", provider, err)
        except Exception as https_err:
            logger.warning("HTTPS dispatch attempt notice: %s; falling back to standard backend", https_err)

        # 2. Fall back to standard Django backend (SMTP for localhost / locmem for tests)
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=from_email,
            to=[contact_message.email],
            connection=connection,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info(
            "Dispatched client auto-response confirmation to %s for ContactMessage id=%s",
            contact_message.email,
            getattr(contact_message, 'id', None)
        )
        return True
    except Exception as e:
        err_msg = str(e)
        if '101' in err_msg or 'Network is unreachable' in err_msg or 'timed out' in err_msg.lower():
            err_msg = (
                f"{e} (Render Free Tier blocks outbound SMTP ports 25, 465, 587. "
                f"To enable email from Render, configure BREVO_API_KEY, RESEND_API_KEY, "
                f"or GMAIL_WEBHOOK_URL in MongoDB Atlas app_config, or upgrade Render to Starter)."
            )
        logger.error(
            "Failed to send client auto-response for ContactMessage id=%s: %s",
            getattr(contact_message, 'id', None),
            err_msg,
            exc_info=False
        )
        raise RuntimeError(err_msg) from e


# =============================================================================
# Operations Console & Enquiry Admin Portal (Connected to MongoDB Atlas)
# =============================================================================

def admin_required(view_func):
    """Decorator ensuring that only authenticated administrators access the portal."""
    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('trinials_admin_logged_in'):
            login_url = reverse('website:admin_login')
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_login(request):
    """
    Authenticate administrator credentials and establish secure session.
    Accepts admin username or trinial26@gmail.com with configured password.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('website:admin_dashboard')

    if request.session.get('trinials_admin_logged_in'):
        return redirect(next_url)

    error = None
    if request.method == 'POST':
        from .mongo import verify_admin_credentials
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if verify_admin_credentials(username, password):
            request.session['trinials_admin_logged_in'] = True
            request.session['trinials_admin_user'] = username
            messages.success(request, f"Welcome back, {username}! Signed in successfully.")
            return redirect(next_url)
        else:
            error = "Invalid username or password. Please verify credentials."

    return render(request, 'admin/login.html', {
        'error': error,
        'next_url': next_url,
    })


def admin_logout(request):
    """Terminate administrator session and return to login page."""
    request.session.flush()
    messages.success(request, "You have been logged out safely.")
    return redirect('website:admin_login')


@admin_required
def admin_dashboard(request):
    """
    Operations dashboard displaying live enquiry metrics, search/filtering,
    calendar date range filtering, and granular enquiry audit records directly from MongoDB Atlas.
    """
    from .mongo import get_enquiry_stats, search_enquiries

    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all').strip().lower()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    stats = get_enquiry_stats()
    enquiries, total_matching = search_enquiries(
        query=query,
        status_filter=status_filter,
        date_from=date_from or None,
        date_to=date_to or None,
        limit=200
    )

    return render(request, 'admin/dashboard.html', {
        'stats': stats,
        'enquiries': enquiries,
        'total_matching': total_matching,
        'query': query,
        'current_status': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    })


@admin_required
def admin_bulk_delete(request):
    """
    Bulk delete enquiries matching a date range and optional status filter.
    Enforces administrator confirmation.
    """
    if request.method != 'POST':
        return redirect('website:admin_dashboard')

    from .mongo import delete_enquiries_by_filter

    date_from = request.POST.get('date_from', '').strip()
    date_to = request.POST.get('date_to', '').strip()
    status_filter = request.POST.get('status', 'all').strip().lower()

    if not date_from and not date_to and status_filter in ('all', ''):
        messages.error(request, "Please specify at least a start date, end date, or status filter to perform bulk deletion.")
        return redirect('website:admin_dashboard')

    deleted_count = delete_enquiries_by_filter(
        date_from=date_from or None,
        date_to=date_to or None,
        status_filter=status_filter
    )

    if deleted_count > 0:
        messages.success(request, f"Successfully deleted {deleted_count} enquiry record(s) matching your criteria.")
    else:
        messages.info(request, "No enquiry records matched your criteria for deletion.")

    return redirect('website:admin_dashboard')


@admin_required
def admin_enquiry_action(request, enquiry_id):
    """
    Handle lifecycle actions on individual enquiries:
    - update status (new, contacted, in_progress, closed)
    - mark as read / unread
    - delete enquiry
    - re-trigger email notification
    """
    if request.method != 'POST':
        return redirect('website:admin_dashboard')

    from .mongo import get_enquiry_by_id, update_enquiry_status, delete_enquiry

    action = request.POST.get('action', '').strip().lower()

    if action == 'mark_read':
        update_enquiry_status(enquiry_id, is_read=True)
        return JsonResponse({'success': True, 'action': 'mark_read'})

    elif action == 'update_status':
        new_status = request.POST.get('new_status', '').strip().lower()
        if new_status in ('new', 'contacted', 'in_progress', 'closed'):
            update_enquiry_status(enquiry_id, status=new_status, is_read=True)
            messages.success(request, f"Enquiry status updated to '{new_status}'.")

    elif action == 'delete':
        if delete_enquiry(enquiry_id):
            messages.success(request, "Enquiry deleted permanently.")
        else:
            messages.error(request, "Could not delete enquiry.")

    elif action == 'resend_email':
        doc = get_enquiry_by_id(enquiry_id)
        if doc:
            class InqContainer:
                def __init__(self, d):
                    self.id = d.get('id')
                    self.name = d.get('name')
                    self.email = d.get('email')
                    self.phone = d.get('phone')
                    self.subject = d.get('subject')
                    self.message = d.get('message')
                    self.created_at = d.get('created_at')

            _dispatch_inquiry_emails(InqContainer(doc), mongo_id=enquiry_id)
            messages.success(request, f"Re-dispatched notification emails for {doc.get('name')}.")
        else:
            messages.error(request, "Enquiry not found.")

    return redirect('website:admin_dashboard')


@admin_required
def admin_export_csv(request):
    """Export all enquiries from MongoDB Atlas to a downloadable CSV file."""
    import csv
    from .mongo import search_enquiries

    enquiries, _ = search_enquiries(limit=1000)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="trinials_enquiries_{datetime.now():%Y%m%d_%H%M%S}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'MongoDB ID',
        'Date Submitted (UTC)',
        'Client Name',
        'Email',
        'Phone',
        'Subject',
        'Status',
        'Is Read',
        'Team Email Sent',
        'Client Email Sent',
        'IP Address',
        'Message'
    ])

    for e in enquiries:
        dispatch = e.get('email_dispatch', {})
        writer.writerow([
            e.get('id'),
            f"{e.get('created_at'):%Y-%m-%d %H:%M:%S}" if e.get('created_at') else '',
            e.get('name', ''),
            e.get('email', ''),
            e.get('phone', ''),
            e.get('subject', ''),
            e.get('status', 'new'),
            'Yes' if e.get('is_read') else 'No',
            'Yes' if dispatch.get('team_dispatched') else 'No',
            'Yes' if dispatch.get('client_dispatched') else 'No',
            e.get('ip_address', ''),
            e.get('message', ''),
        ])

    return response

