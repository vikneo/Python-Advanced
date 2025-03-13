SELECT c.full_name, m.full_name, purchase_amount, date FROM "order" as o
INNER JOIN customer as c ON c.customer_id = o.customer_id
INNER JOIN manager as m ON m.manager_id = o.manager_id
