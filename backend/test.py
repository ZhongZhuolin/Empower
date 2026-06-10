
from main import fetch_news, format_articles, ask_claude, ask_claude_sum


articles = fetch_news("Palantir")

print(format_articles(articles))

