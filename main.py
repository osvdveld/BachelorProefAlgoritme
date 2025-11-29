import random
import time

def main(bestandvoorkeuren, bestandprojecten, aantaliteraties=50):
    voorkeuren, partners = lees_studenten_voorkeuren(bestandvoorkeuren)
    projecten = uitlezen_projecten_aantal(bestandprojecten)

    beste_toewijzing = []
    beste_som = float('inf')
    beste_eerste = 0

    paren = detecteer_paren(voorkeuren, partners, projecten)
    for _ in range(aantaliteraties):
        # random volgorde van studenten
        voorkeuren_random, partners_random = willekeurigevolgorde(voorkeuren, partners)
        # kopie van projecten
        projecten_copy = projecten.copy()

        toewijzing, som, eerstekeuze = wijs_projecten_toe(voorkeuren_random, partners_random, projecten_copy, paren)

        if som < beste_som:
            beste_som = som
            beste_toewijzing = [toewijzing]
        elif som == beste_som:
            if eerstekeuze > beste_eerste:
                beste_eerste = eerstekeuze
                beste_toewijzing.append(toewijzing)

    return beste_toewijzing, beste_som, beste_eerste


def lees_studenten_voorkeuren(bestandsnaam):
    voorkeuren = {}
    partners = {}
    with open(bestandsnaam, "r", encoding="utf-8") as f:
        for lijn in f:
            lijn = lijn.strip()
            if lijn == "":
                continue
            delen = [d.strip() for d in lijn.split(".")]
            naam = delen[0]
            # Als tweede veld een partner is
            if len(delen) > 2 and (delen[1] in voorkeuren or delen[1].isalpha()):
                partner = delen[1]
                keuzes = delen[2:]
            else:
                partner = None
                keuzes = delen[1:]
            voorkeuren[naam] = keuzes
            partners[naam] = partner
    return voorkeuren, partners


def uitlezen_projecten_aantal(bestandsnaam):
    projecten = {}
    with open(bestandsnaam, "r", encoding="utf-8") as f:
        for lijn in f:
            lijn = lijn.strip()
            if lijn == "":
                continue
            delen = lijn.split(".")
            project_naam = delen[0].strip()
            aantal = int(delen[1].strip())
            projecten[project_naam] = aantal
    return projecten


def willekeurigevolgorde(voorkeuren, partners):
    items = list(voorkeuren.items())
    random.shuffle(items)

    nieuwe_voorkeuren = {k: v for k, v in items}
    nieuwe_partners = {k: partners[k] for k, _ in items}

    return nieuwe_voorkeuren, nieuwe_partners


def detecteer_paren(voorkeuren, partners, projecten):
    paren = []
    gebruikt = set()

    for student, partner in partners.items():
        if partner is None:
            continue
        if partner not in partners:
            continue  
        if partners.get(partner) != student:
            continue  
        if student in gebruikt or partner in gebruikt:
            continue

        # beide moeten zelfde eerste keuze hebben
        if voorkeuren[student][0] != voorkeuren[partner][0]:
            continue
        project = voorkeuren[student][0]
        # capaciteit check
        if projecten.get(project, 0) < 2:
            continue
        # geldige paar gevonden
        paren.append((student, partner))
        gebruikt.add(student)
        gebruikt.add(partner)

    return paren


def wijs_projecten_toe(voorkeuren, partners, projecten, paren, max_rondes = 5):
    """
    Wijs projecten toe in maximaal 5 rondes.
    - In ronde i wordt keuze[i] gebruikt.
    - Studenten wiens keuze[i] niet beschikbaar is, schuiven automatisch door naar een volgende ronde.
    - Paren worden altijd samen behandeld.
    """
    som=0
    eerstekeuze = 0
    toewijzing = {student: None for student in voorkeuren}

    partner_van = {}
    for a, b in paren:
        partner_van[a] = b
        partner_van[b] = a

    # Ronde-per-ronde toewijzen
    for ronde in range(max_rondes):
        # 1) Eerst alle paren behandelen
        for a, b in paren:
            # al toegewezen?
            if toewijzing[a] is not None:
                continue

            keuzes = voorkeuren[a]
            if ronde >= len(keuzes):
                continue  # geen keuze meer

            project = keuzes[ronde]
            # capaciteit check
            if projecten.get(project, 0) >= 2:
                toewijzing[a] = project
                toewijzing[b] = project
                projecten[project] -= 2
                som += (ronde + 1) * 2
                eerstekeuze += 2

        # 2) Solo studenten
        for student, keuzes in voorkeuren.items():
            # al toegewezen of deel van een paar?
            if toewijzing[student] is not None:
                continue
            if student in partner_van:
                continue
            if ronde >= len(keuzes):
                continue

            project = keuzes[ronde]

            if projecten.get(project, 0) > 0:
                if ronde == 0:
                    eerstekeuze += 1  
                toewijzing[student] = project
                projecten[project] -= 1
                som += (ronde + 1)

    # Strafpunten voor wie geen project heeft
    for student, project in toewijzing.items():
        if project is None:
            som += 6

    return toewijzing, som, eerstekeuze

if __name__ == "__main__":
    start = time.time()

    bestandvoorkeuren = "voorbeeldlijststudenten.txt"
    bestandprojecten = "projecten2526.txt"

    beste_toewijzing, beste_som, beste_eerste = main(bestandvoorkeuren, bestandprojecten, aantaliteraties=100000)

    end = time.time()

    print("Beste som:", beste_som)
    print("Beste toewijzing(en):")
    for t in beste_toewijzing:
        print(t, "\n")
    print("Beste aantal eerste keuzes:", beste_eerste)
    print(f"Runtime: {end - start:.4f} seconds")
