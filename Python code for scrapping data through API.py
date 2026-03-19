import urllib.request
import json
import re
import csv

API_KEY    = "AIzaSyCNMvRjqd7FdkrsNZFIDng8mXJ4MyayDIg"
CHANNEL_ID = "UCHOKvQW2N4kLVhKYn2bvF7A"

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def is_long(dur):
    h = int((re.search(r'(\d+)H', dur) or type('',(),{'group':lambda s,x:0})()).group(1) or 0)
    m = int((re.search(r'(\d+)M', dur) or type('',(),{'group':lambda s,x:0})()).group(1) or 0)
    s = int((re.search(r'(\d+)S', dur) or type('',(),{'group':lambda s,x:0})()).group(1) or 0)
    return (h*3600 + m*60 + s) >= 600

def dur_label(dur):
    h = int((re.search(r'(\d+)H', dur) or type('',(),{'group':lambda s,x:0})()).group(1) or 0)
    m = int((re.search(r'(\d+)M', dur) or type('',(),{'group':lambda s,x:0})()).group(1) or 0)
    s = int((re.search(r'(\d+)S', dur) or type('',(),{'group':lambda s,x:0})()).group(1) or 0)
    return f"{h}h {m:02d}m" if h else f"{m}m {s:02d}s"

# ── Step 1: Channel info ───────────────────────────────────────────────────────
print("Step 1/3 — Fetching channel info...")
ch = api(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={CHANNEL_ID}&key={API_KEY}")["items"][0]
playlist_id = ch["contentDetails"]["relatedPlaylists"]["uploads"]
print(f"  Channel : {ch['snippet']['title']}")
print(f"  Subs    : {ch['statistics'].get('subscriberCount','?')}")

# ── Step 2: All video IDs ──────────────────────────────────────────────────────
print("\nStep 2/3 — Fetching all video IDs...")
video_ids, page_token, page = [], "", 0
while True:
    page += 1
    url = (f"https://www.googleapis.com/youtube/v3/playlistItems"
           f"?part=snippet&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
           + (f"&pageToken={page_token}" if page_token else ""))
    data = api(url)
    for item in data["items"]:
        video_ids.append(item["snippet"]["resourceId"]["videoId"])
    page_token = data.get("nextPageToken", "")
    print(f"  Page {page}: {len(video_ids)} IDs total")
    if not page_token:
        break

# ── Step 3: Full video data ────────────────────────────────────────────────────
print(f"\nStep 3/3 — Fetching full data for {len(video_ids)} videos...")
videos  = []
chunks  = [video_ids[i:i+50] for i in range(0, len(video_ids), 50)]

for i, chunk in enumerate(chunks):
    url = (f"https://www.googleapis.com/youtube/v3/videos"
           f"?part=statistics,snippet,contentDetails&id={','.join(chunk)}&key={API_KEY}")
    data = api(url)
    for v in data["items"]:
        dur = v["contentDetails"].get("duration", "PT0S")
        if not is_long(dur):
            continue
        videos.append({
            "id":          v["id"],
            "title":       v["snippet"]["title"],
            "date":        v["snippet"]["publishedAt"][:10],
            "duration":    dur_label(dur),
            "views":       int(v["statistics"].get("viewCount",   0)),
            "likes":       int(v["statistics"].get("likeCount",   0)),
            "comments":    int(v["statistics"].get("commentCount",0)),
            "description": v["snippet"].get("description", "")[:1000],  # first 1000 chars
            "url":         f"https://youtube.com/watch?v={v['id']}",
            "category":    ""   # <- tum baad mein Claude se fill karwana
        })
    print(f"  Batch {i+1}/{len(chunks)} done — {len(videos)} long videos so far")

videos.sort(key=lambda x: x["views"], reverse=True)

# ── Save JSON ──────────────────────────────────────────────────────────────────
with open("videos_raw.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)
print(f"\n✓ Saved: videos_raw.json  ({len(videos)} videos)")

# ── Save CSV ───────────────────────────────────────────────────────────────────
fields = ["id","title","date","duration","views","likes","comments","url","description","category"]
with open("videos_raw.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(videos)
print(f"✓ Saved: videos_raw.csv   ({len(videos)} videos)")

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total long videos : {len(videos)}
  Total views       : {sum(v['views'] for v in videos):,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ab yeh 2 files Claude ko do:
  1. videos_raw.json
  2. videos_raw.csv
Woh categories add karke final dashboard denge!
""")


