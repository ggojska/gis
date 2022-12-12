select_gas_stations_with_distance = \
"""
SELECT
    gas_stations.id AS id
    , gas_stations.name AS name
    , gas_stations.lat AS lat
    , gas_stations.lon AS lon
    , ROUND(2.0 * 6371.0 *
    atan2(
        sqrt(
            sin((lat * pi()/180.0 - :lat * pi()/180.0)/2) *
            sin((lat * pi()/180.0 - :lat * pi()/180.0)/2) +
            cos(:lat * pi()/180.0) * cos(lat * pi()/180.0) *
            sin((lon * pi()/180.0 - :lon * pi()/180.0)/2) *
            sin((lon * pi()/180.0 - :lon * pi()/180.0)/2)
        ),
        sqrt(1-
            sin((lat * pi()/180.0 - :lat * pi()/180.0)/2) *
            sin((lat * pi()/180.0 - :lat * pi()/180.0)/2) +
            cos(:lat * pi()/180.0) * cos(lat * pi()/180.0) *
            sin((lon * pi()/180.0 - :lon * pi()/180.0)/2) *
            sin((lon * pi()/180.0 - :lon * pi()/180.0)/2)
        )
    ), 0) AS distance
FROM
    gas_stations
"""