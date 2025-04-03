# content.py
import feedparser
import openai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from config import OPENAI_API_KEY, OPENAI_MODEL, DEFAULT_RSS_URL

openai.api_key = OPENAI_API_KEY

def fetch_rss(url=DEFAULT_RSS_URL):
    feed = feedparser.parse(url)
    if not feed.entries:
        return None
    return feed.entries

def summarize_text(text, max_length=200):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 2)
        return " ".join([str(sentence) for sentence in summary])[:max_length]
    except:
        return text[:max_length]

def translate_text(text):
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a translator. Translate the following English text to natural and fluent Turkish."},
                {"role": "user", "content": f"Translate this text to Turkish: {text}"}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Çeviri hatası: {str(e)}"

def generate_content(topic):
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a content creator. Generate a 100-word post in Turkish on the given topic. Use a friendly tone and ensure the content is accurate and culturally appropriate for Turkish readers."},
                {"role": "user", "content": f"Generate a post on this topic: {topic}"}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"İçerik oluşturma hatası: {str(e)}"

def process_rss_content(template):
    entries = fetch_rss()
    if not entries:
        return None
    entry = entries[0]
    title = entry.title
    summary = summarize_text(entry.summary)
    translated_title = translate_text(title)
    translated_summary = translate_text(summary)
    return template.format(title=translated_title, summary=translated_summary, link=entry.link)
