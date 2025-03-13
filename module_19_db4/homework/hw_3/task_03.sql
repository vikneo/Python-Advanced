-- Используя вложенные запросы найдите всех учеников того преподавателя, кто задает самые простые задания 
-- (те задания, где средний бал самый высокий)

-- задание со звездочкой: напишите этот же запрос с использованием одного из join

SELECT full_name as name_students FROM students s
JOIN students_groups sg ON s.group_id = sg.group_id
WHERE sg.teacher_id = 
	(SELECT teacher_id FROM 
		(SELECT a.teacher_id, avg(ag.grade) as avg_grade
			FROM assignments_grades as ag
			JOIN assignments as a ON a.assisgnment_id = ag.assisgnment_id
		GROUP BY ag.assisgnment_id
		ORDER BY avg_grade DESC
	)
);
