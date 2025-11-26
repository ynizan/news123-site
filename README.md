# News123 - Static News Site Generator

A Python-based static site generator for creating a news aggregation website.

## Project Overview

News123 is a static news site that aggregates and displays news articles across multiple categories. The site provides a clean, fast reading experience with category browsing, search functionality, and mobile-responsive design.

## Features

- 📰 **News Aggregation**: Display articles from multiple sources
- 🗂️ **Categories**: Organized by Technology, Business, Politics, Sports, Entertainment, and more
- 🔍 **Search**: Find articles by keyword or topic
- 📱 **Mobile Responsive**: Works seamlessly on all devices
- 🔗 **SEO Optimized**: Full meta tags and JSON-LD structured data
- 🚀 **Fast Generation**: Static HTML for blazing-fast performance

## Project Structure

```
news123-site/
├── data/
│   └── articles/            # News article database (JSON format)
│       └── sample_articles.json
├── templates/
│   ├── index.html           # Homepage template
│   ├── article_page.html    # Individual article page template
│   ├── category_page.html   # Category listing template
│   └── components/
│       ├── header.html      # Site header
│       └── footer.html      # Site footer
├── output/                   # Generated static HTML files (git-ignored)
│   ├── index.html
│   ├── sitemap.xml
│   ├── robots.txt
│   └── {category}/{slug}/   # Article pages
├── static/                   # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── variables.css    # Brand color system
│   └── favicon/
├── generator.py              # Main site generator script
└── requirements.txt          # Python dependencies
```

## Data Schema

### Article Fields

**Required Fields:**
- `id` - Unique identifier
- `title` - Article headline
- `slug` - URL-friendly slug
- `category` - Category name
- `category_slug` - Category URL slug
- `excerpt` - Short description
- `content` - Full article content (HTML)
- `author` - Author name
- `published_date` - Publication date (YYYY-MM-DD)
- `source` - News source name

**Optional Fields:**
- `source_url` - Original source URL
- `image_url` - Featured image URL
- `image_caption` - Image caption
- `tags` - List of tags
- `reading_time` - Estimated reading time in minutes
- `updated_date` - Last updated date
- `is_breaking` - Breaking news flag
- `is_featured` - Featured article flag
- `related_articles` - List of related article IDs

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ynizan/news123-site.git
   cd news123-site
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the site:**
   ```bash
   python3 generator.py
   ```

## Usage

### Generating the Site

Run the generator to create all HTML pages:

```bash
python3 generator.py
```

This will:
- Load articles from all JSON files in `data/articles/`
- Generate homepage at `output/index.html`
- Generate individual article pages at `output/{category}/{slug}/index.html`
- Generate category pages at `output/category/{slug}/index.html`
- Create `sitemap.xml`
- Create `robots.txt`

### Adding New Articles

1. **Add entries to a JSON file in `data/articles/`**
2. **Fill the required fields** (see schema above)
3. **Run the generator**: `python3 generator.py`
4. **Test the output** by viewing generated HTML files

### Preview Pages Locally

Use Python's built-in HTTP server:

```bash
cd output
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Brand Colors

News123 uses a dark blue and red accent color scheme:

- **Primary** (`#1a1a2e`): Headers, navigation, primary elements
- **Accent** (`#e94560`): Breaking news, CTAs, category badges
- **Text** (`#1a1a1a`): Body text
- **Text Light** (`#666666`): Secondary text, meta information
- **Background** (`#f8f9fa`): Page background
- **Background White** (`#ffffff`): Card backgrounds

## Generated Pages

### Homepage (`/index.html`)
- Hero section with search bar
- Statistics dashboard (total articles, sources, categories)
- Category pills for quick navigation
- Latest news grid
- Featured topics section
- Newsletter signup

### Article Pages (`/{category}/{slug}/index.html`)
Each article page includes:
- Category badge
- Article title and metadata
- Author and publication date
- Reading time
- Full article content
- Tags
- Related articles
- Source attribution

### Category Pages (`/category/{slug}/index.html`)
- Category name and article count
- Chronological list of articles in that category

## SEO Features

- ✅ Comprehensive meta tags (title, description)
- ✅ Open Graph tags for social sharing
- ✅ Twitter Card tags
- ✅ Canonical URLs
- ✅ JSON-LD structured data (NewsArticle, Organization, WebSite)
- ✅ Semantic HTML5 structure
- ✅ Sitemap.xml
- ✅ Robots.txt

## Development

### Requirements
- Python 3.7+
- jinja2

### Customization

**Templates:**
- Edit `templates/index.html` for homepage layout
- Edit `templates/article_page.html` for article pages
- Edit `templates/components/header.html` and `footer.html` for site-wide components
- Uses Tailwind CSS via CDN

**Styling:**
- Tailwind CSS for rapid UI development
- Custom color scheme defined in `static/css/variables.css`
- Responsive breakpoints: mobile, tablet, desktop

## Future Enhancements

- [ ] Client-side search
- [ ] RSS feed generation
- [ ] Newsletter integration
- [ ] Social sharing buttons
- [ ] Comment system
- [ ] Author profile pages
- [ ] Tag pages
- [ ] Pagination for category pages

## License

© 2024 News123. All rights reserved.

---

**Last Updated:** 2024-11-25
**Version:** 1.0.0
