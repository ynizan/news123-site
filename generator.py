#!/usr/bin/env python3
"""
News123 Static Site Generator v1.0
Generates static HTML pages for a news aggregation website.

This script generates static HTML pages for news articles.
It reads data from JSON files in /data/articles and generates pages.

Directory Structure:
- /templates: Jinja2 templates
- /data/articles: News article JSON data files
- /output: Generated HTML pages
- /static: Static assets (CSS, JS, images)

Usage:
    python generator.py
"""

import os
import json
import glob
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import re


# Required fields for article records
REQUIRED_FIELDS = [
    'id',              # Unique identifier
    'title',           # Article headline
    'slug',            # URL-friendly slug
    'category',        # Category name
    'category_slug',   # Category URL slug
    'excerpt',         # Short description
    'content',         # Full article content (HTML)
    'author',          # Author name
    'published_date',  # Publication date (YYYY-MM-DD)
    'source',          # News source name
]

# Optional fields
OPTIONAL_FIELDS = [
    'source_url',           # Original source URL
    'image_url',            # Featured image URL
    'image_caption',        # Image caption
    'tags',                 # List of tags
    'reading_time',         # Estimated reading time in minutes
    'updated_date',         # Last updated date
    'is_breaking',          # Breaking news flag
    'is_featured',          # Featured article flag
    'related_articles',     # List of related article IDs
]


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def format_date(date_str):
    """Format date string for display."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str


def load_articles(data_dir='data/articles'):
    """Load all article data from JSON files."""
    articles = []

    if not os.path.exists(data_dir):
        print(f"Creating data directory: {data_dir}")
        os.makedirs(data_dir)
        return articles

    json_files = glob.glob(os.path.join(data_dir, '*.json'))

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    articles.extend(data)
                else:
                    articles.append(data)
            print(f"Loaded {json_file}")
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    # Add formatted date to each article
    for article in articles:
        article['published_date_formatted'] = format_date(article.get('published_date', ''))

    return articles


def get_categories(articles):
    """Extract unique categories from articles."""
    categories = {}

    for article in articles:
        cat_name = article.get('category', 'Uncategorized')
        cat_slug = article.get('category_slug', slugify(cat_name))

        if cat_slug not in categories:
            categories[cat_slug] = {
                'name': cat_name,
                'slug': cat_slug,
                'article_count': 0,
                'articles': []
            }

        categories[cat_slug]['article_count'] += 1
        categories[cat_slug]['articles'].append(article)

    return list(categories.values())


def get_featured_topics(articles):
    """Get featured topics based on article tags and categories."""
    topics = [
        {
            'name': 'Technology',
            'slug': 'technology',
            'description': 'The latest in tech innovation, AI, startups, and digital transformation.',
            'article_count': len([a for a in articles if a.get('category_slug') == 'technology'])
        },
        {
            'name': 'Business',
            'slug': 'business',
            'description': 'Market analysis, corporate news, and economic insights.',
            'article_count': len([a for a in articles if a.get('category_slug') == 'business'])
        },
        {
            'name': 'Politics',
            'slug': 'politics',
            'description': 'Political news, policy updates, and government affairs.',
            'article_count': len([a for a in articles if a.get('category_slug') == 'politics'])
        },
    ]
    return [t for t in topics if t['article_count'] > 0] or topics[:3]


def calculate_stats(articles, categories):
    """Calculate site statistics."""
    sources = set()
    for article in articles:
        if article.get('source'):
            sources.add(article['source'])

    return {
        'total_articles': len(articles),
        'total_sources': len(sources),
        'total_categories': len(categories),
    }


def generate_site(articles, output_dir='output'):
    """Generate all static pages."""
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Get categories and stats
    categories = get_categories(articles)
    stats = calculate_stats(articles, categories)
    featured_topics = get_featured_topics(articles)

    # Sort articles by date (newest first)
    articles_sorted = sorted(
        articles,
        key=lambda x: x.get('published_date', ''),
        reverse=True
    )
    latest_articles = articles_sorted[:9]  # Get 9 latest for homepage

    # Generate homepage
    print("Generating homepage...")
    template = env.get_template('index.html')
    html = template.render(
        stats=stats,
        categories=categories,
        latest_articles=latest_articles,
        featured_topics=featured_topics
    )
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    # Generate article pages
    print("Generating article pages...")
    article_template = env.get_template('article_page.html')

    for article in articles:
        # Create category directory
        cat_dir = os.path.join(output_dir, article.get('category_slug', 'uncategorized'))
        os.makedirs(cat_dir, exist_ok=True)

        # Create article directory
        article_dir = os.path.join(cat_dir, article.get('slug', article['id']))
        os.makedirs(article_dir, exist_ok=True)

        # Find related articles (same category, different article)
        related = [
            a for a in articles
            if a.get('category_slug') == article.get('category_slug')
            and a['id'] != article['id']
        ][:4]

        # Render article page
        html = article_template.render(
            article=article,
            related_articles=related
        )

        with open(os.path.join(article_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    # Generate category pages
    print("Generating category pages...")
    generate_category_pages(env, categories, output_dir)

    # Generate sitemap
    print("Generating sitemap...")
    generate_sitemap(articles, categories, output_dir)

    # Generate robots.txt
    print("Generating robots.txt...")
    generate_robots(output_dir)

    # Copy static files
    print("Copying static files...")
    copy_static_files(output_dir)

    print(f"\nSite generation complete!")
    print(f"  - {len(articles)} articles")
    print(f"  - {len(categories)} categories")
    print(f"  - Output directory: {output_dir}/")


def generate_category_pages(env, categories, output_dir):
    """Generate category listing pages."""
    # Create a simple category template inline if it doesn't exist
    category_template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ category.name }} News - News123</title>
    <meta name="description" content="Latest {{ category.name }} news and articles from News123.">
    <link rel="canonical" href="https://news123.com/category/{{ category.slug }}/">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --primary: #1a1a2e;
            --accent: #e94560;
            --text: #1a1a1a;
            --text-light: #666666;
            --bg: #ffffff;
            --bg-light: #f8f9fa;
            --border: #e0e0e0;
            --radius-large: 12px;
            --radius-medium: 8px;
            --shadow-medium: 0 4px 16px rgba(0,0,0,0.1);
        }
        body { background: var(--bg-light); color: var(--text); }
        h1, h2 { font-family: 'Arial Black', sans-serif; color: var(--primary); }
        .news-card {
            background: white;
            padding: 24px;
            border-radius: var(--radius-large);
            border: 1px solid var(--border);
            transition: all 0.2s;
        }
        .news-card:hover {
            box-shadow: var(--shadow-medium);
            transform: translateY(-2px);
        }
        .category-badge {
            display: inline-block;
            padding: 4px 12px;
            background: var(--accent);
            color: white;
            font-size: 12px;
            font-weight: 600;
            border-radius: 4px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    {% include 'components/header.html' %}

    <main class="container mx-auto px-4 py-12">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-4xl font-bold mb-2">{{ category.name }}</h1>
            <p class="text-lg mb-8" style="color: var(--text-light);">{{ category.article_count }} articles</p>

            <div class="grid gap-6">
                {% for article in category.articles %}
                <a href="/{{ article.category_slug }}/{{ article.slug }}/" class="news-card block" style="text-decoration: none;">
                    <span class="category-badge">{{ article.category }}</span>
                    <h2 class="text-xl font-bold mt-3 mb-2" style="color: var(--primary);">{{ article.title }}</h2>
                    <p class="text-sm mb-2" style="color: var(--text-light);">{{ article.source }} &bull; {{ article.published_date_formatted }}</p>
                    <p style="color: var(--text-light);">{{ article.excerpt }}</p>
                </a>
                {% endfor %}
            </div>
        </div>
    </main>

    {% include 'components/footer.html' %}
</body>
</html>'''

    # Write category template
    with open('templates/category_page.html', 'w', encoding='utf-8') as f:
        f.write(category_template_content)

    # Reload environment to pick up new template
    env = Environment(loader=FileSystemLoader('templates'))
    category_template = env.get_template('category_page.html')

    # Create categories index directory
    categories_dir = os.path.join(output_dir, 'category')
    os.makedirs(categories_dir, exist_ok=True)

    for category in categories:
        # Sort articles by date
        category['articles'] = sorted(
            category['articles'],
            key=lambda x: x.get('published_date', ''),
            reverse=True
        )

        # Create category directory
        cat_dir = os.path.join(categories_dir, category['slug'])
        os.makedirs(cat_dir, exist_ok=True)

        # Render category page
        html = category_template.render(category=category)

        with open(os.path.join(cat_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)


def generate_sitemap(articles, categories, output_dir):
    """Generate sitemap.xml."""
    sitemap_entries = []
    base_url = 'https://news123.com'
    today = datetime.now().strftime('%Y-%m-%d')

    # Homepage
    sitemap_entries.append(f'''  <url>
    <loc>{base_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>''')

    # Category pages
    for category in categories:
        sitemap_entries.append(f'''  <url>
    <loc>{base_url}/category/{category['slug']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>''')

    # Article pages
    for article in articles:
        lastmod = article.get('updated_date') or article.get('published_date', today)
        sitemap_entries.append(f'''  <url>
    <loc>{base_url}/{article.get('category_slug', 'news')}/{article.get('slug', article['id'])}/</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>
  </url>''')

    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>'''

    with open(os.path.join(output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)


def generate_robots(output_dir):
    """Generate robots.txt."""
    robots_content = '''User-agent: *
Allow: /

Sitemap: https://news123.com/sitemap.xml
'''

    with open(os.path.join(output_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots_content)


def copy_static_files(output_dir):
    """Copy static files to output directory."""
    import shutil

    static_src = 'static'
    static_dest = output_dir

    if os.path.exists(static_src):
        for item in os.listdir(static_src):
            src_path = os.path.join(static_src, item)
            dest_path = os.path.join(static_dest, item)

            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)


def main():
    """Main entry point."""
    print("News123 Static Site Generator")
    print("=" * 40)

    # Load articles
    articles = load_articles()

    if not articles:
        print("\nNo articles found. Creating sample data...")
        create_sample_data()
        articles = load_articles()

    print(f"\nLoaded {len(articles)} articles")

    # Generate site
    generate_site(articles)


def create_sample_data():
    """Create sample news article data."""
    sample_articles = [
        {
            "id": "tech-001",
            "title": "AI Revolution: How Machine Learning is Transforming Industries",
            "slug": "ai-revolution-machine-learning-transforming-industries",
            "category": "Technology",
            "category_slug": "technology",
            "excerpt": "From healthcare to finance, artificial intelligence is reshaping how businesses operate and make decisions.",
            "content": "<p>Artificial intelligence and machine learning technologies are experiencing unprecedented growth and adoption across virtually every industry sector.</p><p>Healthcare organizations are using AI to diagnose diseases earlier and more accurately. Financial institutions leverage machine learning for fraud detection and risk assessment. Manufacturing companies employ predictive maintenance to reduce downtime.</p><p>The implications of this technological shift are profound, affecting employment patterns, business models, and even the way we interact with technology in our daily lives.</p>",
            "author": "Sarah Chen",
            "published_date": "2024-11-25",
            "source": "Tech Daily",
            "reading_time": 5,
            "tags": [{"name": "AI", "slug": "ai"}, {"name": "Machine Learning", "slug": "machine-learning"}]
        },
        {
            "id": "business-001",
            "title": "Global Markets Rally as Economic Indicators Show Growth",
            "slug": "global-markets-rally-economic-indicators-growth",
            "category": "Business",
            "category_slug": "business",
            "excerpt": "Stock markets around the world posted significant gains following positive economic data releases.",
            "content": "<p>Global stock markets experienced a significant rally this week as economic indicators across major economies showed stronger-than-expected growth.</p><p>The S&P 500 rose 2.3%, while European markets gained an average of 1.8%. Asian markets also closed higher, with the Nikkei advancing 1.5%.</p><p>Analysts attribute the positive sentiment to encouraging employment figures, robust consumer spending data, and easing inflation concerns.</p>",
            "author": "Michael Torres",
            "published_date": "2024-11-24",
            "source": "Financial Times",
            "reading_time": 4,
            "tags": [{"name": "Markets", "slug": "markets"}, {"name": "Economy", "slug": "economy"}]
        },
        {
            "id": "politics-001",
            "title": "New Climate Agreement Reached at International Summit",
            "slug": "new-climate-agreement-international-summit",
            "category": "Politics",
            "category_slug": "politics",
            "excerpt": "World leaders have agreed to ambitious new targets for reducing carbon emissions by 2030.",
            "content": "<p>In a historic development, representatives from over 150 countries have agreed to new, more ambitious climate targets at the international climate summit.</p><p>The agreement commits signatory nations to reducing carbon emissions by 50% from 2020 levels by 2030, with a pathway to net-zero emissions by 2050.</p><p>Environmental groups have cautiously welcomed the agreement while noting that implementation will be crucial to its success.</p>",
            "author": "Emma Williams",
            "published_date": "2024-11-23",
            "source": "World News",
            "reading_time": 6,
            "tags": [{"name": "Climate", "slug": "climate"}, {"name": "Policy", "slug": "policy"}]
        },
        {
            "id": "tech-002",
            "title": "Breakthrough in Quantum Computing Achieved by Research Team",
            "slug": "breakthrough-quantum-computing-research-team",
            "category": "Technology",
            "category_slug": "technology",
            "excerpt": "Scientists demonstrate quantum advantage in solving complex optimization problems.",
            "content": "<p>A team of researchers has achieved a significant breakthrough in quantum computing, demonstrating clear advantages over classical computers in solving specific optimization problems.</p><p>The achievement marks an important milestone in the development of practical quantum computing applications.</p><p>Industry experts believe this development could accelerate the timeline for commercially viable quantum computers.</p>",
            "author": "David Park",
            "published_date": "2024-11-22",
            "source": "Science Weekly",
            "reading_time": 7,
            "tags": [{"name": "Quantum", "slug": "quantum"}, {"name": "Research", "slug": "research"}]
        },
        {
            "id": "sports-001",
            "title": "Championship Finals Set After Dramatic Semifinal Victories",
            "slug": "championship-finals-dramatic-semifinal-victories",
            "category": "Sports",
            "category_slug": "sports",
            "excerpt": "Both semifinal matches went to overtime in what fans are calling the most exciting playoffs in years.",
            "content": "<p>The championship finals are set after two thrilling semifinal matches that each required overtime to determine a winner.</p><p>Fans witnessed incredible performances from star players on all four teams, with several records broken in the process.</p><p>The finals are scheduled to begin next week, with anticipation building for what promises to be an epic showdown.</p>",
            "author": "James Mitchell",
            "published_date": "2024-11-21",
            "source": "Sports Central",
            "reading_time": 4,
            "tags": [{"name": "Championship", "slug": "championship"}, {"name": "Playoffs", "slug": "playoffs"}]
        },
        {
            "id": "entertainment-001",
            "title": "Streaming Service Announces Major Original Content Expansion",
            "slug": "streaming-service-original-content-expansion",
            "category": "Entertainment",
            "category_slug": "entertainment",
            "excerpt": "Popular streaming platform reveals plans to double original programming budget in 2025.",
            "content": "<p>A leading streaming service has announced ambitious plans to significantly expand its original content offerings, doubling its production budget for the coming year.</p><p>The expansion will include new series from acclaimed creators, feature films, and documentary programming.</p><p>The move comes as competition in the streaming market intensifies, with platforms vying for subscriber attention.</p>",
            "author": "Rachel Green",
            "published_date": "2024-11-20",
            "source": "Entertainment Weekly",
            "reading_time": 3,
            "tags": [{"name": "Streaming", "slug": "streaming"}, {"name": "TV", "slug": "tv"}]
        }
    ]

    # Create data directory
    os.makedirs('data/articles', exist_ok=True)

    # Write sample data
    with open('data/articles/sample_articles.json', 'w', encoding='utf-8') as f:
        json.dump(sample_articles, f, indent=2)

    print("Sample data created in data/articles/sample_articles.json")


if __name__ == '__main__':
    main()
