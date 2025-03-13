SELECT 
    c1.full_name as customer_1, 
    c2.full_name as customer_2
FROM customer as c1
JOIN customer as c2 ON c1.customer_id != c2.customer_id
WHERE c1.city = c2.city AND c1.manager_id = c2.manager_id
