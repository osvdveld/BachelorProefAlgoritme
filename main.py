import random
import time

def main(bestandvoorkeuren, bestandprojecten, aantaliteraties=50):
    voorkeuren, partners = lees_studenten_voorkeuren(bestandvoorkeuren)
    projecten = uitlezen_projecten_aantal(bestandprojecten)

    beste_toewijzing = []
    beste_som = float('inf')

    for i in range(aantaliteraties):

        # random volgorde van studenten
        voorkeuren_random, partners_random = willekeurigevolgorde(voorkeuren, partners)

        # kopie van projecten
        projecten_copy = projecten.copy()

        # paren detecteren
        paren = detecteer_paren(voorkeuren_random, partners_random, projecten_copy)

        toewijzing, som = wijs_projecten_toe(voorkeuren_random, partners_random, projecten_copy, paren)

        if som < beste_som:
            beste_som = som
            beste_toewijzing = [toewijzing]
        elif som == beste_som:
            beste_toewijzing.append(toewijzing)

    return beste_toewijzing, beste_som


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


def wijs_projecten_toe(voorkeuren, partners, projecten, paren):
    toewijzing = {student: None for student in voorkeuren}
    max_rondes = max(len(v) for v in voorkeuren.values())
    som = 0

    # Zet paren om naar set-vorm voor snelle lookup
    is_in_paar = {}
    for a, b in paren:
        is_in_paar[a] = b
        is_in_paar[b] = a


    for ronde in range(max_rondes):

        # Eerst paren verwerken
        for a, b in paren:
            if toewijzing[a] is not None or toewijzing[b] is not None:
                continue  # al iets gekregen

            project = voorkeuren[a][ronde]

            if projecten.get(project, 0) >= 2:
                toewijzing[a] = project
                toewijzing[b] = project
                projecten[project] -= 2

                som += (ronde + 1) * 2  # beide tellen mee

        # Dan solo studenten
        for student, keuzes in voorkeuren.items():

            if student in is_in_paar:
                continue  # paren al behandeld

            if toewijzing[student] is not None:
                continue

            project = keuzes[ronde]

            if projecten.get(project, 0) > 0:
                toewijzing[student] = project
                projecten[project] -= 1
                som += (ronde + 1)

    # Straf voor studenten zonder project
    for student, project in toewijzing.items():
        if project is None:
            som += 6

    return toewijzing, som



if __name__ == "__main__":
    start = time.time()

    bestandvoorkeuren = "voorbeeldlijststudenten.txt"
    bestandprojecten = "projecten2526.txt"

    beste_toewijzing, beste_som = main(bestandvoorkeuren, bestandprojecten, aantaliteraties=10000)

    end = time.time()

    print("Beste som:", beste_som)
    print("Beste toewijzing(en):")
    for t in beste_toewijzing:
        print(t, "\n")

    print(f"Runtime: {end - start:.4f} seconds")
