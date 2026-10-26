# Hockey Scoreboard Builder

Pick men's and women's college hockey games (NCAA.com data) and, optionally, all St. Cloud State Athletics games, then copy or download the resulting JSON.

Live site: `https://YOUR-USERNAME.github.io/YOUR-REPO/`

## Deploy on GitHub Pages
1. Push these files to the root of a repo's `main` branch.
2. In the repo, open Settings > Pages.
3. Under Build and deployment, set Source to "Deploy from a branch", Branch to `main`, folder `/ (root)`, then Save.
4. After a minute the site is live at the address above.

## Notes
- `index.html` is the whole app. There is no build step.
- Scores load in the visitor's browser from `ncaa-api.henrygd.me`, a free public API limited to 5 requests per second per IP.
- The St. Cloud State calendar is read from the Huskies site. If the browser blocks it, use "Load .ics" with a calendar file downloaded from scsuhuskies.com.
