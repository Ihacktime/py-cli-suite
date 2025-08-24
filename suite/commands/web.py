import click
import urllib.request
from bs4 import BeautifulSoup
import os

@click.group()
def web():
    """Web tools: scraping, downloading, etc."""
    pass

@web.command()
@click.argument('url')
@click.option('--selector', '-s', default='.league-standing', 
              help='CSS selector to extract specific elements')
@click.option('--output', '-o', default='output/page.html', 
              help='Output file path')
def scrape(url, selector, output):
    """Scrape content from a webpage using a CSS selector."""
    try:
        response = urllib.request.urlopen(url)
        html = response.read()
        parser = "html.parser"
        sp = BeautifulSoup(html, parser, from_encoding='UTF-8')
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output), exist_ok=True)
        
        # Extract content based on selector
        if selector:
            selected_elements = sp.select(selector)
            if selected_elements:
                html_content = str(selected_elements[0])
            else:
                click.echo(f"No elements found with selector: {selector}")
                return
        else:
            html_content = str(sp)
        
        # Write to file
        with open(output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        click.echo(f"Successfully scraped content to {output}")
        
    except Exception as e:
        click.echo(f"Error scraping website: {e}")