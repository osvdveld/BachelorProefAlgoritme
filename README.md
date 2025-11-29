Beste

In dit document leg ik uit hoe de code werkt. (Bij vragen, opmerkingen of verbeteringen: oscar.vandevelde@ugent.be. U mag natuurlijk ook altijd de code aanpassen en een Pull Request naar de GitHub-pagina.)

Het programma neemt twee tekstbestanden aan. Het eerste is een bestand waarin de titels van alle projecten staan alsook de capaciteit van elk project. Het tweede is een lijst met alle namen van de studenten met hun 5 favoriete projecten (in volgorde). (Zie tekstbestand ... en ... als voorbeeld.) Deze voorbeelden zijn ook handig voor het jaar 2025 - 2026 aangezien dit exact de namen zijn van elk project met de juiste capaciteit en ook de lijst met de namen van de studenten uit dit jaar (met weliswaar fictieve projecten). 

Zoals u kan zien hebben sommigen regels twee namen. Dit zijn mensen die (fictief) een partner opgaven voor hun eerste keuze project. (De eerste naam is de student, de tweede de partner.) Hiervoor zijn enkele regels: 
- beide mensen moeten hetzelfde project op 1 hebben staan
- de studenten moeten beide elkaars naams hebben opgegeven
- de naam van de partner moet een valibele naam binnen de lijst van studenten zijn
Mensen met partners krijgen geen voorrang (ik heb hierover getwijfeld om het te implenteren in de code maar was niet zeker of dit de juiste keuze was).

Het programma neemt de lijst met studenten en hun projecten en 'randomised' de volgorde van deze lijst. Dan overloopt het programma elke student die nog geen project heeft toegewezen gekregen (in het begin is dit elke student). De eerste student krijgt zijn/haar eerste keuze. Voor de overige studenten kijkt het programma of deze student zijn/haar eerste keuze nog vrij is. Zo niet, dan slaat het de student over. Dit doet het programma 5 keer (voor 5 keuzes per student). De tweede ronde kijkt het naar de tweede keuze van de student