SELECT GovernmentForm, sum_p FROM(
	SELECT MAX(sum_p) AS sum_p, GovernmentForm FROM( 
		SELECT SUM(Population)AS sum_p, GovernmentForm FROM Country
		GROUP BY GovernmentForm));