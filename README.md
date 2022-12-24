# Projekt z GIS

## Instalacja

Sklonować repozytorium. Zainstalować potrzebne biblioteki:\
```pip install -r requirements.txt```

## Uruchomienie

Aby uruchomić aplikację lokalnie w środowisku deweloperskim należy:

* ustawić wartość zmiennej środowiskowej FLASK_APP na "projekt_gis":\
Windows:\
```set FLASK_APP=projekt_gis```\
Linux:\
```export FLASK_APP=projekt_gis```

* ustawić wartość zmiennej środowiskowej FLASK_CONFIG na "development":\
Windows:\
```set FLASK_CONFIG=development```\
Linux:\
```export FLASK_CONFIG=development```

* przed samym uruchomieniem trzeba stworzyć bazę danych. W tym celu trzeba wykonać polecenie:\
```flask db upgrade```

* żeby wypełnić bazę danych przykładowymi danymi, trzeba uruchomić polecenie:\
```flask import-sample```

* w linii poleceń uruchomić aplikację poleceniem:\
```flask run```
