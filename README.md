[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rhafarnulis/news-image-20-nov/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/rhafarnulis/news-image-20-nov/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — 20 November 2026

A newspaper front page summing up Friday 20 November 2026, drawn
entirely with Python and PIL — no photographs, no AI image generation.
Every headline, deck and illustration is drawn from shapes and text.

## The day's stories

- **Kyiv, Ukraine (lead).** Russia fired more than 110 missiles and
  400 drones at Ukraine overnight, killing at least eight people,
  hitting three bridges across the Dnipro and cutting power across
  Kyiv — hours after President Putin left the Shenzhen summit with
  Mr Trump and Mr Xi. Poland said three objects crossed into its
  airspace.
- **COP31, Antalya.** The final-day draft of the climate deal strips
  out every mention of phasing out fossil fuels and drops a $120bn
  adaptation-finance target, as talks run into overtime.
- **Markets.** Anthropic shares fell about a tenth on their second
  day of trading after the record listing, as the AI sell-off swept
  Asia: Tokyo's Nikkei fell 5.1% and Seoul's Kospi 5.2%.
- **Brussels.** Britain and the EU sealed a reset deal at their
  second summit since Brexit: food checks, linked carbon markets
  and a youth mobility scheme for 100,000 under-32s.
- **Odisha, India.** Cyclone Akvan came ashore near Gopalpur with
  winds gusting to 90 km/h, after more than 300,000 people were
  moved to shelters. No deaths were reported.
- **In brief.** A tanker caught fire in the Strait of Hormuz after
  a projectile strike near Oman; BepiColombo reached Mercury after
  an eight-year, six-billion-mile voyage.

Each story was checked against reporting from Reuters, CNN, the
Associated Press, the BBC/Guardian, the UK government, the India
Meteorological Department and UKMTO on 20 November 2026.

## How it is built

- `draw_frontpage.py` draws `entry.png` (1024×1024) with PIL and the
  DejaVu fonts. Run it again to reproduce the image byte for byte
  from the same script and fonts.
- `main.py` is the competition entry point: it copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), so two
  runs write identical bytes. Standard library only.

## License

MIT — see `LICENSE`.
