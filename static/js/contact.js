/**
 * Trinials Portfolio Website - Optimized Contact Form Controller
 * File: static/js/contact.js
 * Purpose: Handles asynchronous (AJAX) inquiry submissions, instant visual feedback,
 *          client-side input validation, loading indicators, and dedicated success states.
 */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var form = document.getElementById('contact-form');
        var successCard = document.getElementById('contact-success-card');
        var resetBtn = document.getElementById('contact-btn-reset');
        var messageInput = document.getElementById('contact-message');
        var charCounter = document.getElementById('message-char-count');

        if (!form) return;

        var submitBtn = form.querySelector('.contact-btn-submit');
        var btnSpinner = submitBtn ? submitBtn.querySelector('.btn-spinner') : null;
        var btnLabel = submitBtn ? submitBtn.querySelector('.btn-submit-label') : null;
        var originalBtnHtml = btnLabel ? btnLabel.innerHTML : 'Send Message &nearr;';

        // 1. Live Character Counter for Message Textarea
        if (messageInput && charCounter) {
            function updateCharCount() {
                var len = messageInput.value.length;
                charCounter.textContent = len;
                if (len >= 2900) {
                    charCounter.style.color = '#DC2626';
                    charCounter.style.fontWeight = 'bold';
                } else {
                    charCounter.style.color = '';
                    charCounter.style.fontWeight = '';
                }
            }
            messageInput.addEventListener('input', updateCharCount);
            updateCharCount();
        }

        // 2. Real-Time Clear Error on Input
        var inputs = form.querySelectorAll('.form-input, .form-textarea');
        inputs.forEach(function (input) {
            input.addEventListener('input', function () {
                if (this.classList.contains('input-error')) {
                    this.classList.remove('input-error');
                    var group = this.closest('.form-group');
                    if (group) {
                        group.classList.remove('has-error');
                        var errSpan = group.querySelector('.field-error');
                        if (errSpan) errSpan.remove();
                    }
                }
            });
        });

        // 3. Clear all form error states
        function clearAllErrors() {
            var errorSpans = form.querySelectorAll('.field-error');
            errorSpans.forEach(function (el) { el.remove(); });

            var errorGroups = form.querySelectorAll('.form-group.has-error');
            errorGroups.forEach(function (el) { el.classList.remove('has-error'); });

            var errorInputs = form.querySelectorAll('.input-error');
            errorInputs.forEach(function (el) { el.classList.remove('input-error'); });

            var feedbackAlerts = form.querySelector('.contact-feedback');
            if (feedbackAlerts) feedbackAlerts.innerHTML = '';
        }

        // 4. Render a field error
        function setFieldError(fieldName, errorMessage) {
            var field = form.querySelector('[name="' + fieldName + '"]');
            if (!field) return;

            field.classList.add('input-error');
            var group = field.closest('.form-group');
            if (group) {
                group.classList.add('has-error');
                var existingErr = group.querySelector('.field-error');
                if (existingErr) existingErr.remove();

                var span = document.createElement('span');
                span.className = 'field-error';
                span.setAttribute('role', 'alert');
                span.textContent = errorMessage;
                group.appendChild(span);
            }
        }

        // 5. Asynchronous Form Submission
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            clearAllErrors();

            // Client-side quick validation
            var hasClientError = false;
            var nameVal = (form.querySelector('[name="name"]').value || '').trim();
            var emailVal = (form.querySelector('[name="email"]').value || '').trim();
            var phoneVal = (form.querySelector('[name="phone"]').value || '').trim();
            var subjectVal = (form.querySelector('[name="subject"]').value || '').trim();
            var messageVal = (form.querySelector('[name="message"]').value || '').trim();

            if (!nameVal) {
                setFieldError('name', 'Please enter your full name.');
                hasClientError = true;
            }

            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailVal) {
                setFieldError('email', 'Please enter your email address.');
                hasClientError = true;
            } else if (!emailRegex.test(emailVal)) {
                setFieldError('email', 'Please enter a valid email address.');
                hasClientError = true;
            }

            if (!phoneVal) {
                setFieldError('phone', 'Please enter your contact phone number.');
                hasClientError = true;
            } else if (phoneVal.replace(/\D/g, '').length < 6) {
                setFieldError('phone', 'Please enter a valid phone number with area code.');
                hasClientError = true;
            }

            if (!subjectVal) {
                setFieldError('subject', 'Please enter a subject.');
                hasClientError = true;
            }

            if (!messageVal) {
                setFieldError('message', 'Please enter your project message.');
                hasClientError = true;
            }

            if (hasClientError) {
                var firstErr = form.querySelector('.input-error');
                if (firstErr) firstErr.focus();
                return;
            }

            // Set loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('is-submitting');
                if (btnSpinner) btnSpinner.style.display = 'inline-block';
                if (btnLabel) btnLabel.textContent = 'Sending your message...';
            }

            inputs.forEach(function (inp) { inp.setAttribute('readonly', 'readonly'); });

            var formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { status: response.status, ok: response.ok, data: data };
                });
            })
            .then(function (res) {
                if (res.ok && res.data.success) {
                    // Success Transition
                    form.reset();
                    if (charCounter) charCounter.textContent = '0';

                    // Update personalized details on the success card if available
                    if (res.data.inquiry && res.data.inquiry.name) {
                        var clientNameTarget = document.getElementById('success-client-name');
                        if (clientNameTarget) {
                            clientNameTarget.textContent = res.data.inquiry.name;
                        }
                    }

                    if (successCard) {
                        form.style.display = 'none';
                        successCard.style.display = 'flex';
                        successCard.classList.add('is-active');

                        // Smoothly scroll to the contact container
                        var contactSection = document.getElementById('contact');
                        if (contactSection) {
                            contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }
                } else {
                    // Server returned validation errors
                    restoreFormControls();
                    var errors = res.data.errors || {};
                    var hasFocused = false;
                    for (var fieldKey in errors) {
                        if (errors.hasOwnProperty(fieldKey)) {
                            var errMsg = Array.isArray(errors[fieldKey]) ? errors[fieldKey][0] : errors[fieldKey];
                            setFieldError(fieldKey, errMsg);
                            if (!hasFocused) {
                                var errInput = form.querySelector('[name="' + fieldKey + '"]');
                                if (errInput) {
                                    errInput.focus();
                                    hasFocused = true;
                                }
                            }
                        }
                    }

                    if (!hasFocused) {
                        var feedbackAlerts = form.querySelector('.contact-feedback');
                        if (feedbackAlerts) {
                            feedbackAlerts.innerHTML = '<div class="alert alert-error"><span class="alert-icon">&#9888;</span><span class="alert-text">' +
                                (res.data.message || 'Please check your input and try again.') + '</span></div>';
                        }
                    }
                }
            })
            .catch(function (error) {
                restoreFormControls();
                var feedbackAlerts = form.querySelector('.contact-feedback');
                if (feedbackAlerts) {
                    feedbackAlerts.innerHTML = '<div class="alert alert-error"><span class="alert-icon">&#9888;</span><span class="alert-text">' +
                        'Unable to deliver message right now. Please call us at +91 85908 21155 or email trinial26@gmail.com directly.</span></div>';
                }
            });

            function restoreFormControls() {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('is-submitting');
                    if (btnSpinner) btnSpinner.style.display = 'none';
                    if (btnLabel) btnLabel.innerHTML = originalBtnHtml;
                }
                inputs.forEach(function (inp) { inp.removeAttribute('readonly'); });
            }
        });

        // 6. Reset Form to send another inquiry
        if (resetBtn && successCard) {
            resetBtn.addEventListener('click', function () {
                successCard.style.display = 'none';
                successCard.classList.remove('is-active');
                form.style.display = 'flex';
                clearAllErrors();
                form.reset();

                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('is-submitting');
                    if (btnSpinner) btnSpinner.style.display = 'none';
                    if (btnLabel) btnLabel.innerHTML = originalBtnHtml;
                }

                inputs.forEach(function (inp) { inp.removeAttribute('readonly'); });

                var firstInput = form.querySelector('#contact-name');
                if (firstInput) firstInput.focus();
            });
        }
    });
})();

