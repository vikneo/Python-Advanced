SELECT c.full_name, o.order_no FROM "order" as o
JOIN customer as c ON c.customer_id = o.customer_id
WHERE o.manager_id IS NULL