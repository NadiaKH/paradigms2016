SELECT City.Name FROM City
JOIN Country ON Country.code = City.CountryCode
JOIN Capital ON City.Id = Capital.CityId
WHERE Country.Name LIKE 'Malaysia';
