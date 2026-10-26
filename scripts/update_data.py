"""Saves NCAA hockey scoreboards and the SCSU calendar into data/ so the page can read them from its own site."""
import json, os, time, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
SPORTS = {"men": "icehockey-men", "women": "icehockey-women"}
SOURCES = [
    "https://data.ncaa.com/casablanca/scoreboard/{sport}/d1/{y}/{m}/{d}/scoreboard.json",
    "https://ncaa-api.henrygd.me/scoreboard/{sport}/d1/{y}/{m}/{d}/all-conf",
]
ICS_URLS = [
    "https://scsuhuskies.com/calendar.ashx/calendar.ics",
    "https://scsuhuskies.com/calendar.ashx/calendar.ics?sport_id=0",
]
HEADERS = {"User-Agent": "Mozilla/5.0 (hockey-scoreboard updater)"}

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def fetch_day(sport, day):
    y, m, d = day.split("-")
    for tpl in SOURCES:
        url = tpl.format(sport=sport, y=y, m=m, d=d)
        try:
            data = json.loads(get(url))
            games = [g.get("game", g) for g in data.get("games", [])]
            print("ok  ", url, len(games))
            return games
        except Exception as e:
            print("fail", url, e)
    return None

def main():
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "ncaa.json")
    try:
        old = json.load(open(path))
    except Exception:
        old = {"days": {}}
    today = datetime.now(ZoneInfo("America/Chicago")).date()
    days = {}
    for i in range(-1, 15):
        day = (today + timedelta(days=i)).isoformat()
        entry = {}
        for key, sport in SPORTS.items():
            games = fetch_day(sport, day)
            if games is None:
                games = old.get("days", {}).get(day, {}).get(key)  # keep the last good copy
            if games is not None:
                entry[key] = games
            time.sleep(0.4)
        if entry:
            days[day] = entry
    out = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "days": days}
    # only rewrite when games changed, so the repo history stays quiet
    if json.dumps(out["days"], sort_keys=True) != json.dumps(old.get("days"), sort_keys=True):
        json.dump(out, open(path, "w"), separators=(",", ":"))
        print("wrote ncaa.json")

    for url in ICS_URLS:
        try:
            body = get(url)
            if b"BEGIN:VEVENT" in body:
                open(os.path.join(DATA, "scsu.ics"), "wb").write(body)
                print("ok  ", url, "saved scsu.ics")
                break
            print("no events", url)
        except Exception as e:
            print("fail", url, e)

if __name__ == "__main__":
    main()
