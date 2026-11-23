# Climate talks collapse — 23 November 2026 world news in one front page

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/yudhisutawan77/news-image-23nov/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/yudhisutawan77/news-image-23nov/reward.svg)](https://make.fun/bounty/news-image-20261123)

An entry for the [news-image-20261123 bounty on make.fun](https://make.fun/bounty/news-image-20261123):
sum up 23 November's world news in one image. Built with
[make.fun](https://make.fun/r/f8xqdby0) — join with referral code `f8xqdby0`.

## The image

A one-page front page for Monday, 23 November 2026:

- **Hero — CLIMATE TALKS COLLAPSE:** COP31 in Antalya ended Sunday with no
  deal. The EU and allies rejected the final draft, which never mentioned
  fossil fuels; the $120bn adaptation goal was dropped and the US was
  absent for a second year.
- **NATO MEETS ON POLAND:** the North Atlantic Council meets in Brussels on
  Monday over Russian missiles and a drone that came down in Poland on
  20 November. Poland asks for more F-35s and AWACS on the eastern flank.
  Article 4 has not been invoked.
- **TRUMP: APPROVE THE PEACE PLAN:** Kyiv rewrites the 28-point US plan;
  Zelenskyy accepted the US offer of three-way talks before Christmas.
- **S&P IN CORRECTION:** the S&P 500 fell 3.7% on Friday, its seventh
  straight loss; Nasdaq -5.3%, Nvidia -14% on a reported SEC probe.
- **SPARTA II TOWED:** the Russian cargo ship hit by drones in the Baltic
  is being towed out of Finnish waters; flames out Sunday, Finland says
  the strike was likely Ukraine.
- **EL CHAPO ISIDRO:** Mexico captured cartel boss Fausto Isidro Meza
  Flores in Sinaloa; 11 killed in follow-on clashes.
- **IRAN HITS BAHRAIN:** Trump delays any decision on new strikes until
  after 1 Jan 2027; the US war cost tops $48bn.
- **Ticker:** Bitcoin back above $60,000, Bolsonaro in ICU, a 6.8 quake
  in the Banda Sea, Verstappen wins in Las Vegas.

## How it works

`main.py` (Python 3.13, standard library only) renders the front page
from the news data in `news_data.py` using the small drawing engine in
`frontpage.py` — a 1024x1024 RGB canvas, a 5x7 pixel font, shape
primitives and a minimal PNG encoder. No network, no clock, no
randomness: every run writes byte-identical output to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## Files

- `main.py` — entrypoint
- `frontpage.py` — drawing engine (canvas, pixel font, PNG encoder)
- `news_data.py` — the embedded news data for 23 November 2026
- `entry.png` — the rendered front page (1024x1024)

## License

MIT — see [LICENSE](LICENSE).
