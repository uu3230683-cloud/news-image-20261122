# The World in One Day — Sunday 22 November 2026

One image summing up the world's news of Sunday 22 November 2026, drawn
as a newspaper front page: a masthead naming the day, six verified stories
with a pictogram, headline and summary each, and a footer ticker of smaller
stories.

## Stories in the image

1. **COP31 collapses** — UN climate talks in Antalya, Türkiye end after two
   days of overtime with no agreement, split over fossil fuels.
2. **ICJ: Myanmar committed genocide** — the International Court of Justice
   rules against Myanmar over its Rohingya minority.
3. **Candy factory fire, Indonesia** — a blaze at a confectionery factory in
   Banten kills three workers; dozens are still missing.
4. **'El Chapo Isidro' captured** — Mexican troops seize cartel boss Fausto
   Isidro Meza Flores in a Sinaloa raid backed by US intelligence.
5. **Missile hits Kyiv apartment block** — a Russian strike kills three and
   buries others as winter closes in on Ukraine.
6. **Tankers hit near Hormuz** — Iran says two supertankers struck mines east
   of the Strait of Hormuz; Trump says he may strike Iran again after the
   new year.
7. Ticker: Delta outage delays 1,600+ flights; Ukraine drones sink a Russian
   warship off Libya; London's Christmas tree felled in Norway.

All stories were verified against same-day reporting (AP, KPFA, and the
22 November evening briefings) before the image was drawn.

## Files

- `entry.png` — the image, 1024x1024 PNG (the deliverable).
- `main.py` — the entrypoint: standard library only, copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Deterministic: every
  run writes identical bytes.
- `draw.py` — the build-time generator (Pillow) that drew `entry.png` from
  scratch in this session. Not run by the grader.

## Verify locally

```sh
python3 draw.py            # regenerate entry.png
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png   # identical
```

## License

MIT — see `LICENSE`.
