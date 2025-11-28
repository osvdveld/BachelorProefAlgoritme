import random
import time

def main(bestandvoorkeuren, bestandprojecten, aantaliteraties=50):
    voorkeuren = lees_studenten_voorkeuren(bestandvoorkeuren)
    projecten = uitlezen_projecten_aantal(bestandprojecten)

    beste_toewijzing = []
    beste_som = float('inf')

    for i in range(aantaliteraties):

        # random volgorde van studenten
        voorkeuren_random = willekeurigevolgorde(voorkeuren)

        # kopie van projecten, anders beïnvloeden iteraties elkaar
        projecten_copy = projecten.copy()

        toewijzing, som = wijs_projecten_toe(voorkeuren_random, projecten_copy)

        # beste oplossing bijhouden
        if som < beste_som:
            beste_som = som
            beste_toewijzing = [toewijzing]
        elif som == beste_som:
            beste_toewijzing.append(toewijzing)

    return beste_toewijzing, beste_som


def lees_studenten_voorkeuren(bestandsnaam):
    voorkeuren = {}

    with open(bestandsnaam, "r", encoding="utf-8") as f:
        for lijn in f:
            lijn = lijn.strip()

            if lijn == "":
                continue

            delen = lijn.split(".")
            naam = delen[0].strip()
            projecten = [project.strip() for project in delen[1:]]

            voorkeuren[naam] = projecten

    return voorkeuren


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


def willekeurigevolgorde(voorkeuren):
    items = list(voorkeuren.items())
    random.shuffle(items)
    return dict(items)


def wijs_projecten_toe(voorkeuren, projecten):
    """
    Ronde 1 → 1e keuze
    Ronde 2 → 2e keuze
    ...
    Studenten die geen project krijgen → +6 punten straf
    """

    toewijzing = {student: None for student in voorkeuren}
    max_rondes = max(len(v) for v in voorkeuren.values())
    som = 0

    for ronde in range(max_rondes):
        for student, keuzes in voorkeuren.items():

            # student heeft al project
            if toewijzing[student] is not None:
                continue

            gewenste_project = keuzes[ronde]

            if projecten.get(gewenste_project, 0) > 0:
                toewijzing[student] = gewenste_project
                projecten[gewenste_project] -= 1
                som += (ronde + 1)

    for student, project in toewijzing.items():
        if project is None:
            som += 6   # strafscore


    return toewijzing, som


# uitvoeren
if __name__ == "__main__":
    start = time.time()   # start timing

    bestandvoorkeuren = "voorbeeldlijststudenten.txt"
    bestandprojecten = "projecten.txt"

    beste_toewijzing, beste_som = main(bestandvoorkeuren, bestandprojecten, aantaliteraties=100)

    end = time.time()     # end timing

    print("Beste som:", beste_som)
    print("Beste toewijzing(en):")
    for t in beste_toewijzing:
        print(t, "\n")

    print(f"Runtime: {end - start:.4f} seconds")
