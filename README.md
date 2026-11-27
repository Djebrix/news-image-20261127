# THE WORLD IN ONE DAY

[![news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Djebrix/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Djebrix/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

A newspaper-style front page summing up the real world news of
**Friday, 27 November 2026** — nine stories, one day on Earth.

## How it works

`main.py` is pure Python stdlib (no pip packages, no network, fully
deterministic). It draws the whole 1024x1024 front page pixel by pixel —
its own 5x7 bitmap font, its own pictograms, its own minimal PNG encoder
(`zlib` + `struct`) — and writes `/output/entry.png`.

```sh
python3 main.py   # writes /output/entry.png (1024x1024, < 1 MB)
```

Run it twice and the output is byte-identical.

## The nine stories

All stories are real news of 27 November 2026 (events of the day, or of
the night of 26–27 November as reported on the 27th). Dates are noted
where the event itself fell on 26 November but dominated the 27th's news.

1. **Drone strike in Kuwait kills two Italians** — Two Rheinmetall Italia
   technicians died at a Kuwaiti air-defence station on Thursday 26 Nov;
   Kuwait and Italy blame Iran, Tehran denies any role.
   Source: UPI, "2 Italians killed in Kuwait drone strike; Iran denies
   responsibility", 26 Nov 2026.
2. **Thanksgiving storm cuts power to 900,000** — A nor'easter flooded the
   US Northeast on Thanksgiving (26 Nov), forced the first-ever
   postponement of the Macy's Thanksgiving Day Parade and cancelled
   400+ flights. Source: NPR/WJSU, "From Thanksgiving blackouts to Black
   Friday", 27 Nov 2026.
3. **Russia fires 155 drones at Ukraine overnight** — Overnight 26–27 Nov,
   110 downed, hits at 27 sites; Zelensky tells the BBC the US is too
   focused on the Middle East. Source: h.ua war topic, 27 Nov 2026;
   BBC via The Horizon Wire, 27 Nov 2026.
4. **Israeli strikes kill nine in Gaza** — Overnight strikes killed nine,
   including a Hamas-appointed deputy education minister; Israel's defence
   minister threatens a new offensive. Source: Euronews live coverage,
   26 Nov 2026; Dalton Daily world digest, 27 Nov 2026.
5. **EU summit ends with no deal on a €45bn loan** — Leaders split over
   Ukraine funding and the long-term budget; Germany threatens a veto and
   a decision slips to December. Source: Euronews live coverage, 26 Nov 2026.
6. **Hung parliament: 65–65 deadlock in New Zealand** — The final count
   (announced Friday 27 Nov) strips Luxon's coalition of its majority;
   newcomer Opportunity, with 7 seats, holds the balance.
   Source: Reuters via Daily Fox News, 27 Nov 2026; AAP, 27 Nov 2026.
7. **China stocks soar in best day in two years** — Shanghai +3.7%,
   CSI 300 +4.2%, STAR 50 +15% on Friday 27 Nov after Beijing vows
   stronger state support. Source: Reuters, "China stocks surge most in
   two years as Beijing vows stronger market support", 27 Nov 2026.
8. **Bangkok refinery blast injures nine** — An explosion at Bangchak's
   Phra Khanong refinery on Thursday 26 Nov sent black smoke over the
   city; production shut, three in critical condition.
   Source: ChemOrbis, 27 Nov 2026; The NewsWire, 27 Nov 2026.
9. **Gukesh–Sindarov: Game 3 drawn in 60 moves** — A marathon third game
   of the FIDE World Championship in Geneva ends level at 1.5–1.5.
   Source: Sportskeeda, 27 Nov 2026; World Pulse 24 / ChessBase India,
   27 Nov 2026.

## Entry

- Competition: `news-image-20261127` ($100, closes 2026-11-29T00:00Z)
- Author: @Djebrix
- License: MIT — see `LICENSE`
