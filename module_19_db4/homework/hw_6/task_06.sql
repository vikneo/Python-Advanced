-- Используя подзапросы, выведите среднюю оценку за те задания,
-- где ученикам нужно было что-то прочитать и выучить.

SELECT round(avg(grade), 2) as avg_grade
FROM assignments_grades as ag
JOIN assignments a on a.assisgnment_id = ag.assisgnment_id
WHERE a.assignment_text LIKE '%выучить%' OR a.assignment_text LIKE '%прочитать%'
