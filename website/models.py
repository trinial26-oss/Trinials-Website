from django.db import models


class ContactMessage(models.Model):
    """
    Model representing an enquiry submitted through the homepage contact form.
    Stores sender details, message body, submission timestamp, and review status.
    """
    name = models.CharField(
        max_length=100,
        help_text="Full name of the sender."
    )
    email = models.EmailField(
        max_length=254,
        help_text="Contact email address of the sender."
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        default='',
        help_text="Contact phone number of the sender."
    )
    subject = models.CharField(
        max_length=150,
        help_text="Brief subject or inquiry topic."
    )
    message = models.TextField(
        max_length=3000,
        help_text="Detailed message or inquiry."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the inquiry was received."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Flag indicating whether an administrator has reviewed this message."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.created_at:%Y-%m-%d %H:%M})"
