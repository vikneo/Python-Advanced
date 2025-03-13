SELECT DISTINCT battle FROM outcomes
WHERE ship in (
    SELECT name FROM ships
    WHERE class = 'Kongo'
)