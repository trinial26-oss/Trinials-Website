from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.staticfiles import finders


class WebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_status_code(self):
        """Verify that the homepage URL returns HTTP 200 OK."""
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        """Verify that the homepage view renders base.html."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'base.html')

    def test_homepage_contains_expected_title(self):
        """Verify that the rendered homepage contains the Trinials title."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, '<title>Trinials | Web Development & Digital Solutions Company in Kerala</title>')

    def test_navbar_component_included(self):
        """Verify that the navbar component is included in rendered pages."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'components/navbar.html')
        self.assertContains(response, '<header class="site-header"')
        self.assertContains(response, '<nav class="navbar"')

    def test_navbar_brand_logo(self):
        """Verify that the brand wordmark links to homepage and has the blue dot."""
        response = self.client.get(reverse('website:home'))
        home_url = reverse('website:home')
        self.assertContains(response, f'href="{home_url}"')
        self.assertContains(response, 'class="brand-logo"')
        self.assertContains(response, 'alt="Trinials"')

    def test_navbar_navigation_links(self):
        """Verify that all required desktop and mobile navigation links exist."""
        response = self.client.get(reverse('website:home'))
        for link_text in ['Home', 'About', 'Services', 'Work', 'Process', 'Contact']:
            self.assertContains(response, link_text)

    def test_navbar_cta_button(self):
        """Verify that the Let's Talk CTA button is present with arrow."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, "Let's Talk")
        self.assertContains(response, 'btn-nav-cta')

    def test_hero_section_included(self):
        """Verify that the hero section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/hero.html')
        self.assertContains(response, '<section class="hero-section"')

    def test_hero_content_and_typography(self):
        """Verify introductory label, headline, and supporting description."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'CREATIVE MINDS. FRESH PERSPECTIVES.')
        self.assertContains(response, '<h1 id="hero-heading"')
        self.assertContains(response, 'Good ideas deserve')
        self.assertContains(response, 'a beautiful')
        self.assertContains(response, 'beginning')
        self.assertContains(response, 'At Trinials, we bring creativity, fresh perspectives')

    def test_hero_action_buttons(self):
        """Verify primary and secondary CTA buttons in the hero section."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'Explore Our Work')
        self.assertContains(response, 'href="#work"')
        self.assertContains(response, 'Get to Know Us')
        self.assertContains(response, 'href="#about"')

    def test_hero_visual_composition(self):
        """Verify the artistic visual composition container is present."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'class="hero-visual"')
        self.assertContains(response, 'visual-canvas')
        self.assertContains(response, 'visual-arch')

    def test_about_section_included(self):
        """Verify that the about section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/about.html')
        self.assertContains(response, '<section class="about-section" id="about"')

    def test_about_content_and_typography(self):
        """Verify eyebrow label, heading, paragraphs, and action link."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'A LITTLE ABOUT US')
        self.assertContains(response, '<h2 id="about-heading"')
        self.assertContains(response, 'We see things a little differently')
        self.assertContains(response, 'Trinials is built around fresh perspectives')
        self.assertContains(response, "We believe good work doesn't need to be complicated")
        self.assertContains(response, 'More About Our Approach')

    def test_about_visual_and_principles(self):
        """Verify visual statement card and supporting three principles."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'Fresh ideas.')
        self.assertContains(response, 'Thoughtful execution.')
        self.assertContains(response, 'Curiosity')
        self.assertContains(response, 'We look beyond the obvious.')
        self.assertContains(response, 'Clarity')
        self.assertContains(response, 'We make ideas easier to understand.')
        self.assertContains(response, 'Care')
        self.assertContains(response, 'We pay attention to the details.')

    def test_services_section_included(self):
        """Verify that the services section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/services.html')
        self.assertContains(response, '<section class="services-section" id="services"')

    def test_services_content_and_items(self):
        """Verify services eyebrow, heading, intro text, and all four service items."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'WHAT WE DO')
        self.assertContains(response, '<h2 id="services-heading"')
        self.assertContains(response, 'Ideas become meaningful when they take shape')
        self.assertContains(response, 'From the first spark of an idea to the final details')

        # Service 01: Web Development
        self.assertContains(response, '01')
        self.assertContains(response, 'Web Development')
        self.assertContains(response, 'We build responsive, reliable websites that bring ideas to life')

        # Service 02: UI/UX Design
        self.assertContains(response, '02')
        self.assertContains(response, 'UI/UX Design')
        self.assertContains(response, 'We design clear, intuitive experiences that put people first')

        # Service 03: Brand Identity
        self.assertContains(response, '03')
        self.assertContains(response, 'Brand Identity')
        self.assertContains(response, 'We help shape distinctive visual identities that communicate who you are')

        # Service 04: Digital Solutions
        self.assertContains(response, '04')
        self.assertContains(response, 'Digital Solutions')
        self.assertContains(response, 'We explore practical digital ideas and create solutions that address real needs')

    def test_work_section_included(self):
        """Verify that the work section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/work.html')
        self.assertContains(response, '<section class="work-section" id="work"')

    def test_work_content_and_projects(self):
        """Verify work eyebrow, heading, intro text, and all completed live projects."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, "A FEW THINGS WE'VE MADE")
        self.assertContains(response, '<h2 id="work-heading"')
        self.assertContains(response, 'Work that speaks for itself')

        # Major Project: Cherupuzha River Rafting
        self.assertContains(response, 'Cherupuzha River Rafting')
        self.assertContains(response, 'cherupuzhariverrafting.in')
        self.assertContains(response, 'Web Platform &bull; Tourism &amp; Adventure')
        self.assertContains(response, 'Live Website')
        self.assertContains(response, 'images/work/cherupuzha-river-rafting.jpg')
        self.assertContains(response, 'work-item-featured')

        # Project 02: FancyStore
        self.assertContains(response, 'FancyStore')
        self.assertContains(response, 'E-Commerce Platform &bull; Retail')
        self.assertContains(response, 'images/work/fancy-store.jpg')

        # Project 03: ElectroKart ERP
        self.assertContains(response, 'ElectroKart (ERP &amp; Store)')
        self.assertContains(response, 'Web Platform &bull; ERP &amp; Inventory')
        self.assertContains(response, 'images/work/electrokart-erp.jpg')

    def test_process_section_included(self):
        """Verify that the process section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/process.html')
        self.assertContains(response, '<section class="process-section" id="process"')

    def test_process_content_and_steps(self):
        """Verify process eyebrow, heading, intro text, 4 steps in order, and supporting statement."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'HOW WE WORK')
        self.assertContains(response, '<h2 id="process-heading"')
        self.assertContains(response, 'A good idea deserves a thoughtful process')
        self.assertContains(response, 'Every project is different, but our approach stays grounded in curiosity')

        # Step 01: Discover
        self.assertContains(response, '01')
        self.assertContains(response, 'Discover')
        self.assertContains(response, 'We start by listening. We learn about your goals')

        # Step 02: Define
        self.assertContains(response, '02')
        self.assertContains(response, 'Define')
        self.assertContains(response, 'We bring clarity to the idea, shape the direction')

        # Step 03: Create
        self.assertContains(response, '03')
        self.assertContains(response, 'Create')
        self.assertContains(response, 'We turn the direction into something real through thoughtful design')

        # Step 04: Deliver
        self.assertContains(response, '04')
        self.assertContains(response, 'Deliver')
        self.assertContains(response, 'We refine the details, bring everything together')

        # Supporting statement
        self.assertContains(response, 'Good work happens when everyone is part of the process.')

    def test_testimonials_section_not_included(self):
        """Verify that the testimonials / kind words section has been cleanly removed from the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertNotContains(response, 'id="testimonials"')
        self.assertNotContains(response, 'KIND WORDS')
        self.assertNotContains(response, "Good work is better when it's shared")
        self.assertNotContains(response, 'Alex Morgan')
        self.assertNotContains(response, 'Jamie Taylor')
        self.assertNotContains(response, 'Riley Parker')

    def test_contact_section_included(self):
        """Verify that the contact section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/contact.html')
        self.assertContains(response, '<section class="contact-section" id="contact"')

    def test_contact_content_and_form_accessibility(self):
        """Verify eyebrow, heading, intro text, CTA button, contact info, and form fields with labels."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, "LET'S TALK")
        self.assertContains(response, '<h2 id="contact-heading"')
        self.assertContains(response, 'Have an idea in mind')
        self.assertContains(response, "We'd love to hear what you're thinking")
        self.assertContains(response, 'Start a Conversation')

        # Contact Info Placeholders
        self.assertContains(response, 'Direct Inquiries')
        self.assertContains(response, 'trinial26@gmail.com')
        self.assertContains(response, '85908 21155')
        self.assertContains(response, '94003 25570')
        self.assertContains(response, 'Response Commitment')

        # Form fields with corresponding accessible labels
        self.assertContains(response, '<form class="contact-form" id="contact-form"')
        self.assertContains(response, '<label for="contact-name"')
        self.assertContains(response, 'id="contact-name"')
        self.assertContains(response, '<label for="contact-email"')
        self.assertContains(response, 'id="contact-email"')
        self.assertContains(response, 'type="email"')
        self.assertContains(response, '<label for="contact-subject"')
        self.assertContains(response, 'id="contact-subject"')
        self.assertContains(response, '<label for="contact-message"')
        self.assertContains(response, 'id="contact-message"')
        self.assertContains(response, 'Send Message')

    def test_design_preview_status_code(self):
        """Verify that the design preview route returns HTTP 200 OK."""
        response = self.client.get(reverse('website:design_preview'))
        self.assertEqual(response.status_code, 200)

    def test_all_static_assets_exist(self):
        """Verify that all CSS and JS assets are found by Django staticfiles finders."""
        static_files = [
            'css/variables.css',
            'css/reset.css',
            'css/typography.css',
            'css/layout.css',
            'css/components.css',
            'css/responsive.css',
            'css/navbar.css',
            'css/hero.css',
            'css/about.css',
            'css/services.css',
            'css/work.css',
            'css/process.css',
            'css/testimonials.css',
            'css/contact.css',
            'css/footer.css',
            'js/navigation.js',
        ]
        for static_file in static_files:
            result = finders.find(static_file)
            self.assertIsNotNone(result, f"Static asset missing: {static_file}")

    def test_footer_section_included(self):
        """Verify that the footer section template is rendered on the homepage."""
        response = self.client.get(reverse('website:home'))
        self.assertTemplateUsed(response, 'sections/footer.html')
        self.assertContains(response, '<footer class="site-footer" id="site-footer"')
        self.assertContains(response, 'css/footer.css')

    def test_footer_brand_and_navigation_links(self):
        """Verify brand logo, tagline, and all required section navigation links."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'footer-brand')
        self.assertContains(response, 'Complex Made Simple. Growth Made Possible.')

        # Verify semantic navigation element and links to existing homepage sections
        self.assertContains(response, '<nav class="footer-navigation"')
        expected_links = [
            ('Home', '#hero'),
            ('About', '#about'),
            ('Services', '#services'),
            ('Work', '#work'),
            ('Process', '#process'),
            ('Contact', '#contact'),
        ]
        for label, target_id in expected_links:
            self.assertContains(response, f'href="{target_id}"')
            self.assertContains(response, label)

    def test_footer_bottom_and_dynamic_copyright(self):
        """Verify dynamic current year in copyright and smooth Back to top link."""
        response = self.client.get(reverse('website:home'))
        current_year = str(datetime.now().year)
        self.assertContains(response, f'{current_year} Trinials. All rights reserved.')
        self.assertContains(response, 'Back to top')
        self.assertContains(response, 'href="#top"')


    def test_homepage_section_order(self):
        """Verify that sections appear in the strict expected order on the homepage."""
        response = self.client.get(reverse('website:home'))
        html = response.content.decode('utf-8')

        ordered_markers = [
            'id="site-header"',
            'id="hero"',
            'id="about"',
            'id="services"',
            'id="work"',
            'id="process"',
            'id="contact"',
            'id="site-footer"',
        ]

        last_index = -1
        for marker in ordered_markers:
            index = html.find(marker)
            self.assertNotEqual(index, -1, f"Marker missing from rendered homepage: {marker}")
            self.assertGreater(index, last_index, f"Marker {marker} out of order (found at {index}, previous at {last_index})")
            last_index = index

    def test_homepage_sections_included_once(self):
        """Verify that each section is included exactly once without duplication."""
        response = self.client.get(reverse('website:home'))
        html = response.content.decode('utf-8')

        section_ids = ['hero', 'about', 'services', 'work', 'process', 'contact', 'site-footer']
        for sid in section_ids:
            count = html.count(f'id="{sid}"')
            self.assertEqual(count, 1, f"Section id='{sid}' appeared {count} times (expected exactly 1)")

    def test_layout_scroll_margin_defined(self):
        """Verify that layout.css defines scroll-margin-top for sticky header compensation."""
        with open('static/css/layout.css', 'r', encoding='utf-8') as f:
            layout_css = f.read()
        self.assertIn('scroll-margin-top', layout_css)


    def test_all_homepage_anchors_resolve_to_existing_elements(self):
        """Verify that every anchor in the navbar, hero, about, footer, etc. targets an existing ID."""
        response = self.client.get(reverse('website:home'))
        html = response.content.decode('utf-8')

        import re
        anchor_targets = set(re.findall(r'href="#([^"]+)"', html))
        element_ids = set(re.findall(r'id="([^"]+)"', html))

        for target in anchor_targets:
            self.assertIn(target, element_ids, f"Anchor #{target} has no matching element id in DOM")

    def test_contact_form_structure_and_action(self):
        """Verify that the contact form posts to the contact endpoint and has CSRF protection."""
        response = self.client.get(reverse('website:home'))
        contact_url = reverse('website:contact')
        self.assertContains(response, f'action="{contact_url}"')
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'name="website_hp"')

    def test_contact_form_valid_submission(self):
        """Verify that submitting valid data creates a database record, redirects, and shows success message."""
        from website.models import ContactMessage
        payload = {
            'name': 'Sarah Connor',
            'email': 'sarah@example.com',
            'phone': '+1 (555) 019-2834',
            'subject': 'Digital Brand Architecture',
            'message': 'We are looking for creative partners to design our new digital platform.',
            'website_hp': '',
        }
        response = self.client.post(reverse('website:contact'), data=payload, follow=True)

        self.assertRedirects(response, reverse('website:home') + '#contact')

        # Verify DB entry
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Sarah Connor')
        self.assertEqual(msg.email, 'sarah@example.com')
        self.assertEqual(msg.phone, '+1 (555) 019-2834')
        self.assertEqual(msg.subject, 'Digital Brand Architecture')
        self.assertEqual(msg.message, payload['message'])
        self.assertFalse(msg.is_read)

        # Verify success message displayed after redirect
        self.assertContains(response, "Thanks for reaching out. Your message has been received")
        self.assertContains(response, "we&#x27;ll be in touch soon.")

    def test_contact_form_empty_submission_rejected(self):
        """Verify that empty form submission is rejected and creates no DB record."""
        from website.models import ContactMessage
        response = self.client.post(reverse('website:contact'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, 'Please check the form below and correct any errors.')

    def test_contact_form_invalid_email_rejected(self):
        """Verify that invalid email addresses are rejected with field errors."""
        from website.models import ContactMessage
        payload = {
            'name': 'John Doe',
            'email': 'not-an-email',
            'phone': '+1 (555) 019-2834',
            'subject': 'Inquiry',
            'message': 'Testing invalid email rejection.',
        }
        response = self.client.post(reverse('website:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, 'Please enter a valid email address')

    def test_contact_form_phone_validation(self):
        """Verify that phone numbers are strictly validated."""
        from website.models import ContactMessage

        # Test invalid phone (letters or too short)
        payload = {
            'name': 'Ada Lovelace',
            'email': 'ada@analytics.org',
            'phone': 'not-a-phone',
            'subject': 'Analytical Engine',
            'message': 'Discussing punch cards.',
        }
        response = self.client.post(reverse('website:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, 'Please enter a valid phone number.')

        # Test missing phone
        payload['phone'] = ''
        response = self.client.post(reverse('website:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, 'Please provide your phone number.')

    def test_contact_form_whitespace_only_rejected(self):
        """Verify that whitespace-only values are treated as empty and rejected."""
        from website.models import ContactMessage
        payload = {
            'name': '   ',
            'email': 'john@example.com',
            'phone': '   ',
            'subject': '   ',
            'message': '   ',
        }
        response = self.client.post(reverse('website:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_form_preserves_valid_input_on_validation_failure(self):
        """Verify that valid fields retain their values when another field fails validation."""
        payload = {
            'name': 'Elena Rostova',
            'email': 'invalid-email',
            'phone': '+1 (555) 019-2834',
            'subject': 'Enterprise Systems Inquiry',
            'message': 'Preserve this message content.',
        }
        response = self.client.post(reverse('website:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Elena Rostova')
        self.assertContains(response, '+1 (555) 019-2834')
        self.assertContains(response, 'Enterprise Systems Inquiry')
        self.assertContains(response, 'Preserve this message content.')

    def test_contact_form_honeypot_bot_rejection(self):
        """Verify that filling the hidden honeypot rejects the submission as spam."""
        from website.models import ContactMessage
        payload = {
            'name': 'Bot Spammer',
            'email': 'bot@spammer.org',
            'phone': '+1 (555) 019-2834',
            'subject': 'Buy Crypto Now',
            'message': 'Spam message text.',
            'website_hp': 'http://spam-link.ru',
        }
        response = self.client.post(reverse('website:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_get_request_redirects_to_home(self):
        """Verify that hitting GET on /contact/ redirects gracefully to homepage contact section."""
        response = self.client.get(reverse('website:contact'))
        self.assertRedirects(response, reverse('website:home') + '#contact')

    def test_contact_admin_integration(self):
        """Verify that ContactMessage is registered in admin with search, filter, and read actions."""
        from django.contrib.auth.models import User
        from website.models import ContactMessage

        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
        self.client.login(username='admin', password='adminpass123')

        msg = ContactMessage.objects.create(
            name='Arthur Dent',
            email='arthur@earth.galaxy',
            phone='+1 (555) 424-2424',
            subject='Towel Request',
            message='Don’t panic.'
        )

        changelist_url = '/admin/website/contactmessage/'
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Arthur Dent')
        self.assertContains(response, 'Towel Request')

        # Test mark_as_read action
        post_data = {
            'action': 'mark_as_read',
            '_selected_action': [msg.pk],
        }
        self.client.post(changelist_url, data=post_data)
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

        # Test mark_as_unread action
        post_data['action'] = 'mark_as_unread'
        self.client.post(changelist_url, data=post_data)
        msg.refresh_from_db()
        self.assertFalse(msg.is_read)

    def test_contact_email_notification_dispatch(self):
        """Verify email notification dispatch when CONTACT_NOTIFICATION_EMAIL is configured."""
        from django.core import mail
        from django.test import override_settings
        from website.models import ContactMessage

        with override_settings(
            CONTACT_NOTIFICATION_EMAIL='team@millennials.placeholder',
            DEFAULT_FROM_EMAIL='system@millennials.placeholder'
        ):
            payload = {
                'name': 'David Bowie',
                'email': 'david@starman.org',
                'phone': '+1 (555) 019-2834',
                'subject': 'Space Oddity',
                'message': 'Ground Control to Major Tom.',
            }
            response = self.client.post(reverse('website:contact'), data=payload)
            self.assertRedirects(response, reverse('website:home') + '#contact')

            # Verify emails sent (team notification + client auto-response)
            self.assertEqual(len(mail.outbox), 2)
            team_email = mail.outbox[0]
            self.assertEqual(team_email.to, ['team@millennials.placeholder'])
            self.assertEqual(team_email.reply_to, ['david@starman.org'])
            self.assertIn('David Bowie', team_email.subject)
            self.assertIn('Ground Control to Major Tom.', team_email.body)
            self.assertIn('+1 (555) 019-2834', team_email.body)

            client_email = mail.outbox[1]
            self.assertEqual(client_email.to, ['david@starman.org'])
            self.assertIn('Trinials', client_email.subject)
            self.assertIn('David Bowie', client_email.body)
            # Ensure copy of the message is NOT in the client auto-reply
            self.assertNotIn('Ground Control to Major Tom.', client_email.body)

    def test_contact_email_failure_does_not_abort_database_save(self):
        """Verify that an email dispatch failure does not lose the enquiry or crash the request."""
        from unittest.mock import patch
        from django.test import override_settings
        from website.models import ContactMessage

        with override_settings(CONTACT_NOTIFICATION_EMAIL='team@millennials.placeholder'):
            with patch('website.views.EmailMultiAlternatives.send', side_effect=Exception('SMTP server down')):
                payload = {
                    'name': 'Grace Hopper',
                    'email': 'grace@navy.mil',
                    'phone': '+1 (555) 019-2834',
                    'subject': 'Compiler Project',
                    'message': 'Need advice on nanoseconds.',
                }
                response = self.client.post(reverse('website:contact'), data=payload)
                self.assertRedirects(response, reverse('website:home') + '#contact')
                self.assertEqual(ContactMessage.objects.filter(name='Grace Hopper').count(), 1)

    def test_contact_ajax_submission_success(self):
        """Verify that an AJAX POST inquiry submission returns HTTP 200 with JSON payload."""
        from website.models import ContactMessage
        payload = {
            'name': 'Ada Lovelace',
            'email': 'ada@analytical.engine',
            'phone': '+44 20 7946 0991',
            'subject': 'Bernoulli Numbers Calculator',
            'message': 'We need an analytical computing engine interface.',
        }
        response = self.client.post(
            reverse('website:contact'),
            data=payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertIn('inquiry', json_data)
        self.assertEqual(json_data['inquiry']['name'], 'Ada Lovelace')
        self.assertEqual(json_data['inquiry']['phone'], '+44 20 7946 0991')
        self.assertEqual(ContactMessage.objects.filter(name='Ada Lovelace').count(), 1)

    def test_contact_ajax_submission_validation_error(self):
        """Verify that an invalid AJAX submission returns HTTP 400 with field errors JSON."""
        payload = {
            'name': '',
            'email': 'not-an-email',
            'phone': '',
            'subject': '',
            'message': '',
        }
        response = self.client.post(
            reverse('website:contact'),
            data=payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('errors', json_data)
        self.assertIn('email', json_data['errors'])

    def test_navbar_mobile_panel_overflow_resilience(self):
        """Verify that navbar.css configures overflow-y on mobile dropdown to prevent screen clipping."""
        with open('static/css/navbar.css', 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('overflow-y: auto;', css)
        self.assertIn('max-height: calc(100vh - 74px);', css)


    def test_custom_404_template_renders_on_not_found(self):
        """Verify custom 404 page renders without tracebacks when DEBUG=False."""
        from django.test import override_settings
        with override_settings(DEBUG=False):
            response = self.client.get('/this-path-does-not-exist-12345/')
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')
            self.assertContains(response, 'Page Not Found', status_code=404)
            self.assertContains(response, 'Return to Homepage', status_code=404)

    def test_custom_500_template_loads(self):
        """Verify custom 500 error template can be loaded and parsed cleanly."""
        from django.template.loader import get_template
        template = get_template('500.html')
        self.assertIsNotNone(template)
        rendered = template.render({'request': None})
        self.assertIn('Something went wrong', rendered)

    def test_collectstatic_dry_run_executes_cleanly(self):
        """Verify that Django can collect all static assets without missing source errors."""
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('collectstatic', interactive=False, dry_run=True, stdout=out)
        self.assertIn('static files copied', out.getvalue())

    def test_production_security_settings_configured(self):
        """Verify that production security and cookie settings are defined."""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'SECURE_SSL_REDIRECT'))
        self.assertTrue(hasattr(settings, 'SESSION_COOKIE_SECURE'))
        self.assertTrue(hasattr(settings, 'CSRF_COOKIE_SECURE'))
        self.assertTrue(hasattr(settings, 'LOGGING'))
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')

    def test_admin_url_accessible(self):
        """Verify that the Django admin URL is accessible (redirects to login)."""
        response = self.client.get('/admin/', follow=False)
        self.assertEqual(response.status_code, 302)

    def test_navbar_contact_dropdown_structure_and_accessibility(self):
        """Verify that the Let's Talk contact dropdown renders with proper semantic ARIA attributes."""
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

        # Desktop trigger & dropdown
        self.assertContains(response, 'id="nav-cta-trigger"')
        self.assertContains(response, 'aria-haspopup="true"')
        self.assertContains(response, 'aria-expanded="false"')
        self.assertContains(response, 'aria-controls="nav-contact-dropdown"')
        self.assertContains(response, 'id="nav-contact-dropdown"')
        self.assertContains(response, 'role="menu"')

        # Verify trigger & dropdown are in the top navbar actions and not duplicated in mobile panel
        self.assertContains(response, 'class="navbar-actions"')
        self.assertNotContains(response, 'id="mobile-nav-cta-trigger"')

        # Verify dropdown arrow in navbar CTA is replaced with chat icon
        self.assertContains(response, 'class="cta-chat-icon"')

        # Contact options labels and descriptions
        self.assertContains(response, 'WhatsApp')
        self.assertContains(response, 'Start a conversation')
        self.assertContains(response, 'Call')
        self.assertContains(response, 'Call us directly')

    def test_navbar_contact_dropdown_with_configured_contacts(self):
        """Verify that configured WhatsApp URL and phone number render correctly with target and tel: scheme."""
        from django.test import override_settings
        with override_settings(
            CONTACT_WHATSAPP_URL='https://wa.me/15551234567',
            CONTACT_PHONE_NUMBER='+15551234567'
        ):
            response = self.client.get(reverse('website:home'))
            self.assertContains(response, 'href="https://wa.me/15551234567"')
            self.assertContains(response, 'target="_blank"')
            self.assertContains(response, 'rel="noopener noreferrer"')
            self.assertContains(response, 'href="tel:+15551234567"')

    def test_navbar_contact_dropdown_unconfigured_fallback(self):
        """Verify that unconfigured contacts gracefully point to #contact without inventing dummy numbers."""
        from django.test import override_settings
        with override_settings(
            CONTACT_WHATSAPP_URL='',
            CONTACT_PHONE_NUMBER=''
        ):
            response = self.client.get(reverse('website:home'))
            self.assertContains(response, 'data-contact-action="whatsapp"')
            self.assertContains(response, 'data-contact-action="call"')
            # Ensure no fake dummy phone numbers are rendered
            self.assertNotContains(response, '+1-555')
            self.assertNotContains(response, '+1234567890')
            self.assertNotContains(response, 'href="tel:"')

    def test_navbar_css_and_js_dropdown_integration(self):
        """Verify that navbar.css and navigation.js contain styling and behavior for the contact dropdown."""
        with open('static/css/navbar.css', 'r', encoding='utf-8') as f:
            css = f.read()
        self.assertIn('.nav-contact-dropdown', css)
        self.assertIn('.nav-dropdown-wrapper', css)
        self.assertIn('.nav-contact-item', css)
        self.assertIn('.mobile-contact-dropdown', css)
        self.assertIn('.cta-chat-icon', css)

        with open('static/js/navigation.js', 'r', encoding='utf-8') as f:
            js = f.read()
        self.assertIn('initContactDropdowns', js)
        self.assertIn('nav-cta-trigger', js)
        self.assertIn('mobile-nav-cta-trigger', js)
        self.assertIn('Escape', js)
        self.assertIn('pointerdown', js)

    def test_about_page_renders_cleanly(self):
        """Verify dedicated About Us page renders with 200 OK and expected studio story content."""
        response = self.client.get(reverse('website:about_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about.html')
        self.assertContains(response, 'About Trinials')
        self.assertContains(response, 'Who We Are')
        self.assertContains(response, 'Our Core Principles')
        self.assertContains(response, 'trinial26@gmail.com')

    def test_privacy_policy_page_renders_cleanly(self):
        """Verify dedicated Privacy Policy page renders with 200 OK and expected legal content."""
        response = self.client.get(reverse('website:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/privacy_policy.html')
        self.assertContains(response, 'Privacy Policy')
        self.assertContains(response, 'Information We Collect')
        self.assertContains(response, 'No Spam Guarantee')
        self.assertContains(response, 'trinial26@gmail.com')
        self.assertContains(response, '85908 21155')

    def test_terms_conditions_page_renders_cleanly(self):
        """Verify dedicated Terms & Conditions page renders with 200 OK and expected legal content."""
        response = self.client.get(reverse('website:terms_conditions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/terms_conditions.html')
        self.assertContains(response, 'Terms &amp; Conditions')
        self.assertContains(response, 'Acceptance of Terms')
        self.assertContains(response, 'Studio Services &amp; Scope')
        self.assertContains(response, 'Intellectual Property Rights')
        self.assertContains(response, 'trinial26@gmail.com')

    def test_footer_contains_updated_contacts_and_legal_links(self):
        """Verify footer displays Trinials contact details and links to legal pages."""
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'trinial26@gmail.com')
        self.assertContains(response, '85908 21155')
        self.assertContains(response, '94003 25570')
        self.assertContains(response, reverse('website:about_page'))
        self.assertContains(response, reverse('website:privacy_policy'))
        self.assertContains(response, reverse('website:terms_conditions'))

    def test_contact_notification_multiple_recipients_dispatch(self):
        """Verify that newly requested recipient emails receive enquiry notifications."""
        from django.core import mail
        from django.test import override_settings

        with override_settings(
            CONTACT_NOTIFICATION_EMAIL='johnpaulalex85@gmail.com, trinial26@gmail.com, Jojogeorge.trinials@gmail.com, joejoseph1235@gmail.com'
        ):
            payload = {
                'name': 'Innovator Client',
                'email': 'client@innovate.org',
                'phone': '+91 98765 43210',
                'subject': 'Strategic Platform Build',
                'message': 'We need a full-stack digital solution crafted by Trinials.',
            }
            response = self.client.post(reverse('website:contact'), data=payload)
            self.assertRedirects(response, reverse('website:home') + '#contact')

            # Verify emails sent
            self.assertEqual(len(mail.outbox), 2)
            team_email = mail.outbox[0]
            expected_recipients = [
                'johnpaulalex85@gmail.com',
                'trinial26@gmail.com',
                'Jojogeorge.trinials@gmail.com',
                'joejoseph1235@gmail.com'
            ]
            self.assertEqual(team_email.to, expected_recipients)
            self.assertIn('+91 98765 43210', team_email.body)
            self.assertIn('Innovator Client', team_email.body)

            # Check client auto-reply
            client_email = mail.outbox[1]
            self.assertEqual(client_email.to, ['client@innovate.org'])
            self.assertNotIn('We need a full-stack digital solution', client_email.body)

    # -------------------------------------------------------------------------
    # Complete SEO, Metadata & Sitemap Test Suite
    # -------------------------------------------------------------------------

    def test_sitemap_xml_endpoint(self):
        """Verify dynamic sitemap.xml returns valid XML and indexes all canonical routes."""
        response = self.client.get(reverse('website:sitemap_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])
        content = response.content.decode('utf-8')

        # Core namespaces and structure
        self.assertIn('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', content)
        self.assertIn('<loc>https://trinial.in/</loc>', content)
        self.assertIn('<loc>https://trinial.in/about/</loc>', content)
        self.assertIn('<loc>https://trinial.in/services/</loc>', content)
        self.assertIn('<loc>https://trinial.in/insights/</loc>', content)

        # All 5 Service Landing Pages
        self.assertIn('<loc>https://trinial.in/services/web-development/</loc>', content)
        self.assertIn('<loc>https://trinial.in/services/ui-ux-design/</loc>', content)
        self.assertIn('<loc>https://trinial.in/services/ecommerce-development/</loc>', content)
        self.assertIn('<loc>https://trinial.in/services/custom-software-development/</loc>', content)
        self.assertIn('<loc>https://trinial.in/services/brand-identity-design/</loc>', content)

        # All 5 Insight Guides
        self.assertIn('<loc>https://trinial.in/insights/website-development-cost-in-kerala/</loc>', content)
        self.assertIn('<loc>https://trinial.in/insights/why-businesses-need-professional-website/</loc>', content)
        self.assertIn('<loc>https://trinial.in/insights/custom-website-vs-wordpress/</loc>', content)
        self.assertIn('<loc>https://trinial.in/insights/ecommerce-website-development-guide/</loc>', content)
        self.assertIn('<loc>https://trinial.in/insights/how-to-choose-web-development-company-kerala/</loc>', content)

        # Priority and Changefreq tags
        self.assertIn('<priority>1.0</priority>', content)
        self.assertIn('<priority>0.9</priority>', content)
        self.assertIn('<priority>0.8</priority>', content)
        self.assertIn('<changefreq>daily</changefreq>', content)

    def test_robots_txt_endpoint(self):
        """Verify robots.txt declares proper crawler directives and references sitemap."""
        response = self.client.get(reverse('website:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response['Content-Type'])
        content = response.content.decode('utf-8')

        self.assertIn('User-agent: *', content)
        self.assertIn('Allow: /', content)
        self.assertIn('Disallow: /admin/', content)
        self.assertIn('Disallow: /design-preview/', content)
        self.assertIn('Sitemap: https://trinial.in/sitemap.xml', content)

    def test_homepage_seo_metadata_and_structured_data(self):
        """Verify homepage contains comprehensive SEO meta tags, OpenGraph, Geo, and JSON-LD."""
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

        # Canonical tag
        self.assertContains(response, '<link rel="canonical" href="https://trinial.in/">')

        # Local SEO Geo directives
        self.assertContains(response, '<meta name="geo.region" content="IN-KL">')
        self.assertContains(response, '<meta name="geo.placename" content="Kerala, India">')

        # OpenGraph and Twitter Cards
        self.assertContains(response, '<meta property="og:site_name" content="Trinials">')
        self.assertContains(response, '<meta property="og:type" content="website">')
        self.assertContains(response, '<meta name="twitter:card" content="summary_large_image">')

        # JSON-LD Schema.org
        self.assertContains(response, '"@type": ["Organization", "ProfessionalService"]')
        self.assertContains(response, '"@type": "WebSite"')
        self.assertContains(response, '"name": "Trinials"')
        self.assertContains(response, '"addressRegion": "Kerala"')
        self.assertContains(response, '"areaServed"')

        # Keyword & Service Links on Homepage
        self.assertContains(response, 'Web Development Company in Kerala')
        self.assertContains(response, reverse('website:service_web_development'))
        self.assertContains(response, reverse('website:service_ui_ux_design'))
        self.assertContains(response, reverse('website:service_ecommerce_development'))
        self.assertContains(response, reverse('website:service_custom_software_development'))
        self.assertContains(response, reverse('website:service_brand_identity_design'))

    def test_all_five_service_pages_render_with_seo_and_schema(self):
        """Verify each of the 5 individual service landing pages renders with proper H1 and Schema."""
        service_slugs = [
            'web-development',
            'ui-ux-design',
            'ecommerce-development',
            'custom-software-development',
            'brand-identity-design',
        ]

        for slug in service_slugs:
            url = reverse('website:service_detail', kwargs={'slug': slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Service page {slug} failed with status {response.status_code}")
            
            # Breadcrumbs & Service schema
            self.assertContains(response, '"@type": "Service"')
            self.assertContains(response, '"@type": "BreadcrumbList"')
            self.assertContains(response, '"@type": "FAQPage"')
            self.assertContains(response, '<h1 id="service-h1"')
            self.assertContains(response, 'Frequently Asked Questions')
            self.assertContains(response, 'trinial26@gmail.com')

    def test_services_index_hub_renders(self):
        """Verify the services hub page lists all 5 services with internal links."""
        response = self.client.get(reverse('website:services_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Digital Studio Services in Kerala')
        self.assertContains(response, reverse('website:service_web_development'))
        self.assertContains(response, reverse('website:service_ui_ux_design'))
        self.assertContains(response, reverse('website:service_ecommerce_development'))
        self.assertContains(response, reverse('website:service_custom_software_development'))
        self.assertContains(response, reverse('website:service_brand_identity_design'))

    def test_all_five_insight_guides_render_with_article_schema(self):
        """Verify each of the 5 customer guides renders with Article schema and rich content."""
        insight_slugs = [
            'website-development-cost-in-kerala',
            'why-businesses-need-professional-website',
            'custom-website-vs-wordpress',
            'ecommerce-website-development-guide',
            'how-to-choose-web-development-company-kerala',
        ]

        for slug in insight_slugs:
            url = reverse('website:insight_detail', kwargs={'slug': slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Insight page {slug} failed with status {response.status_code}")

            # Article & FAQ Schema
            self.assertContains(response, '"@type": "Article"')
            self.assertContains(response, '"@type": "FAQPage"')
            self.assertContains(response, '"@type": "BreadcrumbList"')
            self.assertContains(response, '<h1 id="article-h1"')
            self.assertContains(response, 'Frequently Asked Questions')

    def test_insights_index_hub_renders(self):
        """Verify the insights hub page lists all 5 guides with internal links."""
        response = self.client.get(reverse('website:insights_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Digital Insights &amp; Practical Guides')
        self.assertContains(response, reverse('website:insight_website_cost'))
        self.assertContains(response, reverse('website:insight_why_need_website'))
        self.assertContains(response, reverse('website:insight_custom_vs_wordpress'))
        self.assertContains(response, reverse('website:insight_ecommerce_guide'))
        self.assertContains(response, reverse('website:insight_choose_company'))

    def test_custom_404_contains_noindex_and_navigation(self):
        """Verify nonexistent URLs trigger custom 404 with noindex directive."""
        response = self.client.get('/this-url-definitely-does-not-exist-at-all-404/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'noindex, follow', status_code=404)
        self.assertContains(response, 'Page Not Found', status_code=404)
        self.assertContains(response, reverse('website:home'), status_code=404)
        self.assertContains(response, reverse('website:services_index'), status_code=404)

    def test_mongodb_atlas_save_and_retrieve_enquiry(self):
        """Verify that enquiries are persisted to MongoDB Atlas and can be retrieved."""
        from website.mongo import save_enquiry_to_mongo, get_mongo_db
        db = get_mongo_db()
        if db is None:
            self.skipTest("MongoDB Atlas not reachable")

        payload = {
            'name': 'Unit Test User',
            'email': 'unittest@trinials.in',
            'phone': '+91 99999 00000',
            'subject': 'Atlas Automated Test',
            'message': 'Testing MongoDB Atlas persistence layer.',
            'ip_address': '127.0.0.1',
        }
        enquiry_id = save_enquiry_to_mongo(payload)
        self.assertIsNotNone(enquiry_id)

        # Retrieve from collection
        doc = db.enquiries.find_one({'email': 'unittest@trinials.in'})
        self.assertIsNotNone(doc)
        self.assertEqual(doc['name'], 'Unit Test User')
        self.assertEqual(doc['subject'], 'Atlas Automated Test')

        # Clean up unit test doc
        db.enquiries.delete_one({'_id': doc['_id']})

    def test_mongodb_atlas_email_config_read(self):
        """Verify that email credentials and settings can be retrieved from MongoDB Atlas."""
        from website.mongo import get_email_config_from_mongo
        config = get_email_config_from_mongo()
        if config is None:
            self.skipTest("MongoDB Atlas not reachable")

        self.assertEqual(config.get('_id'), 'email_config')
        self.assertEqual(config.get('EMAIL_HOST'), 'smtp.gmail.com')
        self.assertIn('trinial26@gmail.com', config.get('CONTACT_NOTIFICATION_EMAIL', ''))

    def test_favicon_ico_endpoint(self):
        """Verify that /favicon.ico returns HTTP 200 with image/x-icon content-type."""
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/x-icon')
        self.assertIn('public', response.get('Cache-Control', ''))

    def test_favicon_meta_tags_in_base_template(self):
        """Verify that base template contains Google Search and browser compliant favicon links."""
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, '<link rel="icon" type="image/x-icon" href="/favicon.ico">')
        self.assertContains(response, '<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico">')
        self.assertContains(response, 'favicon-48x48.png')

    def test_https_email_service_fallback_when_unconfigured(self):
        """Verify that send_email_via_https cleanly returns False without crashing when no API key is provided."""
        from website.email_service import send_email_via_https
        success, provider, err = send_email_via_https(
            to_emails=['test@example.com'],
            subject='Test',
            html_content='<p>Test</p>',
            config={}
        )
        self.assertFalse(success)
        self.assertEqual(provider, 'none')
        self.assertIn('No HTTPS email provider configured', err)

    def test_admin_portal_login_redirect_when_unauthenticated(self):
        """Verify that unauthenticated access to /admin-panel/ redirects to login."""
        response = self.client.get(reverse('website:admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('website:admin_login'), response.url)

    def test_admin_portal_login_page_renders(self):
        """Verify that /admin-panel/login/ renders correctly with HTTP 200."""
        response = self.client.get(reverse('website:admin_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Operations Console')
        self.assertContains(response, 'Sign In')

    def test_admin_portal_login_invalid_credentials(self):
        """Verify that incorrect credentials show error and reject login."""
        response = self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'incorrect_password_123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertFalse(self.client.session.get('trinials_admin_logged_in', False))

    def test_admin_portal_login_valid_credentials(self):
        """Verify that valid credentials log in and redirect to dashboard."""
        response = self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'trinials2026!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('website:admin_dashboard'), response.url)
        self.assertTrue(self.client.session.get('trinials_admin_logged_in'))

    def test_admin_portal_dashboard_authenticated(self):
        """Verify that authenticated administrator can view the dashboard and enquiry list."""
        # Log in via login endpoint
        self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'trinials2026!',
        })
        response = self.client.get(reverse('website:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Operations Console')
        self.assertContains(response, 'Total Inquiries')
        self.assertContains(response, 'Export CSV')

    def test_admin_portal_export_csv(self):
        """Verify that authenticated administrator can download enquiries as CSV."""
        self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'trinials2026!',
        })
        response = self.client.get(reverse('website:admin_export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="trinials_enquiries_', response['Content-Disposition'])

    def test_admin_portal_logout(self):
        """Verify that logout clears session and redirects to login."""
        self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'trinials2026!',
        })
        response = self.client.get(reverse('website:admin_logout'))
        self.assertEqual(response.status_code, 302)
        # Dashboard should now redirect to login
        dash_res = self.client.get(reverse('website:admin_dashboard'))
        self.assertEqual(dash_res.status_code, 302)
        self.assertIn(reverse('website:admin_login'), dash_res.url)

    def test_admin_dashboard_serial_number_and_calendar_filters(self):
        """Verify that Sl. No. column, calendar date inputs, and SVG search icon are rendered in the dashboard."""
        self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'trinials2026!',
        })
        response = self.client.get(reverse('website:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sl. No.')
        self.assertContains(response, 'name="date_from"')
        self.assertContains(response, 'name="date_to"')
        self.assertContains(response, 'search-icon-svg')
        self.assertContains(response, 'Delete by Date')

    def test_admin_bulk_delete_endpoint(self):
        """Verify that admin_bulk_delete removes matching enquiries and redirects with status message."""
        from website.mongo import save_enquiry_to_mongo, get_mongo_db
        db = get_mongo_db()
        if db is None:
            self.skipTest("MongoDB Atlas not reachable")

        # Save dummy enquiry for bulk delete test
        doc_id = save_enquiry_to_mongo({
            'name': 'Bulk Delete Tester',
            'email': 'bulk_test_temp@example.com',
            'phone': '0000000000',
            'subject': 'Temp Delete',
            'message': 'Will be deleted',
        })
        self.assertIsNotNone(doc_id)

        # Log in
        self.client.post(reverse('website:admin_login'), {
            'username': 'admin',
            'password': 'trinials2026!',
        })

        # Call bulk delete with today's date
        today_str = datetime.now().strftime('%Y-%m-%d')
        res = self.client.post(reverse('website:admin_bulk_delete'), {
            'date_from': today_str,
            'date_to': today_str,
            'status': 'all',
        })
        self.assertEqual(res.status_code, 302)
        self.assertIn(reverse('website:admin_dashboard'), res.url)

