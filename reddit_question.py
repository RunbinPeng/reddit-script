import praw
import csv
from datetime import datetime

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="market-research:geo-question-miner:v1.0 (by /u/YOUR_USERNAME)"
)

SUBREDDITS = ["investing", "stocks", "Daytrading", "personalfinance", "singaporefi"]
QUESTION_WORDS = ["what", "how", "which", "best", "why", "where", "is ", "are ", "can "]

def is_question(title):
    t = title.lower()
    return any(t.startswith(w) for w in QUESTION_WORDS) or title.endswith("?")

def mine_questions(subreddit_name, limit=100):
    results = []
    sub = reddit.subreddit(subreddit_name)
    for post in sub.new(limit=limit):
        if is_question(post.title):
            results.append({
                "subreddit": subreddit_name,
                "title": post.title,
                "score": post.score,
                "created": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d"),
                "url": post.url
            })
    return results

def main():
    all_questions = []
    for sub in SUBREDDITS:
        print(f"Mining r/{sub}...")
        all_questions.extend(mine_questions(sub))
    with open("questions_output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["subreddit","title","score","created","url"])
        writer.writeheader()
        writer.writerows(all_questions)
    print(f"Done. {len(all_questions)} questions saved.")

if __name__ == "__main__":
    main()
