#!/usr/bin/env python3
"""
PermitIndex Static Site Generator

This script generates static HTML pages for government transactions.
It reads data from CSV files and renders them using Jinja2 templates.

Directory Structure:
- /templates: Jinja2 templates
- /data: CSV data files
- /output: Generated HTML pages
- /static: Static assets (CSS, JS, images)
- /docs: Brand guidelines and documentation

Brand Guidelines:
All generated HTML must follow the PermitIndex brand color system.
See the following files for details:
- /docs/BRAND_GUIDELINES.md - Official brand guidelines
- /static/css/variables.css - CSS color variables
- /DEVELOPER.md - Developer guide for using brand colors

Color System:
- Primary Blue (#003366): Headers, links, primary buttons
- Accent Orange (#FF6B35): CTAs only (use sparingly!)
- Text Dark (#1a1a1a): Body text
- Text Light (#666666): Secondary text
- Backgrounds: #FFFFFF (cards), #F8F9FA (page)
- Borders: #E0E0E0

⚠️  IMPORTANT: Use CSS variables (var(--primary), var(--accent), etc.)
   instead of hardcoded colors or Tailwind classes.

Usage:
    python generator.py
"""

import os
import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import sys
import re


class SiteGenerator:
    """Main site generator class"""

    def __init__(self, base_dir=None):
        """
        Initialize the site generator

        Args:
            base_dir: Base directory path (defaults to script location)
        """
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.base_dir, 'templates')
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')

        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

        # Statistics
        self.stats = {
            'pages_generated': 0,
            'errors': 0,
            'start_time': datetime.now()
        }

    def slugify(self, text):
        """
        Convert text to URL-safe slug

        Args:
            text: Text to slugify

        Returns:
            URL-safe slug
        """
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and replace spaces with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        text = re.sub(r'^-+|-+$', '', text)
        return text

    def generate_url_slug(self, agency_short, request_type):
        """
        Generate URL slug from agency and request type

        Args:
            agency_short: Short agency name
            request_type: Type of permit/transaction

        Returns:
            URL slug (e.g., "california-food-truck-permit")
        """
        # Extract state/jurisdiction from agency name (e.g., "CA" -> "california")
        state_abbrev = agency_short.split()[0] if agency_short else ""

        # Map common state abbreviations to full names
        state_map = {
            'CA': 'california',
            'NY': 'new-york',
            'TX': 'texas',
            'FL': 'florida',
            # Add more as needed
        }

        state_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))

        # Slugify request type
        request_slug = self.slugify(request_type)

        # Combine: state-request-type
        return f"{state_slug}-{request_slug}"

    def load_data(self, csv_file):
        """
        Load data from CSV file

        Args:
            csv_file: Path to CSV file

        Returns:
            pandas DataFrame with loaded data
        """
        csv_path = os.path.join(self.data_dir, csv_file)
        print(f"📂 Loading data from: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
            print(f"✓ Loaded {len(df)} records")
            return df
        except FileNotFoundError:
            print(f"✗ Error: CSV file not found: {csv_path}")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            sys.exit(1)

    def generate_page(self, template_name, data, output_path):
        """
        Generate a single HTML page from template and data

        Args:
            template_name: Name of the Jinja2 template
            data: Dictionary of data to pass to template
            output_path: Full path where to save the generated HTML
        """
        try:
            # Load template
            template = self.env.get_template(template_name)

            # Render template with data
            html_content = template.render(**data)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✓ Generated: {output_path}")
            self.stats['pages_generated'] += 1

        except Exception as e:
            print(f"✗ Error generating page: {e}")
            import traceback
            traceback.print_exc()
            self.stats['errors'] += 1

    def split_numbered_steps(self, text):
        """
        Split a text with numbered steps (e.g., "1. Do this. 2. Do that.")
        into a list of clean step texts without the numbers.

        Args:
            text: String with numbered steps

        Returns:
            List of step strings without number prefixes
        """
        if not text:
            return []

        # Split by pattern: space + digit + period + space (e.g., " 2. ")
        # This preserves periods within sentences
        steps = re.split(r'\s+\d+\.\s+', text)

        # Clean up steps and remove number prefix from first step if present
        cleaned_steps = []
        for step in steps:
            step = step.strip()
            if step:
                # Remove leading number from first step (e.g., "1. text" -> "text")
                step = re.sub(r'^\d+\.\s*', '', step)
                cleaned_steps.append(step)

        return cleaned_steps

    def generate_transaction_pages(self, df):
        """
        Generate all transaction pages from CSV data

        Args:
            df: DataFrame with permit data
        """
        print("\n📄 Generating transaction pages...\n")

        # Generate a page for each row in the CSV
        for idx, row in df.iterrows():
            # Convert row to dictionary
            data = row.to_dict()

            # Parse JSON fields
            json_fields = ['community_feedback', 'user_tips', 'faqs']
            for field in json_fields:
                if field in data and isinstance(data[field], str) and data[field]:
                    try:
                        data[field] = json.loads(data[field])
                    except json.JSONDecodeError:
                        print(f"⚠️  Warning: Could not parse JSON for {field}")
                        data[field] = []
                else:
                    data[field] = []

            # Parse how_to_description into clean steps
            if 'how_to_description' in data and data['how_to_description']:
                data['how_to_steps'] = self.split_numbered_steps(data['how_to_description'])
            else:
                data['how_to_steps'] = []

            # Extract jurisdiction slug
            state_abbrev = data['agency_short'].split()[0] if data['agency_short'] else ""
            state_map = {
                'CA': 'california',
                'NY': 'new-york',
                'TX': 'texas',
                'FL': 'florida',
            }
            jurisdiction_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))
            data['jurisdiction_slug'] = jurisdiction_slug

            # Generate clean permit slug (just the permit name, not state-permit)
            permit_slug = self.slugify(data['request_type'])
            data['permit_slug'] = permit_slug

            # Full URL slug for compatibility (jurisdiction-permit)
            data['url_slug'] = f"{jurisdiction_slug}-{permit_slug}"

            # Build output path: /output/{jurisdiction}/{permit-slug}/index.html
            # This creates clean URLs like /california/food-truck-permit/
            output_path = os.path.join(
                self.output_dir,
                jurisdiction_slug,
                permit_slug,
                'index.html'
            )

            # Generate the page
            self.generate_page('transaction_page.html', data, output_path)

    def generate_jurisdiction_hubs(self, df):
        """
        Generate hub pages for each jurisdiction

        Args:
            df: DataFrame with permit data
        """
        print("\n🌎 Generating jurisdiction hub pages...\n")

        # Group permits by jurisdiction
        jurisdictions = {}
        for _, row in df.iterrows():
            state_abbrev = row['agency_short'].split()[0] if row['agency_short'] else ""
            state_map = {
                'CA': 'california',
                'NY': 'new-york',
                'TX': 'texas',
                'FL': 'florida',
            }
            jurisdiction_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))

            if jurisdiction_slug not in jurisdictions:
                jurisdictions[jurisdiction_slug] = {
                    'name': row['agency_short'],
                    'permits': []
                }

            permit_slug = self.slugify(row['request_type'])
            jurisdictions[jurisdiction_slug]['permits'].append({
                'request_type': row['request_type'],
                'agency_full': row['agency_full'],
                'description': row['description'] if 'description' in row else '',
                'cost': row['cost'],
                'processing_time': row['processing_time'] if 'processing_time' in row else row.get('effort_hours', ''),
                'online_available': row['online_available'],
                'api_available': row['api_available'],
                'mcp_available': row.get('mcp_available', 'No'),
                'permit_slug': permit_slug,
                'estimated_monthly_volume': row.get('estimated_monthly_volume', '0')
            })

        # Generate a hub page for each jurisdiction
        for jurisdiction_slug, data in jurisdictions.items():
            # Calculate statistics
            total_permits = len(data['permits'])
            online_permits = len([p for p in data['permits'] if p['online_available'] == 'Yes'])
            api_permits = len([p for p in data['permits'] if p['api_available'] == 'Yes'])
            mcp_permits = len([p for p in data['permits'] if p['mcp_available'] == 'Yes'])

            # Sort permits by monthly volume (most popular first)
            # Handle non-numeric values like '800-1200' by taking the first number
            def get_volume(permit):
                vol = permit.get('estimated_monthly_volume', '0')
                # Extract first number from string like '800-1200' -> 800
                import re
                match = re.search(r'\d+', str(vol))
                return int(match.group()) if match else 0

            sorted_permits = sorted(data['permits'], key=get_volume, reverse=True)

            # Get top 6 popular permits
            popular_permits = sorted_permits[:6]

            # Prepare template data
            template_data = {
                'jurisdiction_name': data['name'],
                'jurisdiction_slug': jurisdiction_slug,
                'total_permits': total_permits,
                'online_permits': online_permits,
                'api_permits': api_permits,
                'mcp_permits': mcp_permits,
                'popular_permits': popular_permits,
                'all_permits': sorted_permits
            }

            # Generate hub page at /output/{jurisdiction}/index.html
            output_path = os.path.join(
                self.output_dir,
                jurisdiction_slug,
                'index.html'
            )

            self.generate_page('jurisdiction_hub.html', template_data, output_path)

    def generate_homepage(self, df):
        """
        Generate the homepage (index.html) with agency and permit listings

        Args:
            df: DataFrame with permit data
        """
        print("\n🏠 Generating homepage...")

        # Calculate statistics
        stats = {
            'total_permits': len(df),
            'total_agencies': df['agency_full'].nunique(),
            'online_permits': len(df[df['online_available'] == 'Yes']),
            'api_permits': len(df[df['api_available'] == 'Yes'])
        }

        # Get list of agencies with permit counts
        agency_counts = df.groupby('agency_short').size().reset_index(name='permit_count')
        jurisdictions = []
        for _, row in agency_counts.iterrows():
            # Generate slug for agency
            agency_slug = self.slugify(row['agency_short'])
            jurisdictions.append({
                'name': row['agency_short'],
                'slug': agency_slug,
                'permit_count': row['permit_count']
            })

        # Sort agencies alphabetically
        jurisdictions = sorted(jurisdictions, key=lambda x: x['name'])

        # Get recent/featured permits (all permits for now)
        recent_permits = []
        for _, row in df.iterrows():
            state_abbrev = row['agency_short'].split()[0] if row['agency_short'] else ""
            state_map = {
                'CA': 'california',
                'NY': 'new-york',
                'TX': 'texas',
                'FL': 'florida',
            }
            jurisdiction_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))
            permit_slug = self.slugify(row['request_type'])

            recent_permits.append({
                'agency_short': row['agency_short'],
                'request_type': row['request_type'],
                'cost': row['cost'],
                'effort_hours': row['effort_hours'],
                'online_available': row['online_available'],
                'url_slug': f"/{jurisdiction_slug}/{permit_slug}/",
                'jurisdiction_slug': jurisdiction_slug,
                'permit_slug': permit_slug,
                'location_applicability': row['location_applicability']
            })

        # Prepare template data
        template_data = {
            'stats': stats,
            'jurisdictions': jurisdictions,
            'recent_permits': recent_permits
        }

        # Generate homepage
        output_path = os.path.join(self.output_dir, 'index.html')
        self.generate_page('index.html', template_data, output_path)

    def generate_sitemap(self, df):
        """
        Generate sitemap.xml with all page URLs and lastmod dates

        Args:
            df: DataFrame with permit data
        """
        print("\n🗺️  Generating sitemap.xml...")

        # Base URL for the site
        base_url = "https://ainews123.com"

        # Build sitemap XML
        sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        # Add homepage
        sitemap_content.append('  <url>')
        sitemap_content.append(f'    <loc>{base_url}/</loc>')
        sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_content.append('    <changefreq>daily</changefreq>')
        sitemap_content.append('    <priority>1.0</priority>')
        sitemap_content.append('  </url>')

        # Add jurisdiction hub pages
        jurisdictions = df.groupby('agency_short').first().reset_index()
        jurisdiction_slugs_added = set()

        for _, row in jurisdictions.iterrows():
            state_abbrev = row['agency_short'].split()[0] if row['agency_short'] else ""
            state_map = {
                'CA': 'california',
                'NY': 'new-york',
                'TX': 'texas',
                'FL': 'florida',
            }
            jurisdiction_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))

            if jurisdiction_slug not in jurisdiction_slugs_added:
                jurisdiction_slugs_added.add(jurisdiction_slug)
                url = f"{base_url}/{jurisdiction_slug}/"

                sitemap_content.append('  <url>')
                sitemap_content.append(f'    <loc>{url}</loc>')
                sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
                sitemap_content.append('    <changefreq>weekly</changefreq>')
                sitemap_content.append('    <priority>0.9</priority>')
                sitemap_content.append('  </url>')

        # Add transaction pages with hierarchical URLs
        for idx, row in df.iterrows():
            state_abbrev = row['agency_short'].split()[0] if row['agency_short'] else ""
            state_map = {
                'CA': 'california',
                'NY': 'new-york',
                'TX': 'texas',
                'FL': 'florida',
            }
            jurisdiction_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))
            permit_slug = self.slugify(row['request_type'])

            # Use hierarchical URL: /jurisdiction/permit-slug/
            url = f"{base_url}/{jurisdiction_slug}/{permit_slug}/"

            sitemap_content.append('  <url>')
            sitemap_content.append(f'    <loc>{url}</loc>')
            sitemap_content.append(f'    <lastmod>{row["date_extracted"]}</lastmod>')
            sitemap_content.append('    <changefreq>weekly</changefreq>')
            sitemap_content.append('    <priority>0.8</priority>')
            sitemap_content.append('  </url>')

        sitemap_content.append('</urlset>')

        # Write sitemap
        sitemap_path = os.path.join(self.output_dir, 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sitemap_content))

        print(f"✓ Sitemap generated: {sitemap_path}")

    def generate_data_json(self, df):
        """
        Generate data.json for future search/filter features

        Args:
            df: DataFrame with permit data
        """
        print("\n📊 Generating data.json...")

        # Convert DataFrame to list of dicts with URL slugs
        permits_data = []
        for _, row in df.iterrows():
            permit = row.to_dict()

            # Generate hierarchical URL
            state_abbrev = row['agency_short'].split()[0] if row['agency_short'] else ""
            state_map = {
                'CA': 'california',
                'NY': 'new-york',
                'TX': 'texas',
                'FL': 'florida',
            }
            jurisdiction_slug = state_map.get(state_abbrev, self.slugify(state_abbrev))
            permit_slug = self.slugify(row['request_type'])

            # Add generated URL slug (hierarchical format)
            permit['url_slug'] = f"/{jurisdiction_slug}/{permit_slug}/"
            permit['jurisdiction_slug'] = jurisdiction_slug
            permit['permit_slug'] = permit_slug

            # Remove source_url (internal only)
            if 'source_url' in permit:
                del permit['source_url']
            permits_data.append(permit)

        # Create data structure
        data = {
            'generated_at': datetime.now().isoformat(),
            'total_permits': len(permits_data),
            'permits': permits_data
        }

        # Write JSON file
        json_path = os.path.join(self.output_dir, 'data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Data JSON generated: {json_path}")

    def generate_robots_txt(self):
        """Generate robots.txt with sitemap location"""
        print("\n🤖 Generating robots.txt...")

        robots_content = [
            "# PermitIndex robots.txt",
            "# Allow all crawlers",
            "",
            "User-agent: *",
            "Allow: /",
            "",
            "# Sitemap location",
            "Sitemap: https://ainews123.com/sitemap.xml"
        ]

        # Write robots.txt
        robots_path = os.path.join(self.output_dir, 'robots.txt')
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(robots_content))

        print(f"✓ Robots.txt generated: {robots_path}")

    def copy_favicon_files(self):
        """Copy favicon files from static/favicon to output/favicon"""
        import shutil

        print("🎨 Copying favicon files...")

        source_dir = os.path.join('static', 'favicon')
        dest_dir = os.path.join(self.output_dir, 'favicon')

        if not os.path.exists(source_dir):
            print("⚠️  Warning: static/favicon directory not found, skipping favicon copy")
            return

        # Ensure destination directory exists
        os.makedirs(dest_dir, exist_ok=True)

        # Copy all files from source to destination
        try:
            for filename in os.listdir(source_dir):
                source_file = os.path.join(source_dir, filename)
                if os.path.isfile(source_file):
                    shutil.copy2(source_file, os.path.join(dest_dir, filename))
            print(f"✓ Favicon files copied: {dest_dir}")
        except Exception as e:
            print(f"✗ Error copying favicon files: {e}")
            self.stats['errors'] += 1

    def print_statistics(self):
        """Print generation statistics"""
        end_time = datetime.now()
        duration = (end_time - self.stats['start_time']).total_seconds()

        print("\n" + "=" * 60)
        print("📊 GENERATION STATISTICS")
        print("=" * 60)
        print(f"Pages generated: {self.stats['pages_generated']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Output directory: {self.output_dir}")
        print("=" * 60 + "\n")

    def generate(self):
        """Run the complete site generation process"""
        print("\n" + "=" * 60)
        print("🏛️  PERMITINDEX STATIC SITE GENERATOR")
        print("=" * 60)

        # Load data once
        df = self.load_data('permits.csv')

        # Generate homepage
        self.generate_homepage(df)

        # Generate jurisdiction hub pages
        self.generate_jurisdiction_hubs(df)

        # Generate transaction pages
        self.generate_transaction_pages(df)

        # Generate sitemap
        self.generate_sitemap(df)

        # Generate data.json
        self.generate_data_json(df)

        # Generate robots.txt
        self.generate_robots_txt()

        # Copy favicon files
        self.copy_favicon_files()

        # Print statistics
        self.print_statistics()

        if self.stats['errors'] == 0:
            print("✅ Site generation completed successfully!\n")
            return 0
        else:
            print("⚠️  Site generation completed with errors.\n")
            return 1


def main():
    """Main entry point"""
    generator = SiteGenerator()
    return generator.generate()


if __name__ == '__main__':
    sys.exit(main())
