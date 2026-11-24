"""Story data for Monday 23 November 2026 (all from the verified story bank)."""

REGIONS = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "AFRICA", "OCEANIA", "MIDDLE EAST", "WORLD"]
RCOL = {
    "EUROPE": (30, 84, 150),
    "AMERICAS": (122, 48, 150),
    "ASIA-PACIFIC": (0, 118, 122),
    "AFRICA": (38, 118, 56),
    "OCEANIA": (190, 132, 12),
    "MIDDLE EAST": (176, 80, 26),
    "WORLD": (92, 92, 100),
}
RCODE = {"EUROPE": "EU", "AMERICAS": "AM", "ASIA-PACIFIC": "AP", "AFRICA": "AF",
         "OCEANIA": "OC", "MIDDLE EAST": "ME", "WORLD": "WD"}

CERT = {
    "CONFIRMED": ("CNF", (28, 118, 58)),
    "OFFICIAL": ("OFF", (108, 50, 140)),
    "REPORTED": ("REP", (160, 100, 14)),
    "CLAIM": ("CLM", (170, 30, 30)),
    "FORECAST": ("FCT", (52, 86, 140)),
}

# n, region, kicker, cert, headline, deck, source
MAINS = [
    (1, "EUROPE", "KYIV REGION, UKRAINE", "CONFIRMED",
     "Kyiv-region strikes kill 14; a block falls in Dymer",
     "Overnight Sun to Mon: 11 dead in Dymer as a five-storey block partly collapsed (a boy, 7, and a "
     "woman, 79, pulled out alive); 3 dead in a Vyshneve supermarket; 11 still missing.",
     "AFP via Euronews, 06:13 UTC; Reuters"),
    (2, "AMERICAS", "NEW YORK, WALL STREET", "CONFIRMED",
     "Huang back at Nvidia; Nasdaq jumps 6.51%",
     "Board reinstated Jensen Huang unanimously, 11 days after he quit; NVDA +31% to ~$165. S&P 500 "
     "+4.73%, Dow +3.01%: best day since April 2025, undoing Friday's crash.",
     "Reuters, Mon 23 Nov close"),
    (3, "EUROPE", "BRUSSELS, EUROPEAN UNION", "OFFICIAL",
     "EU's 22nd package takes 60 banks off SWIFT",
     "Commission proposal: 70+ more shadow-fleet ships, Russia-insured tankers barred, first ban on "
     "electricity services, Russian flag out of EU sport. Needs all 27 states to agree.",
     "European Commission; Reuters"),
]

# n, region, kicker, cert, headline, deck, source
CARDS = [
    (4, "WORLD", "ZURICH, FOOTBALL", "CONFIRMED",
     "2031 Women's World Cup: four hosts, 48 teams",
     "USA, Mexico, Costa Rica, Jamaica by acclamation; UK hosts 2035.", "Reuters, FIFA Congress"),
    (5, "EUROPE", "BRENTFORD, PREMIER LG", "CONFIRMED",
     "Brentford 4-0 Everton, the only Monday match",
     "Lewis-Potter 23', 25'; Janelt 67'; Carvalho 90'. Tarkowski red 40'.", "Sky Sports"),
    (6, "MIDDLE EAST", "GAZA, JABALIA", "CONFIRMED",
     "Israeli strike kills UNRWA worker in Gaza",
     "Adel Al-Helo hit near a well; 4 Palestinians killed on Monday.", "Reuters; UNRWA"),
    (7, "WORLD", "COMMODITIES", "CONFIRMED",
     "Gold +2.7% off 14-month low; oil falls 4%",
     "Gold ~$3,635; WTI ~$81.29; Brent under $92.", "Market wires"),
    (8, "AMERICAS", "WASHINGTON, TECH M&A", "OFFICIAL",
     "CrowdStrike buys Zscaler for $43.9bn",
     "All-stock, $260.41 a share, 34% premium; closes H2 FY2028.", "Joint release; Reuters"),
    (9, "EUROPE", "KOUROU, SPACE", "OFFICIAL",
     "Ariane 6 scrubs Amazon's 36-satellite launch",
     "Ground-systems fault; rocket safe; next try Tue 24 Nov at earliest.", "Arianespace"),
    (10, "ASIA-PACIFIC", "TAIWAN STRAIT", "OFFICIAL",
     "5 Chinese sorties cross Taiwan's median line",
     "6 sorties and 12 ships in 24 hours to 06:00 Monday.", "Taiwan MND"),
    (11, "OCEANIA", "VANUATU, QUAKE", "CONFIRMED",
     "M6.5 quake hits Vanuatu, 598 km deep",
     "02:40 UTC; no damage, GDACS green alert.", "USGS; GDACS"),
    (12, "AFRICA", "LUSAKA, ZAMBIA", "CONFIRMED",
     "Zambia charges opposition leader with treason",
     "Mundubile and 12+ others over an alleged Apr-Aug coup plot.", "Reuters, 12:27 UTC"),
    (13, "EUROPE", "MADRID, ELECTION POLLS", "FORECAST",
     "Spain's right set for majority, final polls say",
     "PP 127-136, Vox 51-61 seats; 176 of 350 needed.", "Reuters; 40dB/El Pais"),
    (14, "AMERICAS", "NEW YORK, FED", "CONFIRMED",
     "Fed's Williams keeps Dec hike alive; 96% priced",
     "Inflation seen 3.5% in 2026, back to 2% only in 2028.", "Reuters; CME FedWatch"),
    (15, "EUROPE", "POLAND, NATO", "CONFIRMED",
     "NATO sends AWACS to Poland after missiles",
     "Reply to 3 Russian Kh-101s that landed there Fri 20 Nov.", "Reuters"),
]

# region, text, source, cert  (numbered 16..39 in this order = order of consequence)
ALSO = [
    ("EUROPE", "Zelenskiy: intel shows Russia planning new strikes", "Reuters", "OFFICIAL"),
    ("EUROPE", "Moscow: Estonia acts 'on verge of open war'", "Reuters", "OFFICIAL"),
    ("EUROPE", "EU-US split on peace-talk order goes public", "Euronews", "CONFIRMED"),
    ("MIDDLE EAST", "US sanctions Iran shadow banks; ~$15bn flows", "US Treasury", "OFFICIAL"),
    ("AFRICA", "64 reported killed in Niger-state attacks, Nigeria", "Reuters", "REPORTED"),
    ("WORLD", "WFP: wars may cost $727m more, 7.3m at risk", "Reuters", "OFFICIAL"),
    ("WORLD", "COP31 fallout: Guterres 'deeply disappointed'", "CNBC Africa", "CONFIRMED"),
    ("AMERICAS", "Trump hush-money appeal revived by appeals court", "AP", "REPORTED"),
    ("AFRICA", "CAS to rule Tuesday on Senegal's AFCON title", "Reuters", "CONFIRMED"),
    ("ASIA-PACIFIC", "KOSPI -3.31% despite stabilisation-fund pledge", "Market data", "CONFIRMED"),
    ("AMERICAS", "Amazon buys Decart AI tech, reportedly ~$7.5bn", "Reuters", "REPORTED"),
    ("EUROPE", "DAX +2.32%, FTSE +1.44% as STOXX ends slide", "Reuters", "CONFIRMED"),
    ("ASIA-PACIFIC", "Taiex +2.35% as Taipei widens short-sale curbs", "Informist", "CONFIRMED"),
    ("WORLD", "Bitcoin back above $60,000 after $55,130 low", "Market data", "REPORTED"),
    ("EUROPE", "NHS starts 700,000-woman AI breast-scan trial", "NIHR", "OFFICIAL"),
    ("AFRICA", "Kenya and DR Congo restore ambassadors", "OkayAfrica", "REPORTED"),
    ("AFRICA", "9 energy exporters made $21.6bn in Iran war", "CREA", "REPORTED"),
    ("AMERICAS", "MNF preview: Bengals at Commanders, 20:15 ET", "Reuters", "FORECAST"),
    ("EUROPE", "UCL Matchday 5 preview: City-Napoli, Arsenal-Dortmund", "UEFA", "FORECAST"),
    ("ASIA-PACIFIC", "Z.ai ships GLM-5.4, a 750B 'loop transformer'", "SiliconNoon", "CLAIM"),
    ("ASIA-PACIFIC", "China's exchanges unveil share-support measures", "Informist", "REPORTED"),
    ("ASIA-PACIFIC", "Hang Seng -0.12%, Shanghai +0.15%; Tokyo shut", "Market data", "CONFIRMED"),
    ("OCEANIA", "England's Will Jacks out of Australia tour, hand", "AFP", "CONFIRMED"),
    ("OCEANIA", "ASX 200 slips for an 8th straight session", "Market data", "CONFIRMED"),
]

STATS = [
    ("14", "killed in Kyiv-region overnight strikes", "AFP"),
    ("+6.51%", "Nasdaq's jump, best since Apr 2025", "Reuters"),
    ("60", "Russian banks to leave SWIFT", "EU Commission"),
    ("48", "teams at the 2031 Women's World Cup", "FIFA"),
    ("M6.5", "Vanuatu quake, 598 km deep", "USGS"),
    ("$43.9bn", "CrowdStrike's Zscaler deal", "Reuters"),
]

TIMELINE = [
    ("02:40", "Vanuatu M6.5"),
    ("06:13", "Kyiv toll: 14"),
    ("11:00", "Zscaler deal"),
    ("12:27", "Zambia treason"),
    ("15:19", "FIFA 2031 vote"),
    ("17:12", "EU-US split"),
    ("20:00", "Brentford kick-off"),
    ("21:00", "Wall St closes"),
]

DATE_LEFT = [
    "COP31 collapse (Sun 22 Nov; Monday is the fallout)",
    "Russian missiles land in Poland (Fri 20 Nov; Monday is NATO's reply)",
    "Friday's crash, Nasdaq -5.28% (Fri 20 Nov; Monday is the rally)",
    "F1 Las Vegas GP (Sat 21 Nov local) and Wembanyama's 50 (Sat 21 Nov)",
    "Liverpool 4-0 Man United, Cowboys 51-30 (Sun 22 Nov)",
]
DATE_MID = [
    "Peru M6.8 quake (Fri 20 Nov) is not Monday's Vanuatu M6.5",
    "Sparta II hit by drones (Sat 21); corvette sunk off Benghazi (Sun 22)",
    "Hunger Games $225m opening (weekend 20-22 Nov)",
    "Ariane's rival: Vulcan loses 40 Leo satellites (Sun 15 Nov)",
    "Commanders 38-33 Bengals (Mon 23 Sep 2024, wrong year)",
]
DATE_NOTYET = [
    "CAS Senegal ruling (Tue 24 Nov)",
    "Bengals-Commanders result (kick-off 20:15 ET)",
    "Ariane retry (Tue 24 Nov at earliest)",
    "Taiwan votes Sat 28 Nov; Spain votes Sun 29 Nov",
]
