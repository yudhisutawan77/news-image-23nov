"""News data for Monday 23 November 2026 — embedded, no network.

Sources (checked the morning of 23 Nov 2026, WITA):
- COP31 collapse: Reuters via Sowetan / sumi.news / IPS (22 Nov); UN SG
  Guterres "deeply disappointed"; EU rejected the final draft.
- NATO Council: PAP via eutoday/europesays, 21-22 Nov — extraordinary
  North Atlantic Council session in Brussels, Monday 23 Nov; Poland
  represented by Deputy Defence Minister Pawel Zalewski; Poland has
  NOT formally invoked Article 4. No outcome claimed: the session is
  Monday midday Brussels, after this image is built.
- Peace plan: AP / Reuters, 21-22 Nov; Zelenskyy accepted the US offer
  of further trilateral talks before Christmas (Washington Post, 22 Nov).
- Markets: Reuters, 22 Nov — S&P 500 -3.7% Friday to 6,910.39, 7th
  straight loss, >10% below the 6 Oct record; Nasdaq -5.28%;
  Nvidia -14% on a reported SEC accounting probe.
- Sparta II: Reuters, 22 Nov — visible flames out Sunday, Russian
  rescue vessel began towing her out of Finnish waters; smoke still
  rising; Finland says the drone strike was likely Ukraine; 16 crew
  evacuated, one slightly injured.
- El Chapo Isidro: Al Jazeera / BBC / Guardian, 22 Nov — Mexican
  special forces captured Fausto Isidro Meza Flores in Sinaloa;
  11 killed in follow-on violence.
- Iran: Reuters, 21-22 Nov — Iran struck civilian industry in Bahrain;
  Trump told Reuters he delays any decision on new strikes until
  after 1 Jan 2027; US war cost vs Iran tops $48.3bn since February.
- Ticker: Bitcoin reclaimed $60,000 over the weekend (low ~$55,100 Sat,
  ~$61,200 Mon 00:10 UTC); Bolsonaro in ICU; M6.8 Banda Sea quake
  (GFZ); Verstappen won in Las Vegas.

Rules honoured: no "ARTICLE 4 INVOKED", no claimed NATO outcome, no
claimed COP31 deal, Zelenskyy did not "approve" the plan, Sparta II
is "likely Ukraine" not certain, Bitcoin shows both the fall and the
rebound. Only 23 November 2026 appears as a date.
"""

DATA = {
    "masthead": {
        "title": "THE WORLD TODAY",
        "date": "MONDAY, 23 NOVEMBER 2026",
        "kicker": "ANTALYA \u2022 BRUSSELS \u2022 KYIV \u2022 WASHINGTON \u2022 SINALOA",
    },
    "hero": {
        "label": "THE TOP STORY",
        "line1": "CLIMATE TALKS",
        "line2": "COLLAPSE",
        "subs": [
            "EU REJECTS THE FINAL DRAFT",
            "NO MENTION OF FOSSIL FUELS",
            "$120BN ADAPTATION GOAL DROPPED",
            "US ABSENT FOR A SECOND YEAR",
        ],
        "strip": "COP31 \u2022 ANTALYA \u2022 NO DEAL",
    },
    "row_a": [
        {
            "kicker": "BRUSSELS \u2022 MONDAY",
            "accent": (31, 78, 121),
            "head": ["NATO MEETS", "ON POLAND"],
            "subs": [
                "POLAND ASKS FOR MORE F-35S",
                "AND AWACS ON EASTERN FLANK",
                "ARTICLE 4 NOT INVOKED",
            ],
        },
        {
            "kicker": "KYIV \u2022 WASHINGTON",
            "accent": (163, 51, 39),
            "head": ["TRUMP: APPROVE", "THE PEACE PLAN"],
            "subs": [
                "KYIV REWRITES THE 28-POINT PLAN",
                "ZELENSKYY ACCEPTS 3-WAY TALKS",
                "BEFORE CHRISTMAS",
            ],
        },
    ],
    "row_b": [
        {
            "kicker": "WALL STREET \u2022 FRIDAY",
            "accent": (140, 40, 40),
            "head": "S&P IN CORRECTION",
            "subs": [
                "S&P -3.7% FRIDAY",
                "NASDAQ -5.3% \u2022 NVIDIA -14%",
            ],
            "graphic": "chart",
        },
        {
            "kicker": "BALTIC SEA \u2022 SATURDAY",
            "accent": (46, 92, 124),
            "head": "SPARTA II TOWED",
            "subs": [
                "FLAMES OUT SUNDAY",
                "FINLAND: LIKELY UKRAINE",
            ],
            "graphic": "ship",
        },
        {
            "kicker": "SINALOA \u2022 SATURDAY",
            "accent": (46, 110, 60),
            "head": "EL CHAPO ISIDRO",
            "subs": [
                "CARTEL BOSS SEIZED",
                "11 KILLED IN CLASHES",
            ],
            "graphic": "star",
        },
    ],
    "band": {
        "line1": "IRAN HITS BAHRAIN",
        "line2": "TRUMP DELAYS NEW STRIKES TO JAN 1 \u2022 US WAR COST TOPS $48BN",
    },
    "ticker": [
        "BITCOIN BACK ABOVE $60,000 \u2022 BOLSONARO IN ICU",
        "6.8 QUAKE STRIKES BANDA SEA \u2022 VERSTAPPEN WINS LAS VEGAS",
    ],
}
