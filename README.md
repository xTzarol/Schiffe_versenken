# Schiffe_versenken
## Ablauf und Nutzen des Projekts

Das Projekt Schiffe_versenken wurde im Rahmen des Softwaretechnikunterrichts erstellt. Es soll die beteiligten Schüler auf den Ablauf einer Programmentwicklung in der Praxis nach iterativer Vorgangsweise vorbereiten. Hauptaugenmerk des Projekts liegt auf der Eigenständigkeit der Schüler. Sie sollen den Programmcode vollständig mithilfe des Internets und anderen Quellen selbst schreiben. Jeden Freitag musste der funktionierende aktuelle Stand des Programms und eine entsprechende Dokumentation vorgestellt werden.

## Kurzbeschreibung

Das Schiffe_versenken Projekt beinhaltet grundlegende Spiellogik des Spieleklassikers Schiffe versenken bzw. Seeschlacht. Dazu kommt die Erweiterung in Form einer Multiplayerfunktionalität, sodass das Spiel innerhalb des gleichen Netzwerks auf zwei verschiedenen Computern gespielt werden kann. Hierfür wurde ein Server eingerichtet. Vor dem Start des Spiels ist es deshalb wichtig, in der [Serverkonfigurationsdatei](https://github.com/xTzarol/Schiffe_versenken/blob/main/serverconfig.ini) die IP Adresse des Hosts vom Server einzutragen. Auch jene Spieler, die keinen Server am Computer laufen haben müssen die IP Adresse des Servers und den entsprechenden Port eintragen.

Dem Nutzer bietet sich nach Ausführung des Programms eine interaktive grafische Oberfläche. Beide Spieler müssen alle eigenen Schiffe setzen, damit das Spiel beginnen kann. Das restliche Spielgeschehen gestaltet sich ganz gleich nach dem gewöhnlichen Ablauf einer Partie Schiffe versenken.

Die Programmierung des Programms erfolgte in Python, sodass ein Python-Interpreter Voraussetzung für ein funktionsfähiges Programm ist. Weiters ist es ebenfalls möglich, das Programm in Dateien mit dem Dateiformat .exe umzuwandeln.

## Verbesserungsmöglichkeiten

- [ ] Aufdecken umliegender Felder bei vollständiger Zerstörung eines Schiffes

- [ ] grafische Aufbereitung

- [ ] erweiterte Multiplayerfunktionalität
