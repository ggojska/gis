# Projekt na zaliczenie z przedmiotu Systemy informacji przestrzennych GIS

## Raport końcowy

## Skład osobowy

**Maciej Pacześny 187229**
**Grzegorz Gojska 174173* **
**Jakub Konkel 187207* **

* Jakub i Grzegorz byli odpowiedzialni za implementację algorytmu wyszukwiania "najtańszej" drogi.

## Wstęp

Projekt obejmował stworzenie serwisu, który pokazuje na mapie stacje benzynowych różnych sieci, z funkcjonalnością m.in. przeglądania stacji na mapie, wyszukiwania stacji według różnych kryteriów, dodawanie ocen i/lub komentarzy do stacji.

### Zaimplementowane przypadki użycia wraz z krótkim opisem

Zrealizowano następujące przypadki użycia:

* przeglądanie stacji benzynowych na mapie

Markery odpowiadające stacjom benzynowym pojawiają się przy odpowiednim zbliżeniu mapy, i aktualizują się w trakcie przesuwania mapy. Po oddaleniu markery znikają.

* podgląd cen dla wybranej stacji benzynowej

Można najechać kursorem na marker odpowiadający stacji benzynowej, żeby zobaczyć skrócony opis dla danej stacji: nazwę, ceny paliw oraz średnią ocenę użytkowników.

* wyszukiwanie stacji benzynowych:
  * według nazwy
  * według ceny
  * według paliwa sprzedawanego na stacji
  * najbliższe w stosunku do danego punktu
  * sortowanie wyników np. po cenie

Istnieją dwa sposoby wyszukiwania: prosty i zaawansowany. Prosty sposób pozwala na wyszukanie stacji po nazwie stacji i zwraca jedynie markery na mapie, bez listy wyszukanych stacji. Wyszukiwanie proste obejmuje tylko widoczny obszar + niewielki margines. Jeżeli wyszukiwanie jest aktywne, wtedy oddalanie/ przybliżanie mapy nie wpływa na znaczniki stacji na mapie.

Przy wyszukiwaniu zaawansowanym można wyszukać po nazwie, cenie wybranego paliwa oraz średniej ocenie stacji benzynowej. Wyniki są zwrócone jako markery na mapie oraz jako lista z prawej strony ekranu. Zarówno na liście, jak i na mapie zawartych jest co najwyżej 100 pierwszych wyników. Lista zawiera skrócone informacje o stacji: nazwę stacji, średnią ocenę, odległość od środka mapy w momencie wyszukiwania oraz cenę paliwa (jeżeli typ paliwa był podany jako parametr wyszukiwania). Lista umożliwa również sortowanie po cenie, odległości oraz średniej ocenie. Na kolejne strony wyników można przechodzić kilkając odpowiednie odnośniki - spowoduje to nie tylko pojawienie się kolejnych wyników na liście, ale również odpowiadających im markerów na mapie. Wyszukiwanie zaawansowane wyszukuje w dużo większym obszarze, niż jest widoczny.

* dodawanie ocen i komentarzy do stacji benzynowych (zalogowany użytkownik)

Zalogowany użytkownik może dodać ocenę i/lub komentarz do wybranej stacji benzynowej. Po kliknięciu na marker stacji pojawia się okno komentarzy, gdzie można dodać komentarz i/lub ocenę - jedno z dwóch nie może być puste. Użytkownik może usunąć komentarz dodany przez siebie. W oknie komentarzy można przeglądać również komentarze i oceny innych użytkowników.

* zapisywanie danych o swoim samochodzie (model, spalanie) (zalogowany użytkownik)

Zalogowany użytkownik na swoim koncie może dodawać dane o swoich samochodach: markę, model, typ paliwa oraz spalanie. Użytkownik może również usuwać dane o swoich samochodach.

### Techniczna realizacja projektu

Na projekt składają się: strona www (front-end) oraz back-end do przetwarzania i odpowiedzi na zapytania ze strony www. Front-end został zrealizowany z wykorzystaniem HTML, CSS i JavaScript, bez żadnych dodatkowych bibliotek, z wyjątkiem biblioteki JavaScript i CSS OpenLayers. Back-end został zrealizowany w Pythonie z użyciem frameworka webowego Flask. Jako bazę danych wykorzystano Sqlite, a do komunikacji z bazą użyto frameworka ORM SqlAlchemy.

Back-end zrealizowano według wzorca MVC, ale z nieco odmienną terminologią, przyjętą we frameworku Flask - Model-View-Template:

* **model** - model to klasa reprezentująca pewien byt w domenie biznesowej. W tym projekcie domeną są stacje benzynowe, a modelami: użytkownik, stacja benzynowa, paliwo z ceną, komentarz z oceną. Jest to główna jednostka informacji w projekcie. Odpowiada modelowi z MVC.
* **view** - tutaj trafiają żądania użytkownika. Widok odpowiada za przetwarzanie i odpowiedź na żądania użytkownika. W toku przetwarzania pobiera model i przekazuje pobrany model do szablonu (template), żeby wyrenderować odpowiedź - jeżeli odpowiedź powinna zostać zwrócona jako strona HTML. Niekiedy widoki używają również formularzy - są to klasy służące do opisania formularzy wykorzystwanych na stronie do wprowadzenia danych. Odpowiadają za logikę formularza - m.in. za jego walidację. Formularze przekazane do szablonu renderowane są jako formularze HTML. W tym projekcie zaimplementowano również niewielkie REST API, które zwraca odpowiedź w formacie JSON, w takim przypadku szablon nie jest renderowany. Widok jest odpowiednikiem kontrolera z MVC.
* **template** - szablon strony HTML, ta część wzorca jest odpowiedzialna za renderowanie stron WWW z wykorzystaniem szablonów oraz przekazanych przez kontroler danych, i zwrócenie wyrenderowanego szablonu. Jest to odpowiednik widoku z MVC.

Wzorzec MVC został użyty tutaj jako wzorzec architektoniczny, ponieważ definiuję architekturę projektu. Oprócz tego wzorca nie wykorzystano innych wzorców projektowych lub architektonicnych.

### Użyte rozwiązania geoprzestrzenne

Wykorzystano...

* wyznaczanie punktu na mapie ze współrzednych geograficznych
* umieszczanie markerów na mapie
* markery interaktywne - po najechaniu na marker pojawia się popup, po kliknięciu pojawia się okienko
* obliczanie promienia w metrach dla aktualnego przybliżenia mapy - szerokość mapy i jakieś obliczenia

Pewnym problemem okazała się baza danych i obliczanie odległości pomiędzy dwoma punktami współrzędnych. Baza Sqlite nie zawiera żadnych funkcji geoprzestrzennych, a pisanie własnych funkcji do bazy jest trudne, ponieważ wymaga napisania własnego rozszerzenia do Sqlite z wykorzystaniem interfejsu bazy. Sama baza nie wspiera pisania funkcji w wysokopozmowym języku proceduralnym opartym o SQL, jak np. Oracle PL-SQL czy SqlServer T-SQL. Ostatecznie obliczanie odległości zrealizowano w czystym SQL, z wykorzystaniem wzoru Harvesine. W aplikacji obliczanie odległości wykorzystywane jest do wyznaczania, które stacje benzynowe znajdują się w promieniu N metrów od podanego punktu.

### Realizacja wymagań

W projekcie postawiono i zrealizowano następujące wymagania:

* strona www wyświetla się poprawnie na dowolnej, nowoczesnej przeglądarce internetowej na komputerze osobistym (dostosowanie wyglądu do obsługi urządzeń przenośnych nie jest przewidziane)
* strona www zgodna ze standardami HTML/XHTML, CSS konsorcjum W3
* back-end stworzony w oparciu o wzorzec MVC
* hasła użytkowników przechowywane w bazie danych w bezpieczny sposób (hash + salt)
* baza danych zabezpieczona przed atakami SQL Injection
* zróżnicowanie widoku graficznego markera na mapie w zależności sieci, do której należy dana stacja benzynowa

Jedno postawione wymaganie nie zostało zrealizowane:

* bezpieczne uwierzytelnianie użytkownika (oparte na tokenie)

Zamiast uwierzytelniania opartego na tokenie zaimplementowano podstawowe uwierzytelnianie HTTP: po udanym zalogowaniu użytkownik otrzymuje informacje o ID swojej sesji w formie ciastczeka, i w następnych żądaniach do strony posługuje się ID sesji w celu uwierzytelnienia. Uwierzytelnianie oparte na tokenie jest szczególnie użyteczne w przypadku REST API, które nie obsługuje ciasteczek, a informacje uwierzytelniające muszą być przesyłane w każdym żądaniu, o ile dany endpoint API wymaga uwierzytelnienia. W tym projekcie jest tylko jeden endpoint REST API, który służy do pobierania informacji o stacjach benzynowych, i nie wymaga uwierzytlenienia. Z tego powodu nie zaimplementowano uwierzytelniania opartego na tokenie.
