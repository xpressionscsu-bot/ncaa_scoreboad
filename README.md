# Hockey Scoreboard Builder

Pick men's and women's college hockey games (NCAA.com data) and, optionally, all St. Cloud State Athletics games, then copy or download the JSON.

## How data gets to the page
The page first asks the NCAA feed directly. If the browser can't reach it, it falls back to files in `data/`, which a GitHub Action refreshes every 15 minutes (yesterday through the next 14 days, plus the SCSU calendar).

## Setup
1. Push everything here to `main`, including the hidden `.github` folder.
2. Settings > Actions > General > Workflow permissions: choose "Read and write permissions" and save.
3. Actions tab > "Update scoreboard data" > Run workflow. Wait for the green check.
4. Settings > Pages: Deploy from a branch, `main`, `/ (root)`.

Open the Action's log to see which sources worked (lines starting "ok" or "fail").
