THEMA = dict(
    id='kreislaufreflexe', titel='Blutdruckregulation durch Reflexe und Hormone', bereich='Herz und Kreislauf',
    kurz='Barorezeptorreflex, Bainbridge-Reflex, Henry-Gauer-Reflex, Rezeptoren an Herz und Gefäßen',
    lern=[
        dict(h='Warum es einen Reflex braucht', li=[
            'Beim Aufstehen fließt das Blut wegen der Schwerkraft schwerer aus den Beinvenen zum Herzen zurück',
        ], fl=dict(s=[['Aufstehen'], ['Vorlast sinkt'], ['Schlagvolumen und HZV sinken'], ['Blutdruck sinkt'], ['Barorezeptorreflex gleicht aus']]),
             q=[('HK', 18)]),
        dict(h='Barorezeptorreflex (Pressorezeptorreflex)', tc=[
            ['Komponente', 'Was'],
            ['1. Rezeptoren', 'Pressorezeptoren im Karotissinus und Aortenbogen messen die Wanddehnung'],
            ['2. Afferenzen', 'Hirnnerven IX (glossopharyngeus) und X (vagus)'],
            ['3. Kreislaufzentrum', 'Medulla oblongata'],
            ['4. Efferenzen', 'Parasympathikus (Vagus, ACh an M₂) und Sympathikus'],
            ['5. Effektoren', 'Herz, Arteriolen, Nebennierenmark'],
        ], li=['Fällt der Druck, steigen **innerhalb von 2 Herzschlägen** Herzfrequenz, Kontraktilität und TPR'],
             m='Ein akuter Blutdruckabfall führt zu einem Anstieg – ein akuter Anstieg zu einem Abfall.',
             q=[('HK', '18–19')]),
        dict(h='Bainbridge-Reflex', fl=dict(s=[['Mehr Blutvolumen', 'mehr venöser Rückstrom'], ['Rechter Vorhof wird gedehnt', 'Dehnungsrezeptoren'],
                                              ['Afferenzen im N. vagus', 'zum Kreislaufzentrum'], ['Sympathikus ↑ / Parasympathikus ↓ am Sinusknoten'], ['Herzfrequenz steigt']]),
             li=['Der Sympathikus beschleunigt die Erregungsbildung im Sinusknoten, der Parasympathikus verzögert sie',
                 'Achtung Skript (S. 17): Auslöser ist der erhöhte **Vorhofdruck** bzw. das Volumen (nicht der arterielle Druck), und die Rezeptoren melden über **Afferenzen**, nicht Efferenzen des Vagus'],
             q=[('HK', '17–18')]),
        dict(h='Rezeptoren an Herz und herznahen Gefäßen', tb=[
            ['Rezeptor', 'Lage', 'Misst', 'Verschaltung'],
            ['Pressorezeptoren', 'Aortenbogen, Karotisgabel', 'Wanddehnung (Druck)', 'vegetatives Nervensystem'],
            ['Volumenrezeptoren', 'rechter Vorhof, Hohlvenen', 'Dehnung (Füllung)', 'vegetatives Nervensystem + Hypothalamus → Hypophysenhinterlappen'],
            ['Chemorezeptoren', 'Aortenbogen, Karotisgabel (N. vagus)', 'pO₂, pCO₂, pH', 'Atem- und Kreislaufzentrum'],
        ], m='**Henry-Gauer-Reflex:** schlechte Füllung des rechten Herzens (Volumenmangel) → mehr **ADH** aus der Hypophyse → die Niere spart Wasser.',
             q=[('EX5', 14)]),
        dict(h='Langfristig: Hormone', tb=[
            ['System', 'Wirkung', 'Mehr dazu'],
            ['RAAS', 'Angiotensin II verengt Gefäße, Aldosteron hält Na⁺ und Wasser zurück → Volumen und Druck steigen', 'Lernseite „RAAS, ADH und Calciumhaushalt“'],
            ['ADH', 'Wasserrückresorption im Sammelrohr, Vasokonstriktion', 'ebenda'],
            ['Adrenalin/Noradrenalin', 'aus dem Nebennierenmark, wirken wie der Sympathikus', 'Lernseite „Vegetatives Nervensystem“'],
        ], q=[('HK', 3), ('EX5', '9–13')]),
    ],
)
