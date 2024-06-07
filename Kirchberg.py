import numpy as np
import matplotlib.pyplot as plt

'''----------------------------------------------------------Setzen der wichtigsten Parameter -------------------------------------------------------------------'''
'''@preis_winter Preis den der Wirt für eine Übernachtung im Winter ansetzt
@preis_sommer Preis den der Wirt für eine Übernachtung im Sommer ansetzt
@anzahl_zimmer Anzahl der Zimmer die der Wirt zu vermieten hat
@preis_fachkraft Arbeitskosten von einer Hotelfachkraft in Euro'''
# Basispreise setzen, auch Änderung möglich
try:
    winter_preis = int(input("Welchen Basispreis soll ein Zimmer im Winter haben? "))
    preis_winter = winter_preis
    sommer_preis = int(input("Welchen Basispreis soll ein Zimmer im Sommer haben? "))
    preis_sommer = sommer_preis

    anzahl_zimmer = int(input("Wie viele Zimmer sollen vermietet werden? "))

    # Anzahl der Versuche der Monte-Carlo Simulation festlegen
    monte_carlo = int(input("Wie viele Simulationen sollen durchgeführt werden? "))

except ValueError:
    print("Bitte einen ganzzahligen Integer eingeben")

# Quelle 4 - Nomenklatur Tirol für Fachkraft mit 4-6 Jahren Berufserfahrung
# Verdopplung des Bruttogehaltes, um die gesamten verursachten Kosten zu berechnen
preis_fachkraft = (1953.90 * 2)

'''--------------------------------------------------------Definieren einer Funktion----------------------------------------------------------'''

''' Überprüfen wie viele Tage eines Monats sich im Winter nicht zum Skifahren eignen.
Wenn es zu viele sind wird der Preis gesenkt. Die Senkung des Preises ist Subjektiv und kann angepasst werden
@simulation zeitreihe der Tagesmiteltemperaturen der einzelnen Monate
'''
def temperature_price_room_influence(simulation):

    # Temporäre Variablen um Tage mit Wetter über 3C und über 0C zu speichern
    # Ab über 3C kann man nicht mehr Skifahren
    bad_skiing_days = 0
    non_skiing_days = 0

    for day in simulation:
        if day >= 3:
            non_skiing_days +=1
        elif day >= 0 and day < 3:
            bad_skiing_days += 1

     # temporäre Variable, um den Preis pro Monat zu bestimmen
    preis_delta = 0

    # Wenn es mehr als 15 Tage über 3C gibt, senke den Preis um 20€ pro Nacht
    if non_skiing_days >= 15:
        preis_delta += 20
        return preis_delta
    elif non_skiing_days >= 10:
        preis_delta += 15
        return preis_delta
    elif non_skiing_days >= 5:
        preis_delta += 10
        return preis_delta
    # Wenn es mehr als 5 Tage über 0C gibt, senke den Preis um 5€ pro Nacht
    elif bad_skiing_days >= 5:
        preis_delta += 5
        return preis_delta
    else:
        preis_delta += 0
        return preis_delta


'''-----------------------------------------Datenhaltung von Auslastung, Wetter und Nachfrage-------------------------------------------------------'''

# Auslastungsraten für Hotels in Österreich von 2012 - 2019
# Quelle 2 siehe Dokumentationtatista
auslastungsrate_winter = [0.4040,0.3990,0.4040,0.4140,0.4140,0.4290,0.4340]
auslastungsrate_sommer = [0.41, 0.4150,0.4270,0.4440,0.4480,0.4510,0.4620]

# Tirol Nächtigungen pro Saison
# Von 2000 - 2023 ausgenommen[2020,2021] aufgrund von Covid
# Quelle 1 siehe Dokumentation
sommer_demand = [22788556,22443288,22161313,21798908,21188147, 20767759, 19669564, 18953625, 18715631, 18325187, 18068597, 17784386, 17547539, 17806549, 17447438, 16895521, 17292843, 17382307, 17792473, 17656247, 17006337, 17404601]    
winter_demand= [25707235,20912701,27486459,27580594, 26464201, 26800488, 25960346, 25368026, 26189170, 25699115, 24830645, 25241464, 25584483, 25612058, 24062117, 24766815, 25047404, 24648277, 24345343, 23870576, 23503160, 22400614]

# Durchschnittliche Temperaturdaten für Kirchberg, Tirol von 1991 -2021 
# Quelle 3 siehe Dokumentation
januar_temp_avg = -6.1
januar_temp_min = -10.5
januar_temp_max = -0.9

februar_temp_avg = -4.4
februar_temp_min = -9.1
februar_temp_max = 0.6

maerz_temp_avg = -0.7
maerz_temp_min = -5.8
maerz_temp_max = 4.3

april_temp_avg = 3.1
april_temp_min = -2.6
april_temp_max = 8.3

mai_temp_avg = 8
mai_temp_min = 1.9
mai_temp_max = 13.2

juni_temp_avg = 12.1
juni_temp_min = 6.3
juni_temp_max = 17.1

juli_temp_avg = 13.6
juli_temp_min = 8
juli_temp_max = 18.7

august_temp_avg = 13.5
august_temp_min = 8
august_temp_max = 18.7

september_temp_avg = 9.6
september_temp_min = 4.5
september_temp_max = 14.7

oktober_temp_avg = 5.8
oktober_temp_min = 0.7
oktober_temp_max = 11.4

november_temp_avg = -0.1
november_temp_min = -4.8
november_temp_max = 5.2

dezember_temp_avg = -4.8
dezember_temp_min = -9.2
dezember_temp_max = 0.4


'''-----------------------------------------Vorbereitung der Simulation von Auslastung, Wetter und Nachfrage----------------------------------'''


# Durchschnitt und Standardabweichung berechnen, damit daraus eine Normalverteilung für die Auslastungsrate simuliert werden kann
avg_auslastung_winter = np.mean(auslastungsrate_winter)
avg_auslastung_sommer = np.mean(auslastungsrate_sommer)
std_auslastung_winter = np.std(auslastungsrate_winter)
std_auslastung_sommer = np.std(auslastungsrate_sommer)


# Simulation von der gesamten Anzahl an Übernachtungen in Tirol im Winter und im Sommer
# Mittelwert und Standardabweichung bestimmen
avg_sommer = np.mean(sommer_demand)
avg_winter = np.mean(winter_demand)
std_sommer = np.std(sommer_demand)
std_winter = np.std(winter_demand)


# Erzeugung von Zufallswerten für die Temperaturen über die einzelnen Monate
# Normalverteilung gewählt, weil eine Gleichverteilung sehr unwahrscheinlich ist
std_januar = (abs(januar_temp_avg - januar_temp_min) + abs(januar_temp_max - januar_temp_avg)) / 2
std_februar = (abs(februar_temp_avg - februar_temp_min) + abs(februar_temp_max - februar_temp_avg)) / 2
std_maerz = (abs(maerz_temp_avg - maerz_temp_min) + abs(maerz_temp_max - maerz_temp_avg)) / 2
std_april = (abs(april_temp_avg - april_temp_min) + abs(april_temp_max - april_temp_avg)) / 2
std_mai = (abs(mai_temp_avg - mai_temp_min) + abs(mai_temp_max - mai_temp_avg)) / 2
std_juni = (abs(juni_temp_avg - juni_temp_min) + abs(juni_temp_max - juni_temp_avg)) / 2
std_juli = (abs(juli_temp_avg - juli_temp_min) + abs(juli_temp_max - juli_temp_avg)) / 2
std_august = (abs(august_temp_avg - august_temp_min) + abs(august_temp_max - august_temp_avg)) / 2
std_september = (abs(september_temp_avg - september_temp_min) + abs(september_temp_max - september_temp_avg)) / 2
std_oktober = (abs(oktober_temp_avg - oktober_temp_min) + abs(oktober_temp_max - oktober_temp_avg)) / 2
std_november = (abs(november_temp_avg - november_temp_min) + abs(november_temp_max - november_temp_avg)) / 2
std_dezember = (abs(dezember_temp_avg - dezember_temp_min) + abs(dezember_temp_max - dezember_temp_avg)) / 2


'''-----------------------------------------Simulation von Auslastung, Wetter und Nachfrage---------------------------------------------------'''


# Anlegen von Arrays, um die Werte für die einzelnen Durchläufe der Simulation zu speichern
betten_belegt_winter_array = []
betten_belegt_sommer_array = []
preis_winter_array = []
preis_sommer_array = []
umsatz_november_array = []
umsatz_dezember_array = []
umsatz_januar_array = []
umsatz_februar_array = []
umsatz_maerz_array = []
umsatz_april_array = []
umsatz_winter_array = []
umsatz_sommer_array = []
budget_personal_sommer_array = []
budget_personal_winter_array = []
anzahl_fachkraft_winter_array = []
anzahl_fachkraft_sommer_array = []
preis_november_array = []


for i in range(monte_carlo): 
    ''' Generierung von normalverteilten Zufallszahlen 
    @loc bildet den Ausgangspunkt für die Simulation der Daten (Zentrum der Verteilung)
    @scale Standardabweichung vom Ausgangspunkt
    @size Azahl der Tage für den Monat
    '''
    # Simulation der Auslastungsrate für Sommer und Winter
    simulation_auslastungsrate_winter = np.random.normal(loc=avg_auslastung_winter, scale=std_auslastung_winter)
    simulation_auslastungsrate_sommer = np.random.normal(loc=avg_auslastung_sommer, scale=std_auslastung_sommer)

    # Berechnung der konkreten Anzahl an Betten
    betten_belegt_winter = int(round(simulation_auslastungsrate_winter * anzahl_zimmer,0))
    betten_belegt_winter_array.append(betten_belegt_winter)
    betten_belegt_sommer = int(round(simulation_auslastungsrate_sommer * anzahl_zimmer,0))
    betten_belegt_sommer_array.append(betten_belegt_sommer)

    # Simulation für die Anzahl an Übernachtungsgäste durchführen
    simulation_uebernachtungen_winter = np.random.normal(loc=avg_winter, scale=std_winter)
    simulation_uebernachtungen_sommer = np.random.normal(loc=avg_sommer, scale=std_sommer)

    # Generierung von normalverteilten Zufallszahlen für das Wetter
    simulation_temp_januar = np.random.normal(loc=januar_temp_avg, scale=std_januar, size=31)
    simulation_temp_februar = np.random.normal(loc=februar_temp_avg, scale=std_februar, size=28)
    simulation_temp_maerz = np.random.normal(loc=maerz_temp_avg, scale=std_maerz, size=31)
    simulation_temp_april = np.random.normal(loc=april_temp_avg, scale=std_april, size=30)
    simulation_temp_mai = np.random.normal(loc=mai_temp_avg, scale=std_mai, size=31)
    simulation_temp_juni = np.random.normal(loc=juni_temp_avg, scale=std_juni, size=30)
    simulation_temp_juli = np.random.normal(loc=juli_temp_avg, scale=std_juli, size=31)
    simulation_temp_august = np.random.normal(loc=august_temp_avg, scale=std_august, size=31)
    simulation_temp_september = np.random.normal(loc=september_temp_avg, scale=std_september, size=30)
    simulation_temp_oktober = np.random.normal(loc=oktober_temp_avg, scale=std_oktober, size=31)
    simulation_temp_november = np.random.normal(loc=november_temp_avg, scale=std_november, size=30)
    simulation_temp_dezember = np.random.normal(loc=dezember_temp_avg, scale=std_dezember, size=31)


    '''-----------------------------------------Preisanpassungen basierend auf Gesamtnachfrage -------------------------------------------------------'''


    # Preisanpassung für den Preis pro Zimmer in einer Nacht basierend auf der Simulation der gesamten Übernachtungen in Tirol
    # Winter
    preis_winter_delta = 0
    preis_sommer_delta = 0

    if simulation_uebernachtungen_winter < avg_winter - 3_000_000:
        preis_winter_delta =  -35
    elif simulation_uebernachtungen_winter < avg_winter - 2_000_000:
        preis_winter_delta = -25
    elif simulation_uebernachtungen_winter < avg_winter - 1_000_000:
        preis_winter_delta = -15
    elif simulation_uebernachtungen_winter > avg_winter + 3_000_000:
        preis_winter_delta = 35
    elif simulation_uebernachtungen_winter > avg_winter + 2_000_000:
        preis_winter_delta = 25
    elif simulation_uebernachtungen_winter > avg_winter + 1_000_000:
        preis_winter_delta = 15
    preis_winter = preis_winter + preis_winter_delta
    preis_winter_array.append(preis_winter)
    preis_winter = winter_preis

    # Sommer
    if simulation_uebernachtungen_sommer < avg_sommer - 3_000_000:
        preis_sommer_delta = -35
    elif simulation_uebernachtungen_sommer < avg_sommer - 2_000_000:
        preis_sommer_delta = -25
    elif simulation_uebernachtungen_sommer < avg_sommer - 1_000_000:
        preis_sommer_delta = -15
    elif simulation_uebernachtungen_sommer > avg_sommer + 3_000_000:
        preis_sommer_delta = 35
    elif simulation_uebernachtungen_sommer > avg_sommer + 2_000_000:
        preis_sommer_delta = 25
    elif simulation_uebernachtungen_sommer > avg_sommer + 1_000_000:
        preis_sommer_delta = 15
    preis_sommer = preis_sommer + preis_sommer_delta
    preis_sommer_array.append(preis_sommer)
    preis_sommer = sommer_preis
    

    '''-----------------------------------------Preisanpassung basierend auf der Temperatur-------------------------------------------------------'''


    # Preisänderungen aufgrund von Tauwetter im Winter
    preis_delta_november  = temperature_price_room_influence(simulation_temp_november)
    preis_delta_dezember  = temperature_price_room_influence(simulation_temp_dezember)
    preis_delta_januar  = temperature_price_room_influence(simulation_temp_januar)
    preis_delta_februar  = temperature_price_room_influence(simulation_temp_februar)
    preis_delta_maerz  = temperature_price_room_influence(simulation_temp_maerz)
    preis_delta_april  = temperature_price_room_influence(simulation_temp_april)


    umsatz_november = (betten_belegt_winter*(preis_winter - preis_delta_november)) * 30
    preis_november_array.append(preis_winter - preis_delta_november)
    umsatz_november_array.append(umsatz_november)
    umsatz_november_int = round(np.sum(umsatz_november_array)/monte_carlo,2)

    umsatz_dezember = (betten_belegt_winter*(preis_winter - preis_delta_dezember)) * 31
    umsatz_dezember_array.append(umsatz_dezember)
    umsatz_dezember_int = round(np.sum(umsatz_dezember_array)/monte_carlo,2)

    umsatz_januar = (betten_belegt_winter*(preis_winter - preis_delta_januar)) * 31
    umsatz_januar_array.append(umsatz_januar)
    umsatz_januar_int = round(np.sum(umsatz_januar_array)/monte_carlo,2)

    umsatz_februar = (betten_belegt_winter*(preis_winter - preis_delta_februar)) * 28
    umsatz_februar_array.append(umsatz_februar)
    umsatz_februar_int = round(np.sum(umsatz_februar_array)/monte_carlo,2)

    umsatz_maerz = (betten_belegt_winter*(preis_winter - preis_delta_maerz)) * 31
    umsatz_maerz_array.append(umsatz_maerz)
    umsatz_maerz_int = round(np.sum(umsatz_maerz_array)/monte_carlo,2)

    umsatz_april = (betten_belegt_winter*(preis_winter - preis_delta_april)) * 30
    umsatz_april_array.append(umsatz_april)
    umsatz_april_int = round(np.sum(umsatz_april_array)/monte_carlo,2)


    # 30 Tage pro Monat für 6 Monate jeweils Sommer und Winter
    umsatz_winter = umsatz_november + umsatz_dezember + umsatz_januar + umsatz_februar + umsatz_maerz + umsatz_april
    umsatz_winter_array.append(umsatz_winter)
    umsatz_sommer = (betten_belegt_sommer * preis_sommer) * 30 * 6
    umsatz_sommer_array.append(umsatz_sommer)

    # Gewinn pro Monat/ Saison berechnen
    gewinn_november = (np.sum(umsatz_november_array)/monte_carlo) * 0.04
    gewinn_dezember = (np.sum(umsatz_dezember_array)/monte_carlo) * 0.04
    gewinn_januar = (np.sum(umsatz_januar_array)/monte_carlo) * 0.04
    gewinn_februar = (np.sum(umsatz_februar_array)/monte_carlo) * 0.04
    gewinn_maerz = (np.sum(umsatz_maerz_array)/monte_carlo) * 0.04
    gewinn_april = (np.sum(umsatz_april_array)/monte_carlo) * 0.04

    gewinn_winter = gewinn_november + gewinn_dezember + gewinn_januar + gewinn_februar + gewinn_maerz + gewinn_april
    gewinn_sommer = (np.sum(umsatz_sommer_array)/monte_carlo) * 0.04

    # Budget Fachkräfte berechnen
    budget_personal_winter = int(umsatz_winter * 0.35)
    budget_personal_winter_array.append(budget_personal_winter)
    budget_personal_sommer = int(umsatz_sommer * 0.35)
    budget_personal_sommer_array.append(budget_personal_sommer)

    # Anzahl Fachkräfte berechnen
    anzahl_fachkraft_winter = int(round(((budget_personal_winter / 6)/preis_fachkraft),0))
    anzahl_fachkraft_winter_array.append(anzahl_fachkraft_winter)
    anzahl_fachkraft_sommer = int(round(((budget_personal_sommer / 6)/preis_fachkraft),0))
    anzahl_fachkraft_sommer_array.append(anzahl_fachkraft_sommer)

    fachkraefte_winter = round(np.sum(anzahl_fachkraft_winter_array)/monte_carlo,0)
    fachkraefte_winter = int(fachkraefte_winter)
    fachkraefte_sommer = round(np.sum(anzahl_fachkraft_sommer_array)/monte_carlo,0)
    fachkraefte_sommer = int(fachkraefte_sommer)


'''-----------------------------------------Ermitteln der Ausgabewerte-------------------------------------------------------'''


# Ausgabe der angepassten Preise
print()
print("Umsatz November: ", umsatz_november_int, "€")
print("Gewinn November: ", round(gewinn_november,2), "€")
print()
print("Umsatz Dezember: ", umsatz_dezember_int, "€")
print("Gewinn Dezember: ", round(gewinn_dezember,2), "€")
print()
print("Umsatz Januar: ", umsatz_januar_int, "€")
print("Gewinn Januar: ", round(gewinn_januar,2), "€")
print()
print("Umsatz Februar: ", umsatz_februar_int, "€")
print("Gewinn Februar: ", round(gewinn_februar,2), "€")
print()
print("Umsatz März: ", umsatz_maerz_int, "€")
print("Gewinn März: ", round(gewinn_maerz,2), "€")
print()
print("Umsatz April: ", umsatz_april_int, "€")
print("Gewinn April: ", round(gewinn_april,2), "€")
print()

print("Umsatz Winter gesamt: ", round(np.sum(umsatz_winter_array)/monte_carlo, 2), "€")
print("Gewinn Winter gesamt: ", round(gewinn_winter,2), "€")
print()
print("Umsatz Sommer gesamt: ", round(np.sum(umsatz_sommer_array)/monte_carlo,2), "€")
print("Gewinn Sommer gesamt: ", round(gewinn_sommer,2), "€")
print()

print("Die empfohlene Anzahl Fachkräfte für den Winter: ", fachkraefte_winter)
print("Die empfohlene Anzahl Fachkräfte für den Sommer: ", fachkraefte_sommer)


'''-----------------------------------------Grafische Darstellung der Ausgabewerte-----------------------------------------'''


# Daten für die Monate
monate = ['November', 'Dezember', 'Januar', 'Februar', 'März', 'April']
x = np.arange(len(monate))

# Daten für Umsatz und Gewinn
umsatz = [umsatz_november_int,umsatz_dezember_int,umsatz_januar_int,umsatz_februar_int,umsatz_maerz_int,umsatz_april_int]
gewinn = [gewinn_november,gewinn_dezember,gewinn_januar,gewinn_februar,gewinn_maerz,gewinn_april]

# Breite der Balken definieren
bar_width = 0.45

# Figur erstellen für zwei Subplots nebeneinander
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Umsatz und Gewinn des Hotel Goldener Adler in Tirol in den Wintermonaten - Personalbedarf für Sommersaison und Wintersaison')

# Erster Subplot für Umsatz und Gewinn
ax[0].bar(x - bar_width/2, umsatz, bar_width, label='Umsatz')
ax[0].bar(x + bar_width/2, gewinn, bar_width, label='Gewinn')

# Titel und Beschriftungen
ax[0].set_title('Umsatz und Gewinn pro Monat')
ax[0].set_xlabel('Monat')
ax[0].set_ylabel('Betrag in €')
ax[0].legend()

# Beschriftung und Position der x-Achse
ax[0].set_xticks(x)
ax[0].set_xticklabels(monate)

# Daten für die Jahreszeiten
jahreszeiten = ['Winter', 'Sommer']

# Daten für die Anzahl der Fachkräfte
fachkraefte = [fachkraefte_winter, fachkraefte_sommer]

# Zweiter Subplot für Anzahl der Fachkräfte
ax[1].bar(jahreszeiten, fachkraefte, color=['blue', 'orange'])

ax[1].set_title('Empfohlene Anzahl Fachkräfte')
ax[1].set_xlabel('Jahreszeit')
ax[1].set_ylabel('Anzahl der Fachkräfte')

# Plot zeigen
plt.tight_layout()
plt.show()