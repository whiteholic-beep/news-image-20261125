# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/whiteholic-beep/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/whiteholic-beep/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

"THE WORLD ON ONE PAGE" — a newspaper front page summing up Wednesday 25 November 2026's world news in one image: Ukrainian drones hit two Russian refineries 800 km deep, Asian stocks rout as KOSPI falls 6%, Shenzhou-24 carries the first foreign astronaut to Tiangong, plus 32 more stories across seven regions, a pin map and a red DATE CHECK strip. 35 stories in all, every one dated Wednesday 25 November 2026.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies entry.png to the output directory as entry.png. No network, no randomness: the same bytes out every run.

The image itself is drawn by draw.py (Python 3 + Pillow, no network, no clock):

```sh
python3 draw.py
```

It regenerates entry.png deterministically — two runs produce identical bytes.

## Verification

`main.ts` refuses to emit a broken image: it errors out if `entry.png` is missing, empty, not a PNG, over the 1 MiB limit, or over 1024×1024 pixels, and after copying it checks the output byte for byte against the source, aborting on any mismatch. A successful run prints the output path, byte count, and digest. Checked locally:

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
# wrote out/entry.png (203381 bytes, sha256 34e391a2a3d23c7ea5366251d30008772cc61e4241007ac3483077f3dee446d6)
sha256sum out/entry.png entry.png   # identical digests
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=zx2vqcpc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
