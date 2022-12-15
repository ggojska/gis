select_gas_stations_with_distance = \
"""
SELECT
    *
FROM
    (SELECT
        gas_stations.id AS id
        , gas_stations.name AS name
        , gas_stations.lat AS lat
        , gas_stations.lon AS lon
        , ROUND(2.0 * 6371.0 * 1000 * 
            ASIN(
                SQRT(
                    SIN((gas_stations.lat * pi()/180.0 - :lat * pi()/180.0)/2) *
                    SIN((gas_stations.lat * pi()/180.0 - :lat * pi()/180.0)/2) +
                    COS(:lat * pi()/180.0) * COS(gas_stations.lat * pi()/180.0) *
                    SIN((gas_stations.lon * pi()/180.0 - :lon * pi()/180.0)/2) *
                    SIN((gas_stations.lon * pi()/180.0 - :lon * pi()/180.0)/2)
                )), 0) AS distance
    FROM
        gas_stations)
WHERE
    distance < :radius
ORDER BY
    distance
"""