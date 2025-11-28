def lees_studenten_voorkeuren(bestandsnaam):
    """
    Leest een tekstbestand waarin elke lijn bestaat uit:
    Naam.Project X.Project Y.Project Z ...
    
    Geeft een dictionary terug:
    { 'Naam': ['Project X', 'Project Y', ...], ... }
    """
    
    voorkeuren = {}

    with open(bestandsnaam, "r", encoding="utf-8") as f:
        for lijn in f:
            lijn = lijn.strip()

            # sla lege regels over
            if lijn == "":
                continue

            delen = lijn.split(".")

            # eerste stukje = naam
            naam = delen[0].strip()

            # rest = lijst van projecten
            projecten = [project.strip() for project in delen[1:]]

            voorkeuren[naam] = projecten

    return voorkeuren

lees_studenten_voorkeuren("voorbeeldlijststudenten.txt")