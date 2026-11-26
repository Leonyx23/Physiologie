FRAGEN = dict(
    id='test', titel='Testrazzia', razzia=2,
    fragen=[
        dict(id='t1', thema='energie', f='Wofür braucht der Körper Energie?',
             a=[dict(li=['Muskelkontraktion', 'Synthese', 'Transport'])], q=[('A', 3)]),
        dict(id='t2', thema='energie', f='Wie viel ATP liefert die anaerobe Glykolyse?',
             a=[dict(li=['**2 ATP** je Glukose'])], q=[('A', 4), ('B', 1)],
             korr=['Vorlage: „2 ADP“ – richtig sind 2 ATP.']),
        dict(id='t3', nr='III.6a', thema='energie', f='Säure (Laktat)?',
             abb=[dict(h='Abbildung (nachgezeichnet)', br=dict(s=[['Pre', 0, '0 %'], ['Post', 6, '+6 %']]))], a=[dict(m='Laktat ist das Anion der Milchsäure.')],
             q=[('A', 5)]),
        dict(id='t4', nr='III.6b', thema='energie', f='Gleiche Abbildung, andere Frage?',
             abb=[dict(h='Abbildung (nachgezeichnet)', br=dict(s=[['Pre', 0, '0 %'], ['Post', 6, '+6 %']]))],
             a=[dict(li=['Antwort vier'])], q=[('A', 6)]),
    ],
)
