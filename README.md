# README.md

## Overview
This tool:
1. Scrapes top posts from a given subreddit.
2. Preprocesses & chunks their text.
3. Calls OpenAI’s GPT‑4o to summarize common questions/pain points.

## Setup
1. Copy `.env.example` to `.env` and fill in your keys.
2. `pip install -r requirements.txt`
3. `python main.py --subreddit gym --limit 100 --output summary.txt`

## Usage
python main.py
--subreddit ENTREPRENEUR
--limit 100
--timeframe week
--output report.txt