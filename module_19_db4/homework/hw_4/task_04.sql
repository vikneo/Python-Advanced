-- Используя вложенные запросы посчитайте среднее, макс и мин количество просроченных заданий для каждого класса.

-- задание со звездочкой: напишите этот же запрос с использованием одного из join

SELECT * FROM (
	SELECT sg.group_id as classes, 
			min(ag.assisgnment_id) as min_expired, 
			max(ag.assisgnment_id) as max_expired, 
			round(avg(ag.assisgnment_id)) as avg_expired 
	FROM students_groups as sg
		JOIN assignments as a ON a.group_id = sg.group_id
		JOIN assignments_grades as ag ON a.assisgnment_id = ag.assisgnment_id
	WHERE a.due_date < ag.date
	GROUP BY sg.group_id
);
