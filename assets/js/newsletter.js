'use strict';

(function () {
  const endpoint = (window.NEWSLETTER_ENDPOINT || '').trim();

  document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('[data-newsletter-form]');
    if (!forms.length) {
      return;
    }

    forms.forEach((form) => {
      const statusEl = ensureStatusElement(form);
      const submitBtn = form.querySelector('[type="submit"]');
      const emailInput = form.querySelector('[data-newsletter-input]');

      // Check if endpoint is configured
      if (!endpoint) {
        setStatus(statusEl, 'error', 'Newsletter signup is not configured yet.');
        toggleButtonState(submitBtn, true);
        return;
      }

      // Real-time email validation feedback
      if (emailInput) {
        emailInput.addEventListener('input', () => {
          if (emailInput.value && !isValidEmail(emailInput.value)) {
            emailInput.classList.add('border-rose-400/50');
            emailInput.classList.remove('border-white/10');
          } else {
            emailInput.classList.remove('border-rose-400/50');
            emailInput.classList.add('border-white/10');
          }
        });
      }

      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        if (!emailInput) {
          return;
        }

        const email = emailInput.value.trim();
        if (!email || !isValidEmail(email)) {
          setStatus(statusEl, 'error', 'Please enter a valid email address.');
          emailInput.focus();
          shakeElement(emailInput);
          return;
        }

        toggleButtonState(submitBtn, true, true);
        setStatus(statusEl, 'info', 'Subscribing…');

        try {
          const payload = {
            email,
            page: window.location.pathname,
            userAgent: navigator.userAgent,
          };

          const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Accept: 'application/json',
            },
            body: JSON.stringify(payload),
            mode: 'cors',
          });

          let result;
          const contentType = response.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            result = await response.json();
          } else {
            // Handle redirect responses from Apps Script
            const text = await response.text();
            try {
              result = JSON.parse(text);
            } catch {
              result = { success: true, message: 'Thanks for subscribing!' };
            }
          }

          if (result.success === false) {
            const errorMsg = result.message || 'Subscription failed.';
            setStatus(statusEl, 'error', errorMsg);
            return;
          }

          const successMessage = result?.message || 'Thanks for subscribing! 🎉';
          setStatus(statusEl, 'success', successMessage);
          form.reset();
          
          // Celebrate animation
          if (submitBtn) {
            submitBtn.textContent = '✓ Subscribed';
            setTimeout(() => {
              submitBtn.textContent = 'Subscribe';
            }, 3000);
          }
        } catch (error) {
          console.error('Newsletter signup failed:', error);
          let errorMsg = 'Subscription failed. Please try again later.';
          if (error.message && error.message.includes('Failed to fetch')) {
            errorMsg = 'Network error. Check your connection and try again.';
          }
          setStatus(statusEl, 'error', errorMsg);
        } finally {
          toggleButtonState(submitBtn, false, false);
        }
      });
    });
  });

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function shakeElement(element) {
    element.classList.add('animate-shake');
    element.style.animation = 'shake 0.5s ease-in-out';
    setTimeout(() => {
      element.style.animation = '';
    }, 500);
  }

  function ensureStatusElement(form) {
    let element = form.querySelector('[data-newsletter-status]');
    if (!element) {
      element = document.createElement('p');
      element.dataset.newsletterStatus = 'true';
      element.className = 'text-xs mt-2';
      form.appendChild(element);
    }
    return element;
  }

  function setStatus(element, state, message) {
    if (!element) {
      return;
    }

    const classMap = {
      success: 'text-emerald-400',
      error: 'text-rose-400',
      info: 'text-slate-300',
    };

    Object.values(classMap).forEach((cls) => element.classList.remove(cls));
    const cssClass = classMap[state] || classMap.info;
    element.classList.add(cssClass);
    element.textContent = message;
    element.style.display = 'block';
    element.classList.remove('hidden');
  }

  function toggleButtonState(button, disabled, loading = false) {
    if (!button) {
      return;
    }

    button.disabled = !!disabled;
    button.classList.toggle('loading', !!loading);
    
    if (disabled && !loading) {
      button.classList.add('opacity-70', 'cursor-not-allowed');
    } else {
      button.classList.remove('opacity-70', 'cursor-not-allowed');
    }
  }
})();
