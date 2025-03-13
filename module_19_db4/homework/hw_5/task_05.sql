-- Проанализируйте все группы по следующим критериям: 
-- общее количество учеников, 
-- средняя оценка, 
-- количество учеников, которые не сдали работы, 
-- количество учеников, которые просрочили дедлайн, 
-- количество повторных попыток сдать работу.

SELECT s.group_id as groups, -- ID группы
      count(s.student_id) as total_students, -- общее количество учеников в группе
      (SELECT round(avg(ag.grade), 2) as avg_grade
      FROM students as s2
            LEFT JOIN assignments_grades as ag ON s2.student_id = ag.student_id
      WHERE s2.group_id = sg.group_id) as avg_grade, -- средняя оценка в группе
      (SELECT count(*)
      FROM students as s3
            LEFT JOIN assignments_grades as ag1 ON s3.student_id = ag1.student_id
      WHERE s3.group_id = s.group_id 
            AND ag1.grade_id is NULL) as late_pass_work, -- сколько учеников не сдали работы
      (SELECT count(*)
      FROM students as s4
            JOIN assignments_grades as ag2 ON s4.student_id = ag2.student_id
            JOIN assignments as a ON a.assisgnment_id = ag2.assisgnment_id
      WHERE s4.group_id = s.group_id 
            AND a.due_date < ag2.date) as total_student_overdue, -- кол-во учеников, которые просрочили дедлайн
      (SELECT sum(redue)
      FROM
            (SELECT
                  count(ag3.assisgnment_id) AS redue
            FROM students s5
                  JOIN assignments_grades ag3 ON ag3.student_id = s5.student_id
            WHERE
                  s5.group_id = s.group_id
            GROUP BY s5.student_id
            HAVING
                  redue > 1)
      )  as total_redue -- кол-во повторных попыток сдать работу для группы
FROM students_groups as sg
LEFT JOIN students as s ON s.group_id = sg.group_id
GROUP BY s.group_id;