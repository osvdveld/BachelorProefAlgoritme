In dit document leg ik uit hoe de code werkt. Bij vragen, opmerkingen of verbeteringen: oscar.vandevelde@ugent.be. U mag natuurlijk ook altijd de code aanpassen en een Pull Request indienen op deze ([GitHub-pagina](https://github.com/osvdveld/BachelorProefAlgoritme)).

Het programma neemt twee tekstbestanden aan. Het eerste is een bestand waarin de titels van alle projecten staan alsook de capaciteit van elk project. Het tweede is een lijst met alle namen van de studenten met hun 5 favoriete projecten (in volgorde). (Zie tekstbestand ... en ... als voorbeeld.) Deze voorbeelden zijn ook handig voor het jaar 2025 - 2026 aangezien dit exact de namen zijn van elk project met de juiste capaciteit en ook de lijst met de namen van de studenten uit dit jaar (met weliswaar fictieve projecten). 
BELANGRIJK: De namen van studenten (bij paren) en de projecten moeten gescheiden worden door een '.' (zie ook voorbeeld)!

Zoals u kan zien hebben sommigen regels twee namen. Dit zijn mensen die (fictief) een partner opgaven voor hun eerste keuze project. (De eerste naam is de student, de tweede de partner.) Hiervoor zijn enkele regels: 
- beide mensen moeten hetzelfde project op 1 hebben staan
- de studenten moeten beide elkaars naams hebben opgegeven
- de naam van de partner moet een valibele naam binnen de lijst van studenten zijn
Mensen met partners worden apart (en eerst) behandeld waardoor ze voorrang krijgen.

Het programma neemt de lijst met studenten en hun projecten en 'randomised' de volgorde van deze lijst. Dan overloopt het programma elke student die nog geen project heeft toegewezen gekregen (in het begin is dit elke student). De eerste student krijgt zijn/haar eerste keuze. Voor de overige studenten kijkt het programma of deze student zijn/haar eerste keuze nog vrij is. Zo niet, dan slaat het de student over. Dit doet het programma 5 keer (voor 5 keuzes per student). De tweede ronde kijkt het naar de tweede keuze van de student enzoverder. 

Studenten die geen keuze krijgen worden voorgesteld door 'None'. Deze zal u dus zelf nog een project moeten toewijzen. Dit kan u doen aan de hand van de lijst van projecten die nog niet vol zitten die wordt meegegeven.

Vervolgens 'randomised' het programma de volgorde opnieuw en doet het exact hetzelfde. Om te meten welke 'volgorde' (en dus toewijzing) het beste is, werkt het met een puntensysteem. Als een student zijn/haar eerste keuze krijgt, telt dat voor 1 punt enzoverder. Alleen de toewijzing(en) met het laagste aantal punten worden behouden. Om dan nog verder te elimineren tussen toewijzingen bekijkt men het aantal studenten die hun eerste keuze kregen. Zo krijgt men een aantal toewijzingen die zo optimaal mogelijk zijn (afhankelijk van hoeveel iteraties u kiest). Mensen die geen project krijgen tellen voor 6 punten mee. U kan deze 'straf' aanpassen naar gelang hoe belangrijk u het vindt dat een student een project uit zijn/haar lijst krijgt. 
(De grootte van de straf heeft weinig tot geen impact op het aantal niet-toegewezen projecten, zolang de straf niet te klein is. Gemiddeld, bij een straf groter dan 5 punten, ligt het aantal niet-toegewezen projecten op 10.)
