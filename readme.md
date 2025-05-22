<center>

 ![image](https://github.com/user-attachments/assets/a81925ea-0bb9-42c1-9b2b-c5ace954375b)
</center>

# WifiClue - RTU projekts

Precīza atrašanās vieta ir svarīga gan automatizāciju, gan modernās dzīves sastāvdaļa. No Google Maps līdz soļu skaitītājam vai pat pulkstenim, precīzi zināmu atrašanās vietu izmanto modernas ierīces daudzos veidos. Bet kā var laptops vai pat stacionārs dators, bez jebkādas GPS funkcijas zināt kur tas atrodas?

Atbilde ir uztvert ko var redzēt - WiFi. Gandrīz visiem stacionārajiem un pilnīgi visiem laptopiem ir WiFi uztvērējs. Katrs WiFi var strādāt gandrīz kā satelīts - raidot savu MAC identifikatoru un attālumu no ierīces. Skolas vidē kā piemēram RTU tas ir vēl labāk, jo šie wifi punkti ir visos ēkas stūros kā `eduroam` tīkls:

```
> nmcli dev wifi list | grep eduroam
        FC:7F:F1:D0:1D:40  eduroam            Infra  11    130 Mbit/s  69      ▂▄▆_  WPA2 802.1X
        FC:7F:F1:CF:DD:20  eduroam            Infra  6     130 Mbit/s  59      ▂▄▆_  WPA2 802.1X
        FC:7F:F1:CF:D3:B0  eduroam            Infra  108   540 Mbit/s  58      ▂▄▆_  WPA2 802.1X
        FC:7F:F1:D0:21:B0  eduroam            Infra  36    540 Mbit/s  57      ▂▄▆_  WPA2 802.1X
        FC:7F:F1:CF:DD:30  eduroam            Infra  44    540 Mbit/s  57      ▂▄▆_  WPA2 802.1X
        FC:7F:F1:D0:1D:50  eduroam            Infra  116   540 Mbit/s  57      ▂▄▆_  WPA2 802.1X
        FC:7F:F1:D0:0F:40  eduroam            Infra  1     130 Mbit/s  54      ▂▄__  WPA2 802.1X
        FC:7F:F1:CF:68:F0  eduroam            Infra  100   540 Mbit/s  50      ▂▄__  WPA2 802.1X
        FC:7F:F1:D0:19:40  eduroam            Infra  11    130 Mbit/s  49      ▂▄__  WPA2 802.1X
        FC:7F:F1:CF:DC:F0  eduroam            Infra  124   540 Mbit/s  49      ▂▄__  WPA2 802.1X
        FC:7F:F1:D0:21:A0  eduroam            Infra  1     130 Mbit/s  40      ▂▄__  WPA2 802.1X
        FC:7F:F1:D0:0F:50  eduroam            Infra  52    540 Mbit/s  40      ▂▄__  WPA2 802.1X
        FC:7F:F1:D0:19:50  eduroam            Infra  60    540 Mbit/s  39      ▂▄__  WPA2 802.1X
```

Viss kas pietrūkst ir zināt katra punkta aptuveno atrašanās vietu! Projekti kā https://beacondb.net/ apsola šo datubāzi padarīt publisku, bet pagaidām tā vēl nav.
Šī projekta ietvaros mēs apkopojām mazu datubāzi, [wifis.rtu.csv](https://github.com/Edgars-P/WifiClue/blob/main/wifis.rtu.csv), izmantojot https://github.com/mjaakko/NeoStumbler RTU DITEF ēkas ietvaros.

[TODO bilde]

Datubāze tiek apstrādāta programmas sākumā un glabāta atmiņā kā HashTable. Veicot mērījumu no klienta, tiek izmantota izmērītā atrašanās vieta un uztvērēja signāla stiprums lai atrastu uztvērēja aptuvenu atrašanās vietu.

Rezultāts tiek parādīts pārlūka logā izmantojot automatizācijas bibliotēku lai aizpildītu https://geojson.io karti.

## Piemērs

```
Datu bāze apstrādāta!
Importa laiks: 0.03148651123046875 s
>locate scan
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
 - [X] Izveidot labu RTU karti un piemēra mērijumu no tās pašas dienas.
 - [ ] Izmantot pārlūka automatizāciju lai aizpildītu karti

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
