THEMA = dict(
    id='gefaessregulation', titel='Regulation der Gefäßweite', bereich='Herz und Kreislauf',
    kurz='Vasomotorik, Bayliss-Effekt, NO, Nitroglycerin, Endothelin, Hypoxie, Euler-Liljestrand',
    lern=[
        dict(h='Vasomotorik', li=[
            '**Vasokonstriktion** = aktive Kontraktion der glatten Gefäßmuskelzellen → Durchmesser kleiner',
            '**Vasodilatation** = Erschlaffung → Durchmesser passiv größer',
            'Am Ende läuft alles über **Ca²⁺** in der Muskelzelle: über Gap Junctions aus Nachbarzellen und/oder über Calciumkanäle von außen',
            'Der Calciumkanal hat 5 Untereinheiten; bei einem Membranpotenzial von −40 bis −50 mV lässt er 10 Mio. Ca²⁺-Ionen pro Sekunde ein. Der L-Typ-Kanal der Gefäßmuskeln öffnet aber v. a. durch Anhängen eines Phosphats',
        ], tc=[['Wie der Kanal öffnet', 'Beispiel'], ['ligandengesteuert', 'Noradrenalin, Hormone'], ['spannungsabhängig', 'Depolarisation'], ['mechanisch', 'Dehnung → Bayliss-Effekt']],
             q=[('HK', '12–13')]),
        dict(h='Lokal oder überregional, schnell oder langsam', li=[
            '**Lokale** Mechanismen wirken **sofort**, aber nur, solange die Stoffe gebildet werden',
            'Das **vegetative Nervensystem** regelt schnell, je nach Innervation in ganz verschiedenen Organen',
            '**Langfristige**, überregionale Regulation läuft über **Hormone** im Blut – sie wirken überall, wo passende Rezeptoren sitzen',
        ], q=[('HK', '12, 15')]),
        dict(h='Bayliss-Effekt (myogene Autoregulation)', li=[
            'Der Blutdruck schwankt ständig. Manche Organe – v. a. die **Niere** – brauchen einen **stabilen Perfusionsdruck** (ca. 50 mmHg)',
        ], fl=dict(s=[['Perfusionsdruck steigt'], ['Gefäßwand wird gedehnt'], ['Mechanisch gesteuerte Ca²⁺-Kanäle öffnen'],
                      ['Zelle wird weniger negativ', 'viele spannungsabhängige Ca²⁺-Kanäle öffnen'], ['Kontraktion → Gefäß wird enger', 'Durchblutung bleibt gleich']]),
             q=[('HK', 15)]),
        dict(h='NO – das Gas aus dem Endothel', li=[
            '**Furchgott** (Nobelpreis 1998): ACh **erweiterte** Arterienringe – aber nur, solange das Endothel da war. Er postulierte einen „endothelial derived relaxing factor“ (EDRF) – es ist **NO**',
            'Histamin, Serotonin oder Bradykinin binden am Endothel → **eNOS**: Arginin → Citrullin + **NO**',
            'NO diffundiert in die Muskelschicht → **Relaxation** (über cGMP)',
        ], tc=[['Wirkung von NO', ''], ['Vasodilatation', 'Gefäß wird weiter'], ['hemmt die Thrombozytenaggregation', 'weniger Thrombosen'],
               ['hemmt die Vermehrung glatter Muskelzellen', 'Schutz vor Arteriosklerose']],
             m='**Nitroglycerin** (Nitrospray bei Angina pectoris) wird über die Mundschleimhaut aufgenommen und setzt in der Muskelzelle schnell NO frei → Vasodilatation. Es entsteht schnell eine **Nitrotoleranz**. Lebensgefährlich nach Viagra (starker Blutdruckabfall)!',
             q=[('HK', '16–17')]),
        dict(h='Endothelin-1 – der stärkste Vasokonstriktor', li=[
            '1988 entdeckt; Peptid aus dem Endothel, bindet an **ETA-Rezeptoren** der Muskelzellen → öffnet Ca²⁺-Kanäle → **Vasokonstriktion**',
            'Fördert auch die Zellvermehrung',
            'Gegenregelung: über **ETB-Rezeptoren** am Endothel wird mehr NO frei',
        ], q=[('HK', 17)]),
        dict(h='Hypoxie: Erweiterung – nur nicht in der Lunge', tb=[
            ['', 'Gehirn, Herz, Niere', 'Lunge'],
            ['Bei O₂-Mangel', '**Vasodilatation** → mehr Blut, die gelieferte O₂-Menge bleibt erhalten', '**Vasokonstriktion** (Euler-Liljestrand, hypoxische pulmonale Vasokonstriktion)'],
            ['Mechanismus', 'Muskelzellen verlieren K⁺ → Hyperpolarisation → Ca²⁺-Kanäle schließen', 'schlecht belüftete Alveolen werden weniger durchblutet'],
            ['Sinn', 'Organe mit geringer Ischämietoleranz schützen', 'nur belüftete Alveolen durchbluten → weniger **Shunt**'],
        ], q=[('HK', '17–18')]),
        dict(h='Kontraktion und Erschlaffung der glatten Muskelzelle', fl=dict(s=[
            ['Ca²⁺ steigt', 'L-Typ-Kanal oder sarkoplasmatisches Retikulum'], ['Ca²⁺ bindet **Calmodulin**', 'statt Troponin'],
            ['Kinase phosphoryliert die Myosin-Leichtketten'], ['Kontraktion = Vasokonstriktion']]),
             tc=[['Verengen', 'Erweitern'], ['Noradrenalin (α₁), Angiotensin II, Endothelin', 'NO, ANP (über cGMP), β₂-Aktivierung, Prostazyklin']],
             li=['Eine Phosphatase inaktiviert die Leichtketten → Relaxation = Vasodilatation'],
             q=[('HK', 29)]),
    ],
)
