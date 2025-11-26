/**
 * Cloudflare Worker: Feedback Proxy
 *
 * This worker receives feedback submissions from the frontend
 * and creates GitHub Issues on behalf of users using a secret token.
 *
 * Setup:
 * 1. Create GitHub Personal Access Token with 'repo' scope
 * 2. Add as Worker secret: GITHUB_TOKEN
 * 3. Deploy to Cloudflare Workers
 * 4. Update form to POST to this Worker URL
 */

export default {
  async fetch(request, env) {
    // CORS headers for frontend requests
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Only accept POST requests
    if (request.method !== 'POST') {
      return new Response('Method not allowed', {
        status: 405,
        headers: corsHeaders
      });
    }

    try {
      // Parse request body
      const { permit_slug, feedback_type, feedback_text } = await request.json();

      // Validate input
      if (!permit_slug || !feedback_type || !feedback_text) {
        return new Response(JSON.stringify({
          error: 'Missing required fields'
        }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Validate feedback_type
      const validTypes = ['tip', 'common_mistake', 'time_estimate', 'cost_note'];
      if (!validTypes.includes(feedback_type)) {
        return new Response(JSON.stringify({
          error: 'Invalid feedback type'
        }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Validate feedback length
      if (feedback_text.length > 500) {
        return new Response(JSON.stringify({
          error: 'Feedback text exceeds 500 characters'
        }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Create GitHub Issue
      const githubResponse = await fetch(
        'https://api.github.com/repos/ynizan/news123-site/issues',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'User-Agent': 'News123-Feedback-Worker'
          },
          body: JSON.stringify({
            title: `User Feedback: ${permit_slug}`,
            body: `**Permit:** ${permit_slug}\n**Type:** ${feedback_type}\n**Feedback:**\n${feedback_text}`,
            labels: ['user-tip', feedback_type]
          })
        }
      );

      if (!githubResponse.ok) {
        const errorData = await githubResponse.text();
        console.error('GitHub API Error:', errorData);

        return new Response(JSON.stringify({
          error: 'Failed to create issue',
          details: errorData
        }), {
          status: githubResponse.status,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      const issueData = await githubResponse.json();

      // Return success
      return new Response(JSON.stringify({
        success: true,
        issue_number: issueData.number,
        issue_url: issueData.html_url
      }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (error) {
      console.error('Worker Error:', error);

      return new Response(JSON.stringify({
        error: 'Internal server error',
        message: error.message
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
