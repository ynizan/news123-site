"""
Test helper utilities
"""

def normalize_whitespace(text):
    """Normalize whitespace in text for comparison"""
    return ' '.join(text.split())

def get_permit_slug(jurisdiction, permit_type):
    """Generate permit slug from jurisdiction and permit type"""
    return f"{jurisdiction}/{permit_type}/".lower().replace(' ', '-')

def is_valid_url(url):
    """Check if URL is valid format"""
    return url and (url.startswith('http://') or url.startswith('https://'))
