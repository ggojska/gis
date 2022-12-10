select_gas_stations_with_distance = \
"""
SELECT
    gas_stations.id AS gas_stations_id
    , gas_stations.name AS gas_stations_name
    , gas_stations.lat AS gas_stations_lat
    , gas_stations.lon AS gas_stations_lon
    , 2.0 * 6371.0 *
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
    ) AS gas_stations_distance
FROM
    gas_stations
WHERE
    gas_stations_distance < :radius
ORDER BY
    gas_stations_distance
"""
