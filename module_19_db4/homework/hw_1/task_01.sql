-- Узнайте кто из преподавателей задает самые сложные задания.
-- Иначе говоря задания какого преподавателя получают в среднем самые худшие оценки


SELECT round(avg(grade.grade), 2) as avg_grade, t.full_name as teacher_name
FROM assignments_grades grade
       JOIN assignments a ON a.assisgnment_id = grade.assisgnment_id
       JOIN teachers t ON t.teacher_id = a.teacher_id
GROUP BY grade.assisgnment_id
ORDER BY avg_grade
LIMIT 1