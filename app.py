import os
import feedparser
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class NewsletterGenerator:
    def __init__(self, user_preferences=None):
        self.categories = {
            'tech': [
                'http://feeds.feedburner.com/TechCrunch',
                'https://www.wired.com/feed/rss',
                'https://www.technologyreview.com/feed',
                'http://feeds.arstechnica.com/arstechnica/technology-lab'
            ],
            'finance': [
                'http://feeds.bloomberg.com/bloomberg/technology',
                'https://www.cnbc.com/id/19854910/device/rss/rss.html',
                'https://www.ft.com/technology?format=rss'
            ],
            'sports': [
                'https://www.espn.com/espn/rss/news',
                'http://feeds.bbci.co.uk/sport/rss.xml',
                'https://www.skysports.com/rss/12040'
            ],
            'entertainment': [
                'https://variety.com/feed/',
                'https://www.hollywoodreporter.com/feed',
                'https://www.billboard.com/feed/'
            ],
            'science': [
                'https://www.nasa.gov/rss/dyn/breaking_news.rss',
                'https://www.sciencedaily.com/rss/all.xml',
                'http://feeds.arstechnica.com/arstechnica/science'
            ]
        }
        
        self.user_preferences = user_preferences if user_preferences else ['tech', 'science']
        self.rss_feeds = []
        for category in self.user_preferences:
            if category in self.categories:
                self.rss_feeds.extend(self.categories[category])

    def fetch_articles(self):
        """Fetch articles from RSS feeds"""
        articles = []
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Get top 5 articles from each feed
                    articles.append({
                        'title': entry.title,
                        'summary': entry.summary,
                        'link': entry.link,
                        'source': feed.feed.title
                    })
            except Exception as e:
                print(f"Error fetching from {feed_url}: {str(e)}")
        return articles

    def analyze_article(self, article):
        """Analyze article content using OpenAI API and determine relevance"""
        try:
            prompt = f"Analyze this news article and provide:\n1. A brief, engaging summary\n2. The main category (tech, finance, sports, entertainment, or science)\n3. A relevance score (0-10) for the article based on its content quality and newsworthiness\n\nTitle: {article['title']}\nContent: {article['summary']}"
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                
            )
            
            analysis = response.choices[0].message.content
            return analysis
        except Exception as e:
            print(f"Error analyzing article: {str(e)}")
            return article['summary']

    def generate_newsletter(self):
        """Generate the complete personalized newsletter"""
        articles = self.fetch_articles()
        newsletter_content = []

        for article in articles:
            analysis = self.analyze_article(article)
            # Parse the analysis to extract category and relevance score
            lines = analysis.split('\n')
            summary = lines[0] if lines else ''
            category = next((line.split(':')[1].strip().lower() for line in lines if 'category' in line.lower() and ':' in line and len(line.split(':')) > 1), '')
            # Extract relevance score with better error handling
            relevance = 0
            try:
                for line in lines:
                    if 'relevance' in line.lower() and ':' in line and len(line.split(':')) > 1:
                        relevance_text = line.split(':')[1].strip()
                        # Handle cases like "Relevance: 7/10" or just "Relevance: 7"
                        if '/' in relevance_text:
                            relevance_text = relevance_text.split('/')[0].strip()
                        if relevance_text and relevance_text.isdigit():
                            relevance = int(relevance_text)
                            break
            except Exception as e:
                print(f"Error parsing relevance score: {str(e)}")
                relevance = 0
            
            # Only include articles that match user preferences and have good relevance
            if category in self.user_preferences and relevance >= 6:
                newsletter_content.append({
                    'title': article['title'],
                    'analysis': summary,
                    'category': category,
                    'relevance': relevance,
                    'link': article['link'],
                    'source': article['source']
                })

        # Sort articles by relevance score
        newsletter_content.sort(key=lambda x: x['relevance'], reverse=True)
        return newsletter_content

if __name__ == '__main__':
    # Define user personas
    personas = {
        'tech_enthusiast': ['tech', 'science'],
        'finance_guru': ['finance', 'tech'],
        'sports_journalist': ['sports'],
        'entertainment_buff': ['entertainment'],
        'science_nerd': ['science', 'tech']
    }
    
    # Generate newsletter for each persona
    for persona, preferences in personas.items():
        print(f"\n=== Newsletter for {persona.replace('_', ' ').title()} ===")
        newsletter = NewsletterGenerator(user_preferences=preferences)
        content = newsletter.generate_newsletter()
        
        # Print the personalized newsletter content
        for article in content:
            print(f"\n[{article['category'].upper()}] {article['title']}")
            print(f"Source: {article['source']}")
            print(f"Relevance Score: {article['relevance']}/10")
            print(f"Analysis: {article['analysis']}")
            print(f"Read more: {article['link']}\n")
            print("-" * 80)