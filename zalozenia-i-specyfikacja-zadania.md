# Projekt na zaliczenie z przedmiotu Systemy informacji przestrzennych GIS

## Skład osobowy - role w projekcie

**Maciej Pacześny 187229 - kierownik zespołu, programista back-end**
**Grzegorz Gojska 174173 - programista back-end**
**Jakub Konkel 187207 - programista front-end**

## Opis zadania

W ogólnym zarysie zdanie obejmuje stworzenie serwisu, który pokazuje na mapie stacje benzynowe różnych sieci.

### Przewidywane przypadki użycia

* przeglądanie stacji benzynowych na mapie
* podgląd cen dla wybranej stacji benzynowej
* wyszukiwanie stacji benzynowych:
  * według nazwy
  * według ceny
  * według paliwa sprzedawanego na stacji
  * najbliższe w stosunku do danego punktu
  * sortowanie wyników np. po cenie
* wyszukianie "najtańszej" drogi pomiędzy dwoma punktami, tzn. droga która jest najtańsza biorąc pod uwagę spalanie paliwa (podanego przez użytkownika) oraz cenę paliwa na stacjach benzynowych po drodze
  * alternatywny przypadek użycia, gdyby powyższy był zbyt trudny do implementacji: wyszukiwanie najkrótszej drogi pomiędzy punktami i podanie całkowitego kosztu przejazdu, uwzględniając cenę paliwa na stacjach na wyszukanej drodze i spalanie samochodu
* dodawanie ocen i komentarzy do stacji benzynowych (zalogowany użytkownik)
* zapisywanie danych o swoim samochodzie (model, spalanie) (zalogowany użytkownik)

Na realizację zadania składają się:

* strona www (front-end)
* back-end do przetwarzania i odpowiedzi na zapytania ze strony www

### Technologie

* front-end:
  * HTML, CSS, JS
  * biblioteki/ frameworki specyficzne dla GIS (OpenLayers)
* back-end:
  * dowolny serwer WWW
  * Python + Flask
  * baza danych Sqlite

### Narzędzia

* dowolne środowisko developerske (np. vscode, pycharm)
* repozytorium git na platformie Gitlab
* komunikator Discord

## Specyfikacja wymagań

* strona www wyświetla się poprawnie na dowolnej, nowoczesnej przeglądarce internetowej na komputerze osobistym (dostosowanie wyglądu do obsługi urządzeń przenośnych nie jest przewidziane)
* strona www zgodna ze standardami HTML/XHTML, CSS konsorcjum W3
* back-end stworzony w oparciu o wzorzec MVC
* bezpieczne uwierzytelnianie użytkownika (oparte na tokenie)
* hasła użytkowników przechowywane w bazie danych w bezpieczny sposób (hash + salt)
* baza danych zabezpieczona przed atakami SQL Injection
