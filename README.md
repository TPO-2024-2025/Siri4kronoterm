# Namestitev Kontroliranja Toplotne Črpalke preko Home Assistant in Siri

Ta dokument vsebuje navodila za namestitev in uporabo kode za kontroliranje toplotne črpalke preko Home Assistant in Siri glasovnega pomočnika. Sistem deluje preko MQTT Modbus pretvornika, ki povezuje vašo toplotno črpalko z Raspberry Pi 4, na katerem teče Home Assistant.

## Sistemske zahteve

- Raspberry Pi 4 z dostopom do interneta
- Nameščen Home Assistant
- Toplotna črpalka povezana z MQTT Modbus pretvornikom
- iOS naprava za Siri glasovne ukaze

## Postopek namestitve

### 1. Prenos kode iz GitHub repozitorija

1. Obiščite GitHub repozitorij s kodo
2. Prenesite mapo `Koda` kot ZIP datoteko
3. Razširite ZIP datoteko na vašem računalniku

### 2. Namestitev potrebnih integracij v Home Assistant

V Home Assistant je potrebno namestiti naslednje integracije:

1. File Editor
2. MQTT
3. Python Scripts

Za namestitev integracij sledite tem korakom:

1. Odprite Home Assistant v spletnem brskalniku
2. Pojdite na `Nastavitve` (Settings) > `Naprave in storitve` (Devices & Services)
3. V spodnjem desnem kotu kliknite na gumb `Dodaj integracijo` (Add Integration)
4. V iskalnem polju poiščite in namestite vse tri zahtevane integracije:
   - `File Editor`
   - `MQTT`
   - `Python Scripts`
5. Sledite navodilom za nastavitve posameznih integracij

### 3. Kopiranje datotek v Home Assistant

Po namestitvi integracij morate prekopirati datoteke iz prenesene mape `Koda` v vašo Home Assistant instanco:

1. **configuration.yaml**:
   - Odprite Home Assistant File Editor
   - Odprite obstoječo `configuration.yaml` datoteko
   - Kopirajte vsebino nove `configuration.yaml` datoteke iz mape `Koda` v obstoječo datoteko
   - Shranite spremembe

2. **scripts.yaml**:
   - V File Editor poiščite obstoječo `scripts.yaml` datoteko
   - Zamenjajte celotno vsebino z novo datoteko `scripts.yaml` iz mape `Koda`
   - Shranite spremembe

3. **python_scripts**:
   - V File Editor navigirajte do mape, kjer se nahajata `scripts.yaml` in `configuration.yaml`
   - Poiščite ali ustvarite mapo `python_scripts`
   - Kopirajte vse Python skripte iz mape `Koda/python_scripts` v Home Assistant mapo `python_scripts`
   - Shranite spremembe

### 4. Preverjanje konfiguracije in ponovni zagon

Po kopiranju vseh datotek morate preveriti konfiguracijo in ponovno zagnati Home Assistant:

1. Pojdite na `Razvijalska orodja` (Developer Tools) > `Preveri konfiguracijo` (Check Configuration)
2. Kliknite na gumb `Preveri konfiguracijo` (Check Configuration)
3. Če je preverjanje uspešno, kliknite na gumb `Ponovno zaženi` (Restart)
4. Počakajte, da se Home Assistant ponovno zažene (običajno traja nekaj minut)

### 5. Uvoz bližnjic v iOS napravo

Za uporabo Siri glasovnih ukazov morate uvoziti Shortcuts v vašo iOS napravo:

1. Na iOS napravi prenesite Shortcuts iz prenesene mape
2. Odprite aplikacijo Shortcuts
3. Sledite navodilom za uvoz bližnjic
4. Konfigurirajte bližnjice po potrebi, da se povežejo z vašo Home Assistant instanco

## Uporaba

Po uspešni namestitvi lahko uporabljate Siri za kontroliranje toplotne črpalke z glasovnimi ukazi. Na voljo so različne bližnjice, ki omogočajo:

- Spreminjanje temperature
- Preklapljanje med načini delovanja
- Vklop in izklop toplotne črpalke
- Preverjanje stanja toplotne črpalke

## Odpravljanje težav

Če naletite na težave med namestitvijo ali uporabo:

1. Preverite dnevniške zapise v Home Assistant
2. Preverite, ali je MQTT pravilno konfiguriran in povezan s toplotno črpalko
3. Zagotovite, da so vse datoteke pravilno kopirane in shranjene
4. Preverite, ali ima vaša iOS naprava dostop do Home Assistant instance

## Podpora

Za dodatno pomoč obiščite GitHub repozitorij s kodo ali forum Home Assistant skupnosti.
