# mymail
Analyzing macOS Mail ~/Library/Mail/ 
## Vorwort
Ausgangspunkt für dieses Projekt war die Feststellung, dass ~/Library/Mail auf meinem Mac auf über 2GB angewachsen war. Dies stand in keinem Verhältnis zu den Größen, die die Provider meiner E-Mail-Accounts anzeigten.

Der Mail-Ordner enthält eines sqlite-Datenbank mit einem Index der empfangenen, gesendeten und noch zu sendenden E-Mails. Die eigentlichen E-Mails sind als eigene emlx-Dateien in einem Verzeichnisbaum gespeichert, der die Mailboxen widerspiegelt.
Der Verzeichnisbaum kann man mit dem Finder oder vom Terminal nach emlx-Files durchsuchen:

```
~/Library/Mail  % print -l ./**/github*/**/*.emlx
./V10/65558C10-7461-424B-B6BE-E42F7A08BF22/github-notifications.mbox/D5FEFD72-E421-4AFA-BF95-F74D5CDA4E45/Data/1/Messages/1925.emlx
./V10/65558C10-7461-424B-B6BE-E42F7A08BF22/github-notifications.mbox/D5FEFD72-E421-4AFA-BF95-F74D5CDA4E45/Data/1/Messages/1926.partial.emlx
```
Die Inhalte der emlx-Files lassen sich im Finder mit Quickview sinnvoll anzeigen und von dort auch mit Mail öffen.

In der sqlite-DB findet man in der Tabelle `messages` den Index. Primary Key ist die beim Insert generierte Rowid und diese wird auch für die Bildung des Namens der emlx-Files verwendet.

Ich fand nun große emlx-Files, die in der Mail-App nicht zu sehen und zu finden waren: Index und Verzeichnisbaum waren offenbar auseinander gelaufen.

In der Folge startete ich dieses Python-Projekt.

## Aufruf der Analyse

1. Es ist eine Terminal-Anwendung,
2. Die Terminal-App braucht **Full Disk Access** für den Zugriff auf den Mail-Ordner.
3. Das Programm ist ein Python Package.

```
repositories/mymail  % python -m mymail -h
```

Das zeigt die Hilfe an:
```
usage: mymail [-h] [-a `account`] [-m `mbox`] [--mi] [--me] [--le [`n`]] [--la [`n`]] [-p id [id ...]] [-v]

Checks macOS Mail database in ~/Library/Mail

 - provides overview of count and sizes of email per mail box,
 - reports emails in database missing corresponding emlx-files,
 - reports emlx-files missing corresponding index in database,
 - reports email attachments downloaded from IMAP-Server

options:
  -h, --help            show this help message and exit
  -a `account`          filter by account.
  -m `mbox`             filter by mbox.
  --mi                  show emlx missing entry in index optionally filtered by mbox.
  --me                  show messages missing emlx-file optionally filtered by mbox
  --le [`n`]            show top largest emlx
  --la [`n`]            show top largest attachments
  -p, --print id [id ...]
                        print individual ids
  -v                    show more detail

Hints:
    - filtering on mbox or account simply uses startswith().
      To filter Mailboxes OUTBOX you can use `--m OU`.

    - Accounts of Mailboxes are UUIDs. This program displays UUIDs truncated
      after 8 Bytes.
```
### Beispiel: Analyse eines Accounts

Option -a ist optional:
```
repositories/mymail  % python -m mymail -a 6555
```

```
 Overview Mailboxes                                       Index   Files  KB %   👹
65558C10/Archive                                            136     136  11.4
65558C10/INBOX                                                0       2   0.5    2
65558C10/Sent Messages                                      222     222   9.6
65558C10/github-notifications                                 2       2   0.1
                                                      𝚺     360     362 19884    6

👹 emlx-Files w/o Index : 6
```

 - Die Spalten *Index* und *Files* zeigen je die Anzahl Messages im Index und im Verzeichnisbaum an. Diese beiden Zahlen sollten übereinstimmen.

 - Die Spalte *KB %* zeigt an, wie hoch der Anteil der Mailbox am Speicherverbrauch aller Mailboxen annimmt. Der Speicherbrauch wird über `du` ermittelt, weil viele elmx-Files COMPRESSED sind; es wird also der physische Speicherverbrauch verwendet, nicht die logische Größe der emlx-Files.

 - Die Monster-Spalte zeigt die Anzahl der Mismatches zwischen Index und Files an.
 - Die Summenzeile zeigt bei *KB %* den Speicherverbrauch alle Mailboxen, also ungefiltert an, ebenso ist dort die Monsterspalte ungefiltert.

### Beispiel: Anzeige der der verwaisten emlx-Files

Mit der Option `-mi` werden die Namen der verwaisten emlx-Files angezeigt. Mit -v werden dazu noch Subject und Sendedatum angezeigt.  
```
repositories/mymail  % python -m mymail -a 6555 --mi -v
``` 

## Wie erfolgt die Bereinigung?

`mymail` ist read-only.

### Offizieller Weg
Wenn man einen Mismatch in einer Mailbox gefunden hat, kann man in der Mail-App

1. die Mailbox markieren
2. im Menu *Mailbox* den Menubefehl *Rebuild* ausführen.

Das hilft in der Regel.

### Etwas härter
Sind dann noch verwaiste emlx-Files übrig, können diese manuell über Finder oder Terminal mit `rm` (oder `trash`) gelöscht werden.

### Ganz radikal
Eine radikale Methode wäre dann noch das Löschen von ~/Library/Mail:

1. Falls vorhanden: Export der lokalen Mailboxen bei `On my Mac` oder der POP-Mailboxes!
2. Rename ~/Library/Mail nach ~/Library/manweisjanie
3. Start der Mail-App. Die baut nun ohne Murren ~/Library/Mail aus den IMAP-Servern wieder auf. Das dauert je nach Datenmenge ein paar Minuten.
4. Wenn im ersten Schritt etwas exportiert wurde, dieses nun wieder importieren. 
