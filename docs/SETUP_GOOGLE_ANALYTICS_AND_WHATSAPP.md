# Google Analytics (GA4) & WhatsApp Setup

Quick, actionable instructions to finish analytics tracking and add a tracked WhatsApp link.

---

## 🔍 Google Analytics (GA4) — Quick Setup

1. Create a GA4 property
   - Go to https://analytics.google.com → Admin → Create Property → follow steps.
   - Create a **Web Data Stream** and copy the **Measurement ID** (format: `G-XXXXXXXXXX`).

2. Add the tracking snippet to your site
   - Replace the `G-XXXXXXXXXX` placeholder already in `index.html` with your Measurement ID.

```html
<!-- head (already present) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

3. Track popup form submissions (recommended)
   - Add this code where the popup form reports success (inside the `if(res.ok){ ... }` branch):

```js
if (window.gtag) {
  gtag('event', 'contact_popup_submit', {
    'event_category': 'Contact',
    'event_label': 'Popup',
    'value': 1,
    'subject': 'Site Popup: Contacto Rápido'
  });
}
```

4. Verify in GA
   - Open **Realtime** or **DebugView** in GA (DebugView works if you enable the GA Debugger extension or send `debug_mode: true` in the event).
   - Submit a test popup message and confirm the `contact_popup_submit` event appears.

5. Create a Conversion
   - In GA → Configure → Events, find `contact_popup_submit` and mark it as a conversion.

6. Tips
   - Consider using Google Tag Manager for more flexibility in the future.
   - Use UTM parameters for campaign tracking when you run ads or share links.

---

## 💬 WhatsApp Link — Setup and Tracking

1. Create the WhatsApp link
   - Format: `https://wa.me/351XXXXXXXXX?text=Olá%20gostaria%20de%20saber%20sobre%20os%20cursos` (URL-encode the message)
   - Add UTM parameters to track campaign source:

```
https://wa.me/351XXXXXXXXX?text=Olá...&utm_source=site&utm_medium=whatsapp&utm_campaign=contact
```

2. Add the link to your footer (example):

```html
<a id="wa-link" href="https://wa.me/351XXXXXXXXX?text=Ol%C3%A1%20gostaria%20de%20saber%20sobre%20os%20cursos&utm_source=site&utm_medium=whatsapp&utm_campaign=contact" target="_blank" rel="noopener" aria-label="WhatsApp">💬 WhatsApp: +351 XXX XXX XXX</a>
```

3. Track WhatsApp clicks with GA event
   - Add this small JS snippet (place in your main site JS or just before `</body>`):

```js
const wa = document.getElementById('wa-link');
if (wa && window.gtag) {
  wa.addEventListener('click', () => {
    gtag('event', 'click_whatsapp', {
      'event_category': 'Contact',
      'event_label': 'Footer WhatsApp'
    });
  });
}
```

4. Privacy / GDPR
   - Add WhatsApp use to your privacy policy (WhatsApp are third-party processors).
   - Avoid asking users to share sensitive personal data over WhatsApp.

---

## ✅ Test & Validate

- For **GA events**: use GA DebugView and Realtime to confirm events appear.
- For **Formspree** submissions: verify the `_subject` field shows in submission details.
- For **WhatsApp**: click the footer link, verify navigation (opens WhatsApp) and that GA records `click_whatsapp`.

---

## Optional next steps

- Migrate to **Google Tag Manager** (one container to manage GA + future tags).
- Add a small success/thank-you page (redirect after form submission) and mark that page view as a conversion (simpler than custom events).
- Add `event_label` values that include UTM or source so you can segment easily.

---

If you want, I can:
- Replace the `G-XXXXXXXXXX` placeholder with your real Measurement ID and test events, or
- Add the WhatsApp link (you said you'll provide the number later).

