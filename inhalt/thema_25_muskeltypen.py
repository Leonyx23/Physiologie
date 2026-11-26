THEMA = dict(
    id='muskeltypen', titel='Skelett-, Herz- und glatte Muskulatur', bereich='Muskel',
    kurz='Unterschiede im Aufbau, in der Erregung und beim Calcium; Calcium-Antagonisten',
    lern=[
        dict(h='Die drei Muskeltypen im Vergleich', tb=[
            ['', 'Skelettmuskulatur', 'Herzmuskulatur', 'Glatte Muskulatur'],
            ['Zellen', '„Muskelfasern“', '„Kardiomyozyten“', '„glatte Muskelzellen“'],
            ['Querstreifung', 'ja, streng geordnete Sarkomere (A-, I-, Z-Streifen)', 'ja, Zellen über **Glanzstreifen** mit Gap Junctions verbunden', 'nein, Sarkomere unregelmäßig angeordnet'],
            ['Vorkommen', 'willkürliche Muskulatur des Bewegungsapparats', 'Herz', 'Hohlorgane (Speiseröhre, Magen, Darm, Harnwege, Gebärmutter), Gefäße, Bronchien'],
            ['Kerne', 'bis zu 500', '1 in der Zellmitte', '1 in der Zellmitte'],
            ['Länge', '20–30 cm', '50–120 µm', 'ca. 200 µm'],
            ['Calcium', 'T- und L-System des sarkoplasmatischen Retikulums', 'nur T-System; Ca²⁺ von innen und außen, auch über Gap Junctions', 'nur T-System; Ca²⁺ v. a. über Membrankanäle von außen'],
            ['Ansteuerung', 'willkürlich, motorische Endplatte (ACh), motorische Einheit', 'unwillkürlich: Erregungsleitungssystem, Schrittmacherzellen („funny current“), Alles-oder-nichts', 'unwillkürlich: **Single Unit** (Darm, Gebärmutter; Erregung über Gap Junctions) oder **Multi Unit** (Gefäße, Bronchien; einzeln innerviert)'],
        ], q=[('HK', 4)]),
        dict(h='Calcium in der glatten Muskulatur', li=[
            'Skelettmuskel: Ca²⁺ aus dem sarkoplasmatischen Retikulum, freigesetzt durch ein fortgeleitetes Aktionspotenzial, bindet an **Troponin**',
            'Glatter Muskel: Ca²⁺ strömt v. a. über **L-Typ-Calciumkanäle** in die Zelle und bindet an **Calmodulin**',
            'Die Kanäle öffnen sich durch vegetatives Nervensystem, Darmnervensystem, Hormone (z. B. Oxytocin an Gebärmutter und Brustdrüse), lokale Stoffe (z. B. Histamin an Gefäßen und Bronchien) oder Dehnung',
            'Glatte Muskulatur hat keine feste Zugrichtung – sie „fällt in sich zusammen“',
            'ATP braucht der Muskel für den **Querbrückenzyklus** und für die Calciumpumpe (**SERCA**)',
        ], m='**Calcium-Antagonisten** („-dipin“, z. B. Nifedipin, Amlodipin) blockieren die L-Typ-Kanäle der Gefäßmuskeln → weniger Kontraktion → der Blutdruck sinkt.',
             q=[('HK', '4–5')]),
        dict(h='Warum der Sympathikus Gefäße eng stellt', fl=dict(s=[
            ['Noradrenalin bindet an α₁-Rezeptoren'], ['L-Typ-Ca²⁺-Kanal wird aktiviert', 'durch Anhängen eines energiereichen Phosphats'],
            ['Ca²⁺ strömt ein, bindet Calmodulin'], ['Myosin-Leichtketten werden aktiviert'], ['Kontraktion → Vasokonstriktion']]),
             q=[('HK', 5), ('HK', 29)]),
    ],
)
