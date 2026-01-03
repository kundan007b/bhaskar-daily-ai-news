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

      if (!endpoint) {
        setStatus(statusEl, 'error', 'Newsletter signup is not configured yet.');
        toggleButtonState(submitBtn, true);
        return;
      }

      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const emailInput = form.querySelector('[data-newsletter-input]');
        if (!emailInput) {
          return;
        }

        const email = emailInput.value.trim();
        if (!email) {
          setStatus(statusEl, 'error', 'Please enter a valid email address.');
          emailInput.focus();
          return;
        }

        toggleButtonState(submitBtn, true);
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
          });

          const result = await response.json().catch(() => ({}));

          if (result.success === false) {
            const errorMsg = result.message || 'Subscription failed.';
            setStatus(statusEl, 'error', errorMsg);
            return;
          }

          const successMessage = result?.message || 'Thanks for subscribing!';
          setStatus(statusEl, 'success', successMessage);
          form.reset();
        } catch (error) {
          console.error('Newsletter signup failed:', error);
          console.error('Endpoint:', endpoint);
          let errorMsg = 'Subscription failed. Please try again later.';
          if (error.message && error.message.includes('Failed to fetch')) {
            errorMsg = 'Network error. Check your connection or try again.';
          }
          setStatus(statusEl, 'error', errorMsg);
        } finally {
          toggleButtonState(submitBtn, false);
        }
      });
    });
  });

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

  function toggleButtonState(button, disabled) {
    if (!button) {
      return;
    }

    button.disabled = !!disabled;
    button.classList.toggle('opacity-70', !!disabled);
    button.classList.toggle('cursor-not-allowed', !!disabled);
  }
})();
