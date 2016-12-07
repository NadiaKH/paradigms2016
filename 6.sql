SELECT  Country.Name,
		Country.Population AS CountryPopulation,
		City.Name,
        City.Population AS CityPopulation,
        City.Population/Country.Population
FROM (City
JOIN Country ON Country.code = City.CountryCode)
ORDER BY City.Population/Country.Population DESC;