from hw3.connect_to_base import conn_base


def research_income_population(cur) -> None:
    """Research on the income of the population"""

    """
    Выяснить, сколько человек с острова N находятся за чертой бедности, 
    то есть получает меньше 5000 гульденов в год.
    """
    cur.execute("""SELECT COUNT(*) FROM salaries WHERE salary < 5000 """)
    result = cur.fetchone()[0]
    print(f"'{result}' people live below the poverty line")

    """ Посчитать среднюю зарплату по острову N. """
    cur.execute("""SELECT round(AVG(salary), 2) FROM salaries """)
    result = cur.fetchone()[0]
    print(f"The average salary on the island is N '{result}' guilders")

    """ Посчитать медианную зарплату по острову. """
    cur.execute(
        """
        SELECT salary FROM (SELECT row_number() over (ORDER BY salary) as row_num, salary FROM salaries)
        WHERE row_num = (SELECT COUNT(*) / 2 + 1 FROM salaries)
        """
    )
    result = cur.fetchone()[0]
    print(f"The median salary for the island '{result}' guilders")

    """
    Посчитать число социального неравенства F, определяемое как F = T/K, где T — суммарный доход 10%
    самых обеспеченных жителей острова N, K — суммарный доход остальных 90% людей.
    Вывести ответ в процентах с точностью до двух знаков после запятой.
    """
    cur.execute(
        """
        SELECT round(100 * salary_top10 / (SELECT SUM(salary) - salary_top10 FROM salaries), 2)
        FROM (SELECT SUM(top10) as salary_top10
            FROM (SELECT salary as top10 FROM salaries
            ORDER BY salary DESC
            LIMIT round(0.1 * (SELECT COUNT(salary) FROM salaries), 0)))
        """
    )
    result = cur.fetchone()[0]
    print(f"Social inequality number = {result}")


if __name__ == '__main__':
    base_name = 'hw_4_database.db'
    cursor = conn_base(base_name)
    research_income_population(cursor)
