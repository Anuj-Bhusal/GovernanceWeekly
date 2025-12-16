import argparse
import logging
from datetime import datetime, timedelta
import sys
import json
import sqlite3
import os

# Basic debug print
print("DEBUG: Script starting", flush=True)

from database.db import init_db, get_db
print("DEBUG: Imported DB", flush=True)

from scrapers.domain_scrapers.ekantipur import EkantipurScraper
print("DEBUG: Imported Ekantipur", flush=True)
from scrapers.domain_scrapers.kathmandu_post import KathmanduPostScraper
print("DEBUG: Imported KP", flush=True)
from scrapers.domain_scrapers.myrepublica import MyRepublicaScraper
print("DEBUG: Imported MyRepublica", flush=True)
from scrapers.domain_scrapers.setopati import SetopatiScraper
print("DEBUG: Imported Setopati", flush=True)
from scrapers.domain_scrapers.nayapatrika import NayapatrikaScraper
print("DEBUG: Imported Nayapatrika", flush=True)
from scrapers.domain_scrapers.annapurna_post import AnnapurnaPostScraper
print("DEBUG: Imported AnnapurnaPost", flush=True)
from scrapers.domain_scrapers.annapurna_express import AnnapurnaExpressScraper
print("DEBUG: Imported AnnapurnaExpress", flush=True)
from scrapers.domain_scrapers.onlinekhabar import OnlineKhabarScraper
print("DEBUG: Imported OnlineKhabar", flush=True)
from scrapers.domain_scrapers.ratopati import RatopatiScraper
print("DEBUG: Imported Ratopati", flush=True)
from scrapers.domain_scrapers.ukaalo import UkaaloScraper
print("DEBUG: Imported Ukaalo", flush=True)
from translator.translator import Translator
print("DEBUG: Imported Translator", flush=True)
from classifier.classifier import Classifier
print("DEBUG: Imported Classifier", flush=True)
from reporting.summarizer import Summarizer
print("DEBUG: Imported Summarizer", flush=True)
from reporting.pdf_generator import build_pdf
print("DEBUG: Imported PDF Gen", flush=True)
from reporting.drive_uploader import DriveUploader
print("DEBUG: Imported Drive", flush=True)
from config import Config
print("DEBUG: Imported Config", flush=True)
from utils.article_filter import filter_top_articles, get_category_distribution
print("DEBUG: Imported Article Filter", flush=True)

logger = logging.getLogger("GovernanceWeekly")

def has_nepali(text):
    """Check if text contains Nepali Unicode characters"""
    if not text:
        return False
    return any('\u0900' <= char <= '\u097F' for char in text)

def setup():
    print("DEBUG: Inside setup", flush=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    init_db()
    print("DEBUG: init_db done", flush=True)

def collect(target_scraper=None):
    print("DEBUG: Inside collect", flush=True)
    logger.info("Starting collection phase...")
    db_gen = get_db()
    db = next(db_gen)
    print("DEBUG: Got DB connection", flush=True)
    
    # Calculate date range: last Friday to today
    from datetime import datetime, timedelta
    today = datetime.now()
    days_since_friday = (today.weekday() - 4) % 7  # Friday is 4
    if days_since_friday == 0 and today.hour < 12:  # If it's Friday morning, go back a week
        days_since_friday = 7
    last_friday = today - timedelta(days=days_since_friday)
    last_friday = last_friday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    logger.info(f"Collecting articles from {last_friday.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
    
    all_scrapers = [
        EkantipurScraper(),
        KathmanduPostScraper(),
        MyRepublicaScraper(),
        SetopatiScraper(),
        NayapatrikaScraper(),
        AnnapurnaPostScraper(),
        AnnapurnaExpressScraper(),
        OnlineKhabarScraper(),
        RatopatiScraper(),
        UkaaloScraper()
    ]
    
    if target_scraper:
        scrapers = [s for s in all_scrapers if target_scraper.lower() in s.__class__.__name__.lower()]
        if not scrapers:
            logger.error(f"No scraper found matching '{target_scraper}'")
            return
        logger.info(f"Running only: {[s.__class__.__name__ for s in scrapers]}")
    else:
        scrapers = all_scrapers
    
    print(f"DEBUG: Init {len(scrapers)} scrapers", flush=True)
    
    translator = Translator()
    print("DEBUG: Init Translator", flush=True)
    classifier = Classifier()
    print("DEBUG: Init Classifier", flush=True)
    
    total_new = 0
    
    try:
        for scraper in scrapers:
            try:
                articles = scraper.run()
                for data in articles:
                    # 1. Date filter - skip articles outside date range
                    if data.get('published_at'):
                        # Make both timezone-naive for comparison
                        pub_date = data['published_at']
                        if pub_date.tzinfo is not None:
                            pub_date = pub_date.replace(tzinfo=None)
                        
                        if pub_date < last_friday or pub_date > today:
                            logger.debug(f"Skipping article outside date range: {data.get('title', 'No title')[:50]} (published: {pub_date})")
                            continue
                    
                    # 2. Deduplication check by URL
                    db.cursor.execute("SELECT 1 FROM articles WHERE url = ?", (data['url'],))
                    if db.cursor.fetchone():
                        continue
                    
                    # 3. Deduplication check by title similarity (catch same news from different sources)
                    title_to_check = data.get('title', '').strip()
                    if title_to_check:
                        db.cursor.execute("SELECT title_original FROM articles")
                        existing_titles = [row[0] for row in db.cursor.fetchall()]
                        
                        from difflib import SequenceMatcher
                        for existing_title in existing_titles:
                            similarity = SequenceMatcher(None, title_to_check.lower(), existing_title.lower()).ratio()
                            if similarity >= 0.85:  # 85% similar titles = duplicate
                                logger.debug(f"Skipping duplicate by title: {title_to_check[:50]}")
                                continue
                    
                    # 4. Filter out opinion/commentary content by URL and title patterns
                    url_lower = data['url'].lower()
                    title_lower = data.get('title', '').lower()
                    
                    opinion_patterns = [
                        '/opinion/', '/editorial/', '/commentary/', '/column/',
                        '/interview/', '/op-ed/', '/blog/', '/viewpoint/',
                        'opinion', 'editorial', 'commentary', 'interview',
                        'exclusive interview', 'in conversation', 'my view'
                    ]
                    
                    if any(pattern in url_lower or pattern in title_lower for pattern in opinion_patterns):
                        logger.info(f"Skipping opinion/interview content: {data['title']}")
                        continue
                    
                    # 5. Translation - ensure Nepali content is properly translated
                    # Check both title and full_text for Nepali characters
                    needs_translation = (
                        data.get('language') == 'ne' or 
                        has_nepali(data.get('title', '')) or 
                        has_nepali(data.get('full_text', ''))
                    )
                    
                    if needs_translation:
                        # Translate title
                        try:
                            trans_title = translator.translate(data['title'], source_lang='ne', target_lang='en')
                            # If translation returns original Nepali (and it was Nepali), mark as failed
                            if has_nepali(trans_title) and has_nepali(data['title']):
                                data['title_translated'] = "[Translation Failed]"
                            else:
                                data['title_translated'] = trans_title
                        except Exception as e:
                            logger.warning(f"Title translation failed for {data['url']}: {e}")
                            data['title_translated'] = "[Translation Failed]"
                        
                        # Translate full text (chunk if needed)
                        try:
                            full_text = data.get('full_text', '')
                            if len(full_text) > 4000:
                                # Chunk large text
                                chunks = [full_text[i:i+4000] for i in range(0, len(full_text), 4000)]
                                translated_chunks = []
                                for chunk in chunks:
                                    trans_chunk = translator.translate(chunk, source_lang='ne', target_lang='en')
                                    translated_chunks.append(trans_chunk)
                                data['full_text_translated'] = ' '.join(translated_chunks)
                            else:
                                data['full_text_translated'] = translator.translate(full_text, source_lang='ne', target_lang='en')
                                
                            # Check if full text translation failed (still contains Nepali)
                            if has_nepali(data['full_text_translated']) and has_nepali(full_text):
                                logger.warning(f"Full text translation returned Nepali for {data['url']}")
                                # Try to keep what we have or mark failed? 
                                # If it's mostly Nepali, it's useless for summary.
                                # But maybe some parts translated.
                                pass 
                        except Exception as e:
                            logger.warning(f"Text translation failed for {data['url']}: {e}")
                            data['full_text_translated'] = "" # Empty better than blocks
                    else:
                        data['title_translated'] = data['title']
                        data['full_text_translated'] = data['full_text']
                    
                    # 6. Generate summary from translated text (for English summaries)
                    summary_text = ""
                    if data.get('full_text_translated'):
                        temp_summarizer = Summarizer()
                        summary_text = temp_summarizer.summarize(data['full_text_translated'])
                    
                    # 7. Classification
                    text_for_class = (data.get('title_translated') or "") + "\n" + (data.get('full_text_translated') or "")
                    classification = classifier.classify(text_for_class)
                    
                    # Skip if excluded (opinion/commentary detected by classifier)
                    if classification.get('is_excluded'):
                        logger.info(f"Skipping excluded content: {data['title']}")
                        continue
                        
                    # Insert
                    # Serialize complex types
                    cats_json = json.dumps(classification['categories'])
                    
                    db.cursor.execute("""
                        INSERT INTO articles (
                            url, source_domain, title_original, full_text_original, 
                            published_at, fetched_at, language, 
                            title_translated, full_text_translated, summary,
                            categories, relevance_score, raw_html, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data['url'],
                        data['source_domain'],
                        data['title'],
                        data['full_text'],
                        data.get('published_at'), # datetime object usually works with sqlite3 adapter
                        datetime.utcnow(),
                        data.get('language', 'ne'),
                        data['title_translated'],
                        data['full_text_translated'],
                        summary_text,
                        cats_json,
                        classification['relevance_score'],
                        data.get('raw_html'),
                        "pending_review"
                    ))
                    
                    total_new += 1
                    
                db.commit()
            except Exception as e:
                logger.error(f"Scraper {scraper.domain} failed: {e}")
                db.rollback()
    finally:
        db.close()

    logger.info(f"Collection complete. New articles: {total_new}")

def summarize_and_report():
    logger.info("Starting reporting phase...")
    db_gen = get_db()
    db = next(db_gen)
    summarizer = Summarizer()
    
    try:
        # Get items from last Friday to today
        # This gives you the week's news: Friday → Thursday (when run weekly)
        today = datetime.now()
        days_since_friday = (today.weekday() - 4) % 7  # Friday is 4
        if days_since_friday == 0 and today.hour < 12:  # If it's Friday morning, go back a week
            days_since_friday = 7
        last_friday = today - timedelta(days=days_since_friday)
        last_friday = last_friday.replace(hour=0, minute=0, second=0, microsecond=0)
        
        db.cursor.execute("SELECT * FROM articles WHERE fetched_at >= ?", (last_friday,))
        rows = db.cursor.fetchall()
        
        items_by_category = {}
        all_articles = []
        
        for row in rows:
            # Row to dict
            row_dict = dict(row)
            
            # Generate summary if missing
            if not row_dict.get('summary'):
                text_to_sum = row_dict.get('full_text_translated') or row_dict.get('full_text_original') or ""
                summary_text = summarizer.summarize(text_to_sum)
                
                # Update DB
                db.cursor.execute("UPDATE articles SET summary = ? WHERE url = ?", (summary_text, row_dict['url']))
                row_dict['summary'] = summary_text
            
            # Helper to parse json categories
            try:
                cats = json.loads(row_dict.get('categories') or "[]")
            except:
                cats = []
            
            # Skip if no relevant categories (exclude Uncategorized)
            if not cats:
                continue
                
            relevance = row_dict.get('relevance_score', 0)
            
            article_data = {
                'title_translated': row_dict.get('title_translated'),
                'title_original': row_dict.get('title_original'),
                'summary': row_dict.get('summary'),
                'source_domain': row_dict.get('source_domain'),
                'published_at': str(row_dict.get('published_at')),
                'url': row_dict.get('url'),
                'categories': cats,
                'relevance_score': relevance
            }
            all_articles.append(article_data)
        
        logger.info(f"Total articles before filtering: {len(all_articles)}")
        
        # Apply smart filtering to get top most impactful articles
        # Configurable via MAX_ARTICLES_IN_REPORT and MIN_IMPACT_SCORE in .env
        # This includes:
        # - Content-based deduplication (similar articles from different sources)
        # - Impact scoring (category priority + relevance + content depth)
        # - Quality threshold filtering
        top_articles = filter_top_articles(
            all_articles, 
            max_articles=Config.MAX_ARTICLES_IN_REPORT, 
            min_impact_score=Config.MIN_IMPACT_SCORE
        )
        
        logger.info(f"Top articles after filtering: {len(top_articles)}")
        
        # Log category distribution
        category_dist = get_category_distribution(top_articles)
        logger.info(f"Category distribution: {category_dist}")
        
        # Group by category (ensure each article appears only once)
        seen_urls = set()
        for article in top_articles:
            # Skip if already added to another category
            if article['url'] in seen_urls:
                continue
                
            seen_urls.add(article['url'])
            
            # Add to the FIRST (highest priority) category only
            if article['categories']:
                primary_category = article['categories'][0]  # First category is highest priority
                if primary_category not in items_by_category:
                    items_by_category[primary_category] = []
                
                items_by_category[primary_category].append({
                    'title_translated': article['title_translated'],
                    'title_original': article['title_original'],
                    'summary': article['summary'],
                    'source_domain': article['source_domain'],
                    'published_at': article['published_at'],
                    'url': article['url'],
                    'relevance_score': article['relevance_score'],
                    'impact_score': article['impact_score']
                })
                
        db.commit()
        
        # Generate PDF
        filename = f"GovernanceWeekly_{datetime.now().strftime('%Y%m%d')}.pdf"
        out_path = os.path.join(Config.OUTPUT_DIR, filename)
        date_range = f"{last_friday.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"
        
        if build_pdf(items_by_category, out_path, date_range):
            uploader = DriveUploader(Config.DRIVE_FOLDER_ID)
            uploader.upload(out_path)
            
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Governance Weekly Pipeline")
    parser.add_argument("--mode", choices=["collect", "summarize", "force", "export-for-review"], required=True)
    parser.add_argument("--scraper", help="Run specific scraper (e.g. 'onlinekhabar')", default=None)
    args = parser.parse_args()
    
    setup()
    
    if args.mode == "collect":
        collect(target_scraper=args.scraper)
    elif args.mode == "summarize":
        summarize_and_report()
    elif args.mode == "force":
        collect(target_scraper=args.scraper)
        summarize_and_report()
    elif args.mode == "export-for-review":
        print("Export feature pending implementation.")

if __name__ == "__main__":
    main()
