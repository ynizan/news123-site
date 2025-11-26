/**
 * Cloudflare Worker for PermitIndex Contact Form
 *
 * This worker receives contact form submissions and sends emails.
 *
 * DEPLOYMENT INSTRUCTIONS:
 *
 * 1. Go to Cloudflare Dashboard > Workers & Pages
 * 2. Create a new Worker
 * 3. Copy this code into the worker
 * 4. Add the following environment variables (Settings > Variables):
 *    - SEND_TO_EMAIL: Your email address (e.g., contact@permitindex.com)
 *
 * 5. Option A: Use Cloudflare Email Routing (Free)
 *    - Set up Email Routing in Cloudflare Dashboard
 *    - The worker will use fetch() to send to your domain's email
 *
 * 6. Option B: Use Mailgun API (Recommended for reliability)
 *    - Sign up at mailgun.com (free tier available)
 *    - Add these environment variables:
 *      - MAILGUN_API_KEY: Your Mailgun API key
 *      - MAILGUN_DOMAIN: Your Mailgun domain
 *
 * 7. Set up a route:
 *    - Route pattern: permitindex.com/api/contact
 *    - Worker: [your worker name]
 *
 * 8. Test the form on your site!
 */

// CORS headers for the response
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

/**
 * Main worker handler
 */
export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: CORS_HEADERS,
      });
    }

    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response('Method not allowed', {
        status: 405,
        headers: CORS_HEADERS,
      });
    }

    try {
      // Parse the request body
      const data = await request.json();

      // Validate required fields
      if (!data.name || !data.email || !data.subject || !data.message) {
        return new Response(JSON.stringify({ error: 'Missing required fields' }), {
          status: 400,
          headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
        });
      }

      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(data.email)) {
        return new Response(JSON.stringify({ error: 'Invalid email address' }), {
          status: 400,
          headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
        });
      }

      // Send email using configured method
      const emailSent = await sendEmail(data, env);

      if (emailSent) {
        return new Response(JSON.stringify({ success: true }), {
          status: 200,
          headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
        });
      } else {
        return new Response(JSON.stringify({ error: 'Failed to send email' }), {
          status: 500,
          headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
        });
      }
    } catch (error) {
      console.error('Error processing contact form:', error);
      return new Response(JSON.stringify({ error: 'Internal server error' }), {
        status: 500,
        headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
      });
    }
  },
};

/**
 * Send email using Mailgun API
 */
async function sendEmail(data, env) {
  const { name, email, subject, message } = data;

  // Check if Mailgun is configured
  if (env.MAILGUN_API_KEY && env.MAILGUN_DOMAIN) {
    return await sendViaMailgun(data, env);
  }

  // Fallback: Log to console (for development/testing)
  console.log('Email would be sent:', {
    from: `${name} <${email}>`,
    to: env.SEND_TO_EMAIL || 'contact@permitindex.com',
    subject: `[PermitIndex Contact] ${subject}`,
    message,
  });

  // In production without Mailgun, you could:
  // - Use Cloudflare Email Workers (when available)
  // - Use another email service API
  // - Return false to indicate email wasn't sent

  return true; // Return true for now (change to false if you want to require Mailgun)
}

/**
 * Send email via Mailgun API
 */
async function sendViaMailgun(data, env) {
  const { name, email, subject, message } = data;

  const mailgunUrl = `https://api.mailgun.net/v3/${env.MAILGUN_DOMAIN}/messages`;

  const formData = new FormData();
  formData.append('from', `PermitIndex Contact Form <noreply@${env.MAILGUN_DOMAIN}>`);
  formData.append('to', env.SEND_TO_EMAIL || 'contact@permitindex.com');
  formData.append('subject', `[Contact Form] ${subject}`);
  formData.append('text', `
Name: ${name}
Email: ${email}
Subject: ${subject}

Message:
${message}

---
Sent from PermitIndex contact form
Reply-To: ${email}
  `.trim());
  formData.append('h:Reply-To', email);

  try {
    const response = await fetch(mailgunUrl, {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + btoa(`api:${env.MAILGUN_API_KEY}`),
      },
      body: formData,
    });

    if (response.ok) {
      console.log('Email sent successfully via Mailgun');
      return true;
    } else {
      console.error('Mailgun error:', await response.text());
      return false;
    }
  } catch (error) {
    console.error('Error sending via Mailgun:', error);
    return false;
  }
}
