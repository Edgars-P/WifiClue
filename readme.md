# WifiClue - RTU projekts

Apstrādā CSV datubāzi eksportētu no NeoStumbler, uztur to optimizētā veidā atmiņā.

Iedot sarakstu ar uztvertiem WiFi AP, programma var atrast uztvērēja ierīces aptuvenu atrašanās vietu.

NeoStumbler CSV formāts:
```csv
timestamp,latitude,longitude,locationAccuracy,altitude,altitudeAccuracy,locationAge,speed,pressure,macAddress,wifiScanAge,signalStrength,ssid
```

## Piemērs

```
Datu bāze apstrādāta!
Importa laiks: 0.03148651123046875 s
>locate scan
locate 57
fc:7f:f1:d0:1d:42 Robotika2025 70
fc:7f:f1:d0:1d:40 eduroam 65
...
fc:7f:f1:d0:0f:53 Robotika2025 34
2a:11:a8:8a:d1:53 DIRECT-AbRTU22-P0027msIL 29
Atrasta atrašanās vieta izmantojot 50 / 57 wifi punktus
(Atveras pārlūks ar karti)
```

## Datu glabāšana

Wifi datubāze tiek glabāta kā hashtable pēc BSSID (MAC adreses). Tas nodrošina ātru pieeju atrast atrašanās vetu saistītu ar wifi no mērijumiem, jo katrs MAC ir unikāls.

Wifi punkti tiek glabāti kā klase WifiObservation. Tā satur visus wifi parametrus, kā arī atrašanās vietu un rādiusu.

Apstrādājot CSV datubāzi programmas sākšanas brīdī, visi wifi punkti tiek ievietoti HashTable. Konfliktu gadījumā tiek izmantota vidējā atrašanās vieta, kā arī tiek palielināts punkta rādiuss līdz tas iekļauj visus punktus.

Veicot skenēšanu vai ar manuālo ievadi iegūtie wifi punkti tiek saglabāti kā `MinimalWifiObservation`. Tā ir virsklase `WifiObservation` kas nosaka tikai wifi parametrus, bet neiekļauj lokāciju jo tā nav zināma.

TODO
 - [X] CLI funkcijas
 - [X] Dabūt wifi sarakstu no datora un atrast loc pēc tā
 - [X] https://geojson.io/ lai skaisti parādītu visus WIFI punktus
 - [ ] Izveidot labu RTU karti un piemēra mērijumu no tās pašas dienas.

Izmantotās bibliotēkas:
 - `typing` - Python tipi lai noķertu kļūdas un palīdzētu hintiem
 - `time` - Vienkāršs benchmark importa un meklēšanas laikiem
 - `json` - Pārvērš pythion objektu JSON struktūrā lai varētu atvērt karti geojson.io vizualizācijām
 - `urllib` - URL enkodēšana geojson.io saprotamā formātā
 - `webbrowser` - Automātiski atver geojson.io lai vizuāli parādītu karti

---

Noslēguma projekts ir jūsu iespēja izmantot jauniegūtās prasmes, lai izstrādātu pilnvērtīgo programmatūru noteikto uzdevuma risināšanai. Projektā jāizmanto zināšanas, kas ir iegūtas kursa laikā, bet projekta uzdevumu jāģenerē jums pašiem. Mēs gribam, lai Jūs izveidotu sistēmu, kas automatizēs kādu no jūsu ikdienas uzdevumiem.

Tā kā programmatūras izstrāde reti kad ir vienas personas darbs, jums tiek dota iespēja sadarboties ar vienu vai diviem kursabiedriem šī gala projekta izstrādes laikā. Protams, tiek sagaidīts, ka katrs students jebkurā šādā grupā vienlīdzīgi piedalās grupas projekta izstrādē. Turklāt tiek sagaidīts, ka divu vai trīs personu grupas projekta apjoms attiecīgi būs divreiz vai trīsreiz lielāks nekā vienas personas projekts.

Uzdevuma skaidrojums

Projekta izstrādes laikā Jums jāizmanto GitHub, kur Jūs publicēsiet ne tikai programmas kodu, bet nepieciešamo programmatūras dokumentāciju.

Izstrādājot projektu Jums ir nepieciešams izveidot README.md datni, kur Jūs (OBLIGĀTI latviešu valodā):

·       detalizēti aprakstīsiet projekta uzdevumu;

·       izskaidrosiet kādas Python bibliotēkas un kāpēc tiek izmantotas projekta izstrādes laikā

·       projekta izstrādes laikā jāizmanto savas definētas datu struktūras

·       aprakstīsies programmatūras izmantošanas metodes

Var pievienot video (saiti uz to), kurā būs parādīts jūsu programmatūras darbībā un rezultāts.

Ja jums nav pieredzes ar Markdown sintaksi, jums varētu būt noderīga GitHub pamatinformācija parrakstīšana un formatēšana.

Standarta programmatūras projekta README faili bieži var sasniegt tūkstošus vai pat desmitiem tūkstošu vārdu. Jūsu failam nav jābūt tik lielam, bet tur ir jābūt vismaz vairākiem simtiem vārdu, kas detalizēti apraksta projektu!

Visas projekta izstrādes izmaiņas tiek uzglabātas GitHub krātuvē, kas ļauj izsekot projekta izstrādes gaitu.
