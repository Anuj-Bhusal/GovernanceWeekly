from scrapers.base_scraper import BaseScraper
from extractor.article_extractor import extract_article
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SetopatiScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.setopati.com", "setopati.com")

    def run(self):
        logger.info(f"Starting scrape for {self.domain}")
        
        homepage_html = self.fetch(self.base_url)
        if not homepage_html:
            return []
            
        links = self.extract_links(homepage_html)
        
        # Setopati uses numeric article IDs, no year in URL
        # Filter for relevant sections
        article_links = [l for l in links if any(x in l for x in ["/politics/", "/social/", "/kinmel/", "/nepali-brand/"])]
        
        # Exclude opinion/blog/story/interview URLs
        article_links = [l for l in article_links if not any(x in l.lower() for x in ['/opinion/', '/blog/', '/column/', '/interview/', '/story/', '/editorial/', '/bichar/', '/bisleshan/'])]
        
        article_links = list(article_links)[:self.max_articles]
        logger.info(f"Found {len(article_links)} potential articles")
        
        results = []
        for link in article_links:
            html = self.fetch(link)
            if html:
                data = extract_article(html, link)
                if data and data['title']:
                    data['url'] = link
                    data['source_domain'] = self.domain
                    data['language'] = 'ne'  # Setopati is Nepali
                    results.append(data)
            
        return results
