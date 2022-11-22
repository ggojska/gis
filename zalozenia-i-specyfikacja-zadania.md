# Projekt na zaliczenie z przedmiotu Systemy informacji przestrzennych GIS

## Skład osobowy - role w projekcie

**Maciej Pacześny 187229 - kierownik zespołu, programista back-end**
**Grzegorz Gojska 174173 - programista back-end**
**Jakub Konkel 187207 - programista front-end**

## Harmonogram prac

* 27.11.2022 - xx.11.2022
  * TODO
* xx.xx.2022 - xx.xx.2022
  * TODO
* xx.xx.2022 - 24.12.2022
  * Dokończenie zadań z wcześniejszego okresu, które się opóźniły
* 25.12.2022 - 01.01.2023
  * Przerwa
* 02.01.2023 - 08.01.2023
  * Opracowanie w pełni funkcjonalnej wersji
* 09.01.2023 - 21.01.2023
  * Prace końcowe
  * Opracowanie raportu końcowego

## Opis zadania

Zdanie obejmuje stworzenie serwisu, który pokazuje na mapie stacje benzynowe różnych sieci.

Przewidywane przypadki użycia:

* przeglądanie stacji benzynowych na mapie
* podgląd cen dla wybranej stacji benzynowej
* wyszukiwanie stacji benzynowych:
  * według nazwy
  * według ceny
  * według paliwa sprzedawanego na stacji
  * najbliższe w stosunku do danego punktu
  * sortowanie wyników np. po cenie
* wyszukianie "najtańszej" drogi pomiędzy dwoma punktami, tzn. droga która jest najtańsza biorąc pod uwagę spalanie paliwa (podanego przez użytkownika) oraz cenę paliwa na stacjach benzynowych po drodze
* dodawanie ocen i komentarzy do stacji benzynowych (zalogowany użytkownik)
* zapisywanie ustawień swojego samochodu (model, spalanie) (zalogowany użytkownik)

Na realizację zadania składają się:

* strona www (front-end)
* back-end do przetwarzania i odpowiedzi na zapytania ze strony www

Użyte technologie:

* Front-end:
  * HTML, CSS, JS
  * biblioteki/ frameworki specyficzne dla GIS (OpenLayers, KMS)
* Back-end:
  * dowolny serwer WWW
  * Python + Flask
  * baza danych Sqlite

### Specyfikacja wymagań

* Strona www wyświetlana poprawnie na dowolnej, nowoczesnej przeglądarce internetowej
* Strona www dostosowana do wyświetlania na urządzeniach moblinych i komputerach osobistych (responsive web design)
* Strona www wykorzystuje tagi semantyczne HTML5
* Strona www zgodna ze standardami HTML/XHTML, CSS konsorcjum W3
* Back-end stworzony w oparciu o wzorzec MVC
* Bezpieczne uwierzytelnianie użytkownika (oparte na tokenie)
* Ograniczenie liczby nieudanych logowań w czasie
* Hasła użytkowników przechowywane w bazie danych w bezpieczny sposób (hash + salt)
* Baza danych zabezpieczona przed atakami SQL Injection

### Przyjęta metodyka realizacji

Metodyka realizacji projektu będzie bazować na scrumie.

* Spotkanie synchronizacyjne minimum raz w tygodniu
* Zadania dzielimy na możliwe małe fragmenty dostarczające funkcjonalność
* Każdy kawałek kodu musi przejść review, oraz zostać zaakceptowany przez inną osobę
* Po zakończeniu każdego kamienia milowego zespół wspólnie będzie podejmował decyzje o priorytecie kolejnych zadań

### Planowane do użycia narzędzia, w tym do pracy grupowej

* Dowolne środowisko developerske (np. vscode, pycharm)
* Repozytorium git na platformie Gitlab
* Komunikator Discord
