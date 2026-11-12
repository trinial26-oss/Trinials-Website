import os
import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger('website.email')


def send_email_via_https(to_emails, subject, html_content, plain_content="", from_email=None, reply_to=None, config=None):
    """
    Send emails via HTTPS (Port 443) using modern REST APIs.
    Bypasses cloud provider firewall restrictions on outbound SMTP ports (25, 465, 587)
    such as those on Render.com Free tier.

    Supported providers (checked in priority order):
    1. Brevo API (BREVO_API_KEY)
    2. Resend API (RESEND_API_KEY)
    3. Google Apps Script HTTPS Webhook (GMAIL_WEBHOOK_URL)

    Returns:
        tuple (success: bool, provider: str, error_msg: str)
    """
    cfg = config or {}

    # Extract API keys from config (MongoDB Atlas) or environment
    brevo_key = cfg.get('BREVO_API_KEY') or os.environ.get('BREVO_API_KEY', '').strip()
    resend_key = cfg.get('RESEND_API_KEY') or os.environ.get('RESEND_API_KEY', '').strip()
    webhook_url = cfg.get('GMAIL_WEBHOOK_URL') or os.environ.get('GMAIL_WEBHOOK_URL', '').strip()

    if isinstance(to_emails, str):
        recipients = [r.strip() for r in to_emails.split(',') if r.strip()]
    else:
        recipients = [str(r).strip() for r in to_emails if str(r).strip()]

    if not recipients:
        return False, 'none', 'No recipient email addresses provided'

    from_addr = from_email or cfg.get('DEFAULT_FROM_EMAIL') or os.environ.get('DEFAULT_FROM_EMAIL', 'Trinials <dummy11248@gmail.com>')

    # -------------------------------------------------------------------------
    # 1. Brevo API (https://api.brevo.com/v3/smtp/email) - Generous 300 emails/day free
    # -------------------------------------------------------------------------
    if brevo_key:
        sender_name = 'Trinials'
        sender_email = 'dummy11248@gmail.com'
        if '<' in from_addr and '>' in from_addr:
            sender_name = from_addr.split('<')[0].strip()
            sender_email = from_addr.split('<')[1].replace('>', '').strip()
        elif '@' in from_addr:
            sender_email = from_addr.strip()

        payload = {
            'sender': {'name': sender_name, 'email': sender_email},
            'to': [{'email': r} for r in recipients],
            'subject': subject,
            'htmlContent': html_content,
        }
        if plain_content:
            payload['textContent'] = plain_content
        if reply_to:
            payload['replyTo'] = {'email': reply_to if isinstance(reply_to, str) else reply_to[0]}

        try:
            req = urllib.request.Request(
                'https://api.brevo.com/v3/smtp/email',
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'api-key': brevo_key,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'Trinials-Portal/4.0',
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                if 200 <= resp.status < 300:
                    logger.info("Successfully dispatched email via Brevo HTTPS API to %s", recipients)
                    return True, 'brevo', ''
                return False, 'brevo', f"Brevo HTTP {resp.status}"
        except urllib.error.HTTPError as he:
            body = he.read().decode('utf-8', errors='ignore')
            err_msg = f"Brevo API error {he.code}: {body}"
            logger.error(err_msg)
            return False, 'brevo', err_msg
        except Exception as e:
            err_msg = f"Brevo request failed: {e}"
            logger.error(err_msg)
            return False, 'brevo', err_msg

    # -------------------------------------------------------------------------
    # 2. Resend API (https://api.resend.com/emails) - 3,000 emails/month free
    # -------------------------------------------------------------------------
    if resend_key:
        payload = {
            'from': from_addr,
            'to': recipients,
            'subject': subject,
            'html': html_content,
        }
        if plain_content:
            payload['text'] = plain_content
        if reply_to:
            payload['reply_to'] = reply_to if isinstance(reply_to, str) else reply_to[0]

        try:
            req = urllib.request.Request(
                'https://api.resend.com/emails',
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Authorization': f"Bearer {resend_key}",
                    'Content-Type': 'application/json',
                    'User-Agent': 'Trinials-Portal/4.0',
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                if 200 <= resp.status < 300:
                    logger.info("Successfully dispatched email via Resend HTTPS API to %s", recipients)
                    return True, 'resend', ''
                return False, 'resend', f"Resend HTTP {resp.status}"
        except urllib.error.HTTPError as he:
            body = he.read().decode('utf-8', errors='ignore')
            err_msg = f"Resend API error {he.code}: {body}"
            logger.error(err_msg)
            return False, 'resend', err_msg
        except Exception as e:
            err_msg = f"Resend request failed: {e}"
            logger.error(err_msg)
            return False, 'resend', err_msg

    # -------------------------------------------------------------------------
    # 3. Google Apps Script HTTPS Webhook (Sends via personal/workspace Gmail inbox)
    # -------------------------------------------------------------------------
    if webhook_url:
        webhook_secret = cfg.get('GMAIL_WEBHOOK_SECRET') or os.environ.get('GMAIL_WEBHOOK_SECRET', '').strip()
        payload = {
            'secret': webhook_secret,
            'to': recipients,
            'subject': subject,
            'html': html_content,
            'text': plain_content,
        }
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Trinials-Portal/4.0',
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                if 200 <= resp.status < 300:
                    logger.info("Successfully dispatched email via Google Apps Script HTTPS Relay to %s", recipients)
                    return True, 'google_apps_script', ''
                return False, 'google_apps_script', f"Google Webhook HTTP {resp.status}"
        except Exception as e:
            err_msg = f"Google Apps Script relay failed: {e}"
            logger.error(err_msg)
            return False, 'google_apps_script', err_msg

    return False, 'none', 'No HTTPS email provider configured (checked BREVO_API_KEY, RESEND_API_KEY, GMAIL_WEBHOOK_URL)'
