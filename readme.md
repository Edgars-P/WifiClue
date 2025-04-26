# WifiClue - RTU projekts

Apstrādā CSV datubāzi eksportētu no NeoStumbler, uztur to optimizētā veidā atmiņā.

Iedot sarakstu ar uztvertiem WiFi AP, programma var atrast uztvērēja ierīces aptuvenu atrašanās vietu.

CSV formāts:
```csv
timestamp,latitude,longitude,locationAccuracy,altitude,altitudeAccuracy,locationAge,speed,pressure,macAddress,wifiScanAge,signalStrength,ssid
```

Piemērs:

```
Datu bāze apstrādāta!
> locate 10
>> FC:7F:F1:CF:8B:82  RTU-Guest
>> FC:7F:F1:CF:8B:80  eduroam
>> ...
>> 34:8A:12:6F:F1:F2  RTU-Guest
Lokācija atrasta!
Pos: ...
Acc: 10 m
```

TODO
 - [ ] CLI funkcijas
 - [ ] Dabūt wifi sarakstu no datora un atrast loc pēc tā
 - [ ] https://geojson.io/ lai skaisti parādītu visus WIFI punktus

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
