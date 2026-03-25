# mymail
Analyzing macOS Mail ~/Library/Mail/ 
## Vorwort
Ausgangspunkt für dieses Projekt war die Feststellung, dass ~/Library/Mail auf meinem Mac auf über 2GB angewachsen war. Dies stand in keinem Verhältnis zu den Größen, die die Provider meiner E-Mail-Accounts anzeigten.

Der Mail-Ordner enthält eines sqlite-Datenbank mit einem Index der empfangenen, gesendeten und noch zu sendenden E-Mails. Die eigentlichen E-Mails sind als eigene emlx-Dateien in einem Verzeichnisbaum gespeichert, der die Mailboxen widerspiegelt.
Die Verzeichnisbaum kann man mit dem Finder oder vom Terminal nach emlx-Files durchsuchen:

```
~/Library/Mail  % print -l ./**/github*/**/*.emlx
./V10/65558C10-7461-424B-B6BE-E42F7A08BF22/github-notifications.mbox/D5FEFD72-E421-4AFA-BF95-F74D5CDA4E45/Data/1/Messages/1925.emlx
./V10/65558C10-7461-424B-B6BE-E42F7A08BF22/github-notifications.mbox/D5FEFD72-E421-4AFA-BF95-F74D5CDA4E45/Data/1/Messages/1926.partial.emlx
```
Die Inhalte der emlx-Files lassen sich im Finder mit Quickview sinnvoll anzeigen und von dort auch mit Mail öffen.

In der sqlite-DB findet man in der Tabelle `messages` den Index. Primary Key ist die beim Insert generierte Rowid und diese wird auch für die Bildung des Namens der emlx-Files verwendet.

Ich fand nun große emlx-Files, die in der Mail-App nicht zu finden waren: Index und Verzeichnisbaum waren offenbar auseinander gelaufen.

In der Folge startete ich dieses Python-Projekt.

## Aufruf der Analyse

1. Es ist eine Terminal-Anwendung,
2. Die Terminal-App braucht **Full Disk Access** für den Zugriff auf den Mail-Ordner.
3. Das Programm ist ein Python Package.


```
python -m mymail
```

