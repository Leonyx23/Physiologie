THEMA = dict(
    id='haemostase', titel='Blutgerinnung: primäre und sekundäre Hämostase', bereich='Blut und Immunsystem',
    kurz='Thrombozyten, vaskuläre und thrombozytäre Blutstillung, von Willebrand, Kaskadenmodell und zellbasiertes Modell',
    lern=[
        dict(h='Die Hauptakteure', li=[
            '**Thrombozyten:** 1–3 µm, kernlos, 150.000–300.000/µl, leben 8–10 Tage, aus Megakaryozyten im Knochenmark',
            '**Gefäßwand:** Intima (Endothel + Bindegewebe), Media (glatte Muskulatur; Aorta ca. 50 Schichten mit elastischem Gewebe), Adventitia (Bindegewebe mit Vasa und Nervi vasorum)',
            'Im Blut fließen große Zellen in der Mitte, **Thrombozyten am Rand** (laminare Strömung, Scherkräfte) – immer in Tuchfühlung mit dem Endothel',
        ], q=[('GE', '2–3')]),
        dict(h='Übersicht: Ein Schauspiel in drei Akten', tb=[
            ['Akt', 'Was passiert', 'Ergebnis'],
            ['1. Primäre Hämostase', 'vaskuläre Blutstillung + Thrombozytenadhäsion, -aktivierung, -aggregation', '**weißer Thrombus** (instabil)'],
            ['2. Sekundäre Hämostase', 'plasmatische Gerinnung: Fibrinogen → Fibrin, Quervernetzung', '**roter Thrombus** (Erythrozyten im Fibrinnetz)'],
            ['3. Fibrinolyse', 'Plasmin spaltet das Fibrin, wenn das Endothel geheilt ist', 'Thrombus löst sich (D-Dimere)'],
        ], q=[('GE', '1, 17')]),
        dict(h='Primäre Hämostase', fl=dict(s=[
            ['Vaskuläre Blutstillung', 'glatte Muskeln ziehen sich innerhalb von Sekunden zusammen (ca. 60 s), verstärkt durch Serotonin und Thromboxan A₂'],
            ['Adhäsion', 'vWF bindet am freiliegenden Kollagen (Typ I, IV); Thrombozyten binden mit dem **vWF-Rezeptor (GP Ib)** und dem **Kollagenrezeptor (GP Ia/IIa)**'],
            ['Aktivierung', 'Formänderung mit Fortsätzen; Freisetzung von **ADP, Serotonin, Thromboxan A₂** → weitere Thrombozyten werden aktiviert'],
            ['Aggregation', '**Fibrinogen** bindet an den Fibrinogenrezeptor (**GP IIb/IIIa**) und verbindet die Thrombozyten → weißer Thrombus']]),
             li=['Der **vWF** stammt aus dem Endothel und trägt im Blut den Faktor VIII',
                 'Das Enzym **ADAMTS13** (v. a. aus der Leber) schneidet die langen vWF-Fäden klein. Fehlt es (meist durch Antikörper) → Thrombozyten verklumpen auch ohne Verletzung: **TTP** (thrombotisch-thrombozytopenische Purpura)'],
             q=[('GE', '3–6')]),
        dict(h='Störungen der primären Hämostase', tb=[
            ['Störung', 'Ursache', 'Zeichen'],
            ['**Von-Willebrand-Jürgens-Syndrom** – häufigste angeborene Gerinnungsstörung', 'vWF fehlt oder funktioniert nicht', 'Nasenbluten, starke Monatsblutung, blaue Flecken, Nachblutungen, Hämarthros'],
            ['Thrombozytopenie (unter 150.000/µl)', 'meist Antikörper: spontan (M. Werlhof), nach Infekten, nach Heparin', 'schwere Blutungen erst unter 15.000–20.000/µl'],
        ], q=[('GE', 5)]),
        dict(h='Arteriosklerose und arterielle Thrombose', fl=dict(s=[
            ['Endothelschaden', 'mechanisch (Bluthochdruck), chemisch (Rauchen), Sauerstoffradikale (LDL, Fettstoffwechselstörung), Zuckerbindung (Diabetes mellitus)'],
            ['Lipoproteine lagern sich in der Intima ein', 'Makrophagen schaffen es nicht → Entzündung'],
            ['Glatte Muskelzellen wandern ein, die Wand verkalkt'], ['Plaque bricht auf', 'Thrombozyten aggregieren → Verschluss']]),
             li=['Gut **90 %** aller Herzinfarkte entstehen so; bei Schlaganfällen ist es etwa ein Drittel'], q=[('GE', '6–7')]),
        dict(h='Sekundäre Hämostase: Kaskadenmodell', tb=[
            ['Weg', 'Start', 'Ablauf'],
            ['Extrinsisch (exogen)', 'Verletzung legt **Gewebefaktor (III)** frei', 'III + VII → aktiviert X'],
            ['Intrinsisch (endogen)', '**XII** an negativen Oberflächen (z. B. Glas im Röhrchen)', 'XII → XI → IX (+ VIII) → aktiviert X'],
            ['Gemeinsame Endstrecke', 'Xa + Va', 'Prothrombin (II) → **Thrombin (IIa)** → Fibrinogen (I) → **Fibrin**; XIIIa vernetzt'],
        ], li=['12 Faktoren, gezählt bis 13 (VI ist in Wirklichkeit Va). Alle außer III (Gewebefaktor) und IV (Ca²⁺) stammen aus der **Leber**; fast alle sind Proteasen',
               '**Vitamin-K-abhängig:** II, VII, IX, X – Merke **1972** (Olympia-Attentat in München)'],
             q=[('GE', '8–9, 15')]),
        dict(h='Warum das Kaskadenmodell nicht reicht', li=[
            'Bei **Hämophilie A** (Faktor VIII fehlt) oder **B** (IX fehlt) dürfte nach dem Modell nichts passieren – der extrinsische Weg wäre ja da',
            'Tatsächlich liefert der extrinsische Weg nur ca. **5 %** des Thrombins – einen „**Thrombinfunken**“',
        ], fl=dict(s=[['III + VIIa auf subendothelialen Zellen', 'aktivieren X → etwas Thrombin'], ['Thrombin gelangt zu den Thrombozyten'],
                      ['Thrombin aktiviert XI, VIII, V, XIII und Thrombozyten', 'XIa aktiviert IX'],
                      ['VIIIa + IXa (intrinsische Tenase)', '50-mal effektiver als III/VIIa'], ['Xa + Va', 'Va verstärkt Xa 250–1000-fach → massive Thrombinbildung'],
                      ['Fibrinnetz, roter Thrombus']]),
             m='Das Kaskadenmodell beschreibt das **Reagenzglas**, das **zellbasierte Modell** den Körper: die Faktoren reagieren auf Zelloberflächen, beide Wege sind verwoben (VIIa aktiviert auch direkt XI bzw. IX – **Josso-Schleife**).',
             q=[('GE', '9–11'), ('VK', '1–2')]),
    ],
)
