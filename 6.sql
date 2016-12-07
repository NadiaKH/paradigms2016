SELECT  City.Name,
        City.Population AS CityPopulation,
        Country.Population AS CountryPopulation
FROM (City
JOIN Country ON Country.code = City.CountryCode)
ORDER BY City.Population/Country.Population DESC
LIMIT 20;
