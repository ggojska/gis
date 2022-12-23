select_gas_stations_with_distance = \
"""
(SELECT
    gas_stations.id AS id
    , ROUND(2.0 * 6371.0 * 1000 * 
        ASIN(
            SQRT(
                SIN((gas_stations.lat * pi()/180.0 - :lat * pi()/180.0)/2) *
                SIN((gas_stations.lat * pi()/180.0 - :lat * pi()/180.0)/2) +
                COS(:lat * pi()/180.0) * COS(gas_stations.lat * pi()/180.0) *
                SIN((gas_stations.lon * pi()/180.0 - :lon * pi()/180.0)/2) *
                SIN((gas_stations.lon * pi()/180.0 - :lon * pi()/180.0)/2)
            )), 0) AS harvesine
FROM
    gas_stations)
"""