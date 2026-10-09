# Roadmap

## Projektstruktur

Filer markerade som *planerade* skapas när de behövs.

```text
.
├── README.md           # Projektöversikt
├── ROADMAP.md          # Plan och filstruktur
├── .gitignore          # Lokala filer som Git ignorerar
├── __init__.py         # Befintlig paketfil
├── constants.py        # Fysikaliska konstanter
├── models.py           # Datamodeller och parametrar
├── load_cases.py       # Acceleration, bromsning och kurvtagning
├── forces.py           # Krafter och lagerreaktioner (planerad)
├── shaft.py            # Snittstorheter längs axeln (planerad)
├── stresses.py         # Spänningar och koncentrationer (planerad)
├── dimensioning.py     # Dimensionering och säkerhetsfaktorer (planerad)
├── plotting.py         # Diagram (planerad)
└── main.py             # Körning av hela analysen (planerad)
```

## Arbetsplan

- [ ] **1. Yttre laster:** färdigställ och verifiera hjulkrafter, driv- och bromsmoment samt lagerreaktioner för alla tre lastfall. Bestäm även högsta tillåtna kurvhastighet utan hjullyft.
- [ ] **2. Snittstorheter (I):** beräkna normal- och tvärkrafter samt böj- och vridmoment längs bakaxeln. Beakta böjning i två plan vid kurvtagning.
- [ ] **3. Nominella spänningar (II):** beräkna normal- och skjuvspänningar för en antagen diameter och visa variationen längs axeln.
- [ ] **4. Spänningskoncentrationer (III):** analysera dimensionsövergångar för kritiskt lastfall och kontrollera lokal plasticering.
- [ ] **5. Dimensionering (IV–V):** bestäm erforderlig diameter med säkerhet mot plasticering och utmattning (roterande böjning).
- [ ] **6. Redovisning:** skapa diagram med enheter, jämför lastfall och sammanställ resultaten i teknisk rapport.

## Milstolpar enligt uppgiften

- **Vecka 41:** yttre krafter och disposition för rapport och program.
- **Vecka 49:** snittstorheter, spänningar, spänningskoncentrationer och diameter.
- **12 december 2026:** slutrapport enligt uppgiftens tidplan.

> Beräkningsmodellen ska vara parameterbaserad. Numeriska exempel införs först vid dimensioneringen, enligt uppgiftsbeskrivningen. Kryssa av punkter först när de är genomförda och kontrollerade.
