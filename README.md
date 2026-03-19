# Prakhar Gupta — YouTube Channel Analytics Dashboard

A professional analytics dashboard for The Prakhar Gupta Xperience podcast channel. Built using Python and YouTube Data API to fetch live data and present deep insights through an interactive dashboard.

---

## What This Project Does

Fetches all long-form videos (10+ minutes) from the channel, analyses performance data, and presents everything in a clean interactive dashboard — category breakdown, guest performance, growth trends, and strategic insights.

---

## Features

- 284 long videos analysed
- Category-wise performance breakdown
- Top 20 guests ranked by total views
- Year-over-year growth trends from 2020 to 2026
- Views, Likes and Comments for every video
- Search and filter by title, guest or category
- Strategic insights — what is working, red flags, opportunities

---

## Tech Stack

- Python 3 — data fetching and processing
- YouTube Data API v3 — live channel data
- HTML, CSS, JavaScript — dashboard frontend
- Chart.js — interactive charts

---

## Project Structure
```
├── index.html                   — Main dashboard
├── fetch_data.py                — Fetches raw data from YouTube API
├── youtube_deep_analysis_v2.py  — Processes data and builds dashboard
├── videos_raw.csv               — Raw video data
└── README.md                    — Project description
```

---

## How to Run

Step 1 — Open fetch_data.py and add your YouTube API Key and Channel ID

Step 2 — Run the fetch script
```
py fetch_data.py
```

Step 3 — Run the analysis script
```
py youtube_deep_analysis_v2.py
```

Step 4 — Open the generated HTML file in your browser

---

## Key Insights

- Comedy category drives 42.7% of all views from just 25 videos
- Guest videos get 6.2x more views than solo videos
- Best video duration is 60 to 90 minutes with 816K average views
- 2024 was the breakout year with 7.7x growth in average views per video
- Aarush Laila is the top guest with 20.4M total views
- Crime and Dark content averages 1.1M views but only 4 videos exist

---

## Notes

- Only videos of 10 minutes or longer are included
- All categories are manually verified for accuracy
- Data fetched in March 2026
- YouTube API has a daily quota of 10,000 units
