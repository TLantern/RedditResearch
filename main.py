import argparse
from math import ceil
from reddit_scraper import RedditScraper
from summarizer import GPTSummarizer

def split_posts(posts, num_chunks=4):
    chunk_size = ceil(len(posts) / num_chunks)
    return [posts[i*chunk_size:(i+1)*chunk_size] for i in range(num_chunks)]


def main():
    parser = argparse.ArgumentParser(description="Scrape subreddit & summarize in multi-stage prompts")
    parser.add_argument("--subreddit", required=True, help="Subreddit name")
    parser.add_argument("--limit", type=int, default=100, help="Number of posts to fetch")
    parser.add_argument("--timeframe", choices=["day","week","month","year","all"], default="week")
    parser.add_argument("--output", default="summary.txt", help="Output file path")
    args = parser.parse_args()

    scraper = RedditScraper()
    posts = scraper.fetch_posts(args.subreddit, limit=args.limit, timeframe=args.timeframe)
    print(f"Fetched {len(posts)} posts from r/{args.subreddit}")

    # Split into 4 chunks
    post_chunks = split_posts(posts, num_chunks=4)

    summarizer = GPTSummarizer()

    # Stage 1: chunk-level summaries
    chunk_problems = []
    chunk_solutions = []
    for idx, chunk in enumerate(post_chunks, 1):
        text = "\n".join(f"Title: {p['title']}\n{p['text']}" for p in chunk)
        print(f"Summarizing problems chunk {idx}...")
        chunk_problems.append(summarizer.summarize_problems(text))
        print(f"Summarizing solutions chunk {idx}...")
        chunk_solutions.append(summarizer.summarize_solutions(text))

    # Stage 2: consolidate chunk summaries
    print("Consolidating problem summaries...")
    final_problems = summarizer.summarize_problems("\n".join(chunk_problems))
    print("Consolidating solution summaries...")
    final_solutions = summarizer.summarize_solutions("\n".join(chunk_solutions))

    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"Summary of r/{args.subreddit} top {args.limit} posts ({args.timeframe})\n\n")
        f.write("--- Common Problems ---\n")
        f.write(final_problems + "\n\n")
        f.write("--- User Solutions ---\n")
        f.write(final_solutions + "\n")

    print(f"Done! Problems & solutions written to {args.output}")

if __name__ == "__main__":
    main()