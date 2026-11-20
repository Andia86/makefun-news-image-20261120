[![Bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/Andia86/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/Andia86/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The Day in World News — Friday 20 November 2026

An entry for the make.fun bounty
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
one image that sums up the world's news of Friday 20 November 2026.

## What the page shows

A one-page broadsheet front page, drawn programmatically:

- **11 illustrated story cards** (numbered 1–11), each with a small
  original flat drawing, a region tag, a serif headline and a
  one-line summary, plus a source line marked as checked on
  20 Nov 2026.
- **A world map** ("Where it happened") with numbered pins matching
  the cards and dots for further datelines.
- **29 further stories** (12–40) as a numbered list, so the page
  carries 40 stories from 6 regions in total.
- A footer stating that every story was reported on Friday
  20 November 2026 and naming the wires and papers used.

The day's lead stories: the World Court's genocide finding against
Myanmar, the first Trump–Xi–Putin trilateral talks at APEC, the
COP31 fossil-fuel fight, the Hormuz tanker war, and Anthropic's
record-breaking IPO.

## How it is built

- `build_page.py` draws the page with Pillow from the story data
  embedded in it and writes `entry.png` (1024×1024). It is fully
  deterministic — no clock, no randomness, no network — so two runs
  produce byte-identical output.
- `main.py` is the competition entrypoint: it verifies the bundled
  `entry.png` (PNG signature, exact bytes) and delivers it to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, or `/output/entry.png` when the
  variable is unset.
- `NEWS_SOURCES.md` lists the source of every story on the page.

## Run it

```sh
python3 build_page.py          # redraws entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
