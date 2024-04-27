# BelegDiskreteSimulation
Dieses Projekt bildet den Beleg für den Kurs "Diskrete Simulation" im Sommersemester 2024 ab

Aufgabenstellung:
Das Hotel Goldener Adler in Kirchberg, Tirol möchte kalkulieren wie viele Mitarbeiter es sich leisten kann einzustellen jeweils für Sommer- und Wintersaison. Das Hotel hat 500 Zimmer, die schwankend nach Saison, Wetter und Gesamtnachfrage der Übernachtungen ausgelastet sind. Der Preis für eine Übernachtung wird vom Wirt selbst festgelegt und liegt, basierend auf Erfahrungswerten, zwischen 80-150€. 

Der Preis unterliegt jedoch kurzfristigen Schwankungen. Um Wettbewerbsfähig zu sein muss der Wirt den Preis senken, wenn die Gesamtnachfrage für Übernachtungen in Tirol sinkt oder das Wetter im Winter nicht mehr zum Skifahren geeignet ist. Andererseits kann er die Preise erhöhen, wenn die Gesamtnachfrage nach Übernachtungen in Tirol stark ansteigt.

Dadurch muss der Wirt mehrere Kenngrößen basierend auf historischen Daten simulieren: 
        - Die Gesamtnachfrage
        - Die Auslastung seines Hotels
        - Die Temperatur im Winter, um einschätzen zu können, ob Skifahren möglich ist

Das Personal wird nach der Nomenklatur Tirol bezahlt. Erfahrungsgemäß kostet ein Mitarbeiter dem Wirt das doppelte von seinem Bruttolohn. Ermitteln Sie wie viele Hotelfachkräfte eingestellt werden sollten für die nächste Saison, wenn die Personalkosten maximal 30% der Einnahmen betragen dürfen.

Überlegungen:
Um die Gesamtnachfrage nach Übernachtungen in Tirol einschätzen zu können, habe ich auf historische Daten zurückgegriffen (Quelle 1). Dabei habe ich die Nächtigungen von 2000-2023 betrachtet und basierend auf diesen Werten eine normalverteilte Simulation durchgeführt. Die Jahre 2020,2021 habe ich aufgrund des Sondereinflusses von Covid weggelassen, wobei man durchaus argumentieren kann diese Werte ebenfalls mit zu berücksichtigen.

Die Auslastung des Hotels habe ich basierend auf historischen Daten für die Hotelauslastung in Österreich simuliert (Quelle 2). Dabei habe ich die Jahre 2012-2019 als Datengrundlage genommen.

Für die Temperatur habe ich ebenfalls auf historische Durchschnittswerte für Kirchberg, Tirol zurückgegriffen (Quelle 3). Im Gegensatz zu den anderen Werten teilen sich diese auf Monate auf und nicht auf die Saison. Daher habe ich für die Wintersaison die Monate von November bis April gesondert betrachtet. Sicherlich hätte man hier um dem Klimawandel gerecht zu werden eine gewisse dynamik in die Werte einbauen können.

Für alle Simulationsobjekte habe ich mich für normalverteilte Werte entschieden, da diese für mich realistischer erscheinen bei den genannten Beispielen als etwa gleichverteilte Werte.

Kosten für das Personal sind Lohngruppe 3 mit 4-6 Jahren Berufserfahrung der Nomenklatur Tirol (Quelle 4).

Der Code unterteilt sich in vier Bereiche:
1. Das setzen der wichtigsten Parameter erfolgt durch den User. Folgende Parameter können gesetzt werden:
    - Preis für eine Übernachtung im Winter: 150€
    - Preis für eine Übernachtung im Sommer: 80€
    - Anzahl der Zimmer, die zu vermieten sind: 500
    - Anzahl der Durchläufe für die Montecarlo-Simulation: 1000
2. Die Datenhaltung. Hier sind alle historischen Daten zu den Simulationsobjekten abgelegt
3. Die Vorbereitung der Simulation. Hier werden Standardabweichung und Mittelwert ermittelt, um anschließend mit numpy die Simulationen durchführen zu können.
4. Die Simulation. Hier wurden die Werte in eine for-Schleife eingesetzt. Dadurch kann die Anzahl der Versuche für die Montecarlo Simulationen durchlaufen werden. Folgende Schritte folgen:
    - Simulation der Auslastungsrate. Daraus wird die Anzahl der belegten Zimmer berechnet
    - Simulation der Gesamtnachfrage nach Übernachtungen in Tirol: Der Preis steigt, wenn die Nachfrage über dem Durchschnitt für die Saison liegt. Der Preis sinkt, wenn die Nachfrage unter dem Durchschnitt für die Saison liegt.
    - Simulation der Temperatur für die einzelnen Monate in Kirchberg: Hier werden die Temperaturen der Monate für die Wintersaison ausgewertet. Wenn es an einem Tag im Winter 0 Grad oder wärmer ist, muss künstlich beschneit werden. Die Erfahrung des Skifahrens leidet und der Preis sinkt leicht. Wenn es wärmer als 3 Grad ist, kann kaum noch künstlich beschneit werden. Es kann kaum noch Skigefahren werden. Die Preise sinken noch weiter
5. Aus den Preisen werden die Einnahmen für die Monate der Wintersaison berechnet und für die Sommersaison. Abgeleitet aus dem Ertrag werden dann die in der Aufgabenstellung geforderten 30% für Personalkosten berechnet. Dieses Budget wird anschließen durch die Kosten für eine Fachkraft pro Saison geteilt. Dadurch kann genau bestimmt werden wie viele Fachkräfte der Wirt für eine Saison einstellen kann.

Resume:
Das Program ist so konzipiert, dass es dem Nutzer erlaubt die Basisparameter selbst zu wählen.
Mit denen in der Aufgabenstellung gegebenen Parametern hat das Tool folgende Werte geliefert:

    Input:
            Preis für eine Übernachtung im Winter: 150€
            Preis für eine Übernachtung im Sommer: 80€
            Anzahl der Zimmer, die zu vermieten sind: 500
            Anzahl der Durchläufe für die Montecarlo-Simulation: 1000

    Output:
            | Parameter| Wert  | 
            |:-------------------|:----------:|
            | Einnahmen November         | 862,840.95 € |
            | Einnahmen Dezember         | 952,940.155 € |
            | Einnahmen Januar      | 959,154.26 € |
            | Einnahmen Februar       | 859,217.24 €  |
            | Einnahmen März      | 896,206.745 € |
            | Einnahmen April         | 818,607.6 € |
            |:-------------------|:----------:|
            | Einnahmen Wintersaison gesamt          | 534,896,6.95 € |
            | Einnahmen Sommersaison gesamt        |  314,477,2.8 €  |
            |:-------------------|:----------:|
            | Die empfohlene Anzahl Fachkräfte für den Winter:           |  68 |
            | Die empfohlene Anzahl Fachkräfte für den Sommer:        | 40|



Ausführung:
Im Terminal den folgenden Code ausführen:

'''python Kirchberg.py '''

Quellen:


1: https://www.tirol.gv.at/statistik-budget/statistik/tourismus/
Aufgerufen am: 27.04.2024

2: https://de.statista.com/statistik/daten/studie/814504/umfrage/bettenauslastung-in-hotels-in-oesterreich-in-der-winter-und-sommersaison/#:~:text=Bettenauslastung%20in%20Hotels%20in%20%C3%96sterreich%20nach%20Saisons%20bis%202021%2F2022&text=In%20der%20Sommersaison%202022%20(Mai,zu%2043%2C3%20Prozent%20ausgelastet.
Aufgerufen am: 27.04.2024

3: https://de.climate-data.org/europa/oesterreich/tirol/kirchberg-in-tirol-158904/
Aufgerufen am: 27.04.2024

4: https://www.wko.at/oe/kollektivvertrag/loehne-gastronomie-hotellerie-tirol-2023.pdf
Aufgerufen am: 27.04.2024


