import random
import time

def main(bestandvoorkeuren, bestandprojecten, aantaliteraties=50):
    voorkeuren, partners = lees_studenten_voorkeuren(bestandvoorkeuren)
    projecten = uitlezen_projecten_aantal(bestandprojecten)

    beste_toewijzingen = []
    beste_som = float('inf')
    vrije_plekken_lijst = []
    paren = detecteer_paren(voorkeuren, partners, projecten)

    for _ in range(aantaliteraties):
        voorkeuren_random, partners_random = willekeurigevolgorde(voorkeuren, partners)
        projecten_copy = projecten.copy()

        toewijzing, som, vrije_plekken = wijs_projecten_toe(voorkeuren_random, partners_random, projecten_copy, paren)

        if som < beste_som:
            beste_som = som
            beste_toewijzingen = [toewijzing]
            vrije_plekken_lijst = [vrije_plekken]

        elif som == beste_som:
            beste_toewijzingen.append(toewijzing)
            vrije_plekken_lijst.append(vrije_plekken)

    # eerste-keuze scores berekenen
    scores = [(t, tel_eerste_keuzes(t, voorkeuren)) for t in beste_toewijzingen]
    # hoogste aantal eerste keuzes
    max_eerste = max(score for _, score in scores)
    # filteren
    beste_toewijzingen = [t for t, score in scores if score == max_eerste]

    return beste_toewijzingen, beste_som, max_eerste, aantaliteraties, vrije_plekken_lijst


def lees_studenten_voorkeuren(bestandsnaam):
    voorkeuren = {}
    partners = {}
    alle_namen = set()
    # verzamel namen om later paren te maken
    with open(bestandsnaam, "r", encoding="utf-8") as f:
        for lijn in f:
            lijn = lijn.strip()
            if lijn == "":
                continue
            delen = [d.strip() for d in lijn.split(".")]
            naam = delen[0]
            alle_namen.add(naam)

    # paren maken en keuzen linken
    with open(bestandsnaam, "r", encoding="utf-8") as f:
        for lijn in f:
            lijn = lijn.strip()
            if lijn == "":
                continue
            delen = [d.strip() for d in lijn.split(".")]
            naam = delen[0]

            # partner = tweede veld, maar alleen als die naam in het tekstbestand voorkomt
            if delen[1] in alle_namen:
                partner = delen[1]
                keuzes = delen[2:]
            else:
                partner = None
                keuzes = delen[1:]
            partners[naam] = partner
            voorkeuren[naam] = keuzes
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
        print(paren)
    return paren


def wijs_projecten_toe(voorkeuren, partners, projecten, paren, max_rondes = 5):
    """
    Wijs projecten toe in maximaal 5 rondes.
    - In ronde i wordt keuze[i] gebruikt.
    - Studenten wiens keuze[i] niet beschikbaar is, schuiven automatisch door naar een volgende ronde.
    - Paren worden altijd samen behandeld.
    """
    som=0
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
                toewijzing[student] = project
                projecten[project] -= 1
                som += (ronde + 1)

    # Strafpunten voor wie geen project heeft
    for student, project in toewijzing.items():
        if project is None:
            som += 6

    # Niet-toegewezen projecten
    vrije_plekken = {project: cap for project, cap in projecten.items() if cap > 0}

    return toewijzing, som, vrije_plekken


def tel_eerste_keuzes(toewijzing, voorkeuren):
    count = 0
    for student, project in toewijzing.items():
        if voorkeuren[student][0] == project:
            count += 1
    return count


def output(gekozen_toewijzing, vrije_plekken, beste_som, beste_toewijzing, beste_eerste, aantaliter, start, end,
            outputprojecten="output/toewijzing_projecten", outputvrijeplekken="output/vrije_plekken"):
    with open(f"{outputprojecten}.txt", "w", encoding="utf-8") as f:
        f.write("Projecttoewijzing per student (alfabetisch):\n\n")
        for student in sorted(gekozen_toewijzing.keys()):
            f.write(f"{student}: {gekozen_toewijzing[student]}\n")

    with open(f"{outputvrijeplekken}.txt", "w", encoding="utf-8") as f:
        f.write("Vrije plekken na toewijzing:\n\n")
        for project, cap in vrije_plekken.items():
            f.write(f"{project}: {cap}\n")


    print("\nBeste som:", beste_som) 
    print(len(beste_toewijzing), "beste toewijzing(en) gevonden.") 
    print(f"Dit komt neer op {(len(beste_toewijzing) / aantaliter * 100):.2f}% van alle iteraties.") 
    print("Het aantal studenten dat zijn/haar eerste keuze krijgt:", beste_eerste) 
    print(f"Runtime: {end - start:.4f} seconds")
    print("\nBestanden zijn opgeslagen:")
    print(f"- {outputprojecten}.txt")
    print(f"- {outputvrijeplekken}.txt")




if __name__ == "__main__":
    start = time.time()

    # Pas hier de bestandnamen aan indien nodig
    keuzesbestand = "input/voorbeeldlijststudenten.txt"
    projectenbestand = "input/Projecten2526.txt"

    # Pas hier het aantal iteraties aan indien nodig
    beste_toewijzing, beste_som, beste_eerste, aantaliter, vrije_plekken_lijst = main(keuzesbestand, 
                                                                                      projectenbestand, 
                                                                                      aantaliteraties = 100)
    gekozen_toewijzing = random.choice(beste_toewijzing)
    index = beste_toewijzing.index(gekozen_toewijzing)
    vrije_plekken = vrije_plekken_lijst[index]

    end = time.time()

    # Output. Pas hier de outputbestandsnamen aan indien nodig
    output(gekozen_toewijzing, vrije_plekken, beste_som, beste_toewijzing, beste_eerste, aantaliter, start, end,
           outputprojecten="output/toewijzing_projecten", outputvrijeplekken="output/vrije_plekken")
