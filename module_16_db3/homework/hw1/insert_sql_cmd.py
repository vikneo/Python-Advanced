insert_table_director = """
    INSERT INTO 'director' (dir_first_name, dir_last_name) VALUES 
    ('Jon', 'Parker'),
    ('Stiven', 'Spilberg'),
    ('Nikita', 'Michalkov');
"""

insert_table_movie = """
    INSERT INTO 'movie' (mov_title) VALUES 
    ('John Parker'),
    ('Back to the future'),
    ('Back to the future II'),
    ('Back to the future III'),
    ('The eyes are black'),
    ('Relatives');
"""

insert_table_movie_director = """
    INSERT INTO 'movie_director' (dir_id, mov_id) VALUES 
    (1, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 6);
"""

insert_table_actors = """
    INSERT INTO 'actors' (act_first_name, act_lst_name, act_gender) VALUES 
    ('John', 'Parker', 'M'),
    ('Michael Andrew', 'fox', 'M'),
    ('Christopher', 'Lioyd', 'M'),
    ('Lea', 'Thompson', 'W'),
    ('Elena', 'Safronova', 'W'),
    ('Marcello', 'Mastroianni', 'M');
"""

insert_table_actors = """
    INSERT INTO 'movie_cast' (act_id, mov_id, role) VALUES 
    (1, 1, 'primary'),
    (2, 2, 'primary'),
    (2, 3, 'primary'),
    (2, 4, 'primary'),
    (3, 2, 'primary'),
    (3, 3, 'primary'),
    (3, 4, 'primary'),
    (4, 2, 'primary'),
    (4, 3, 'primary'),
    (4, 4, 'primary'),
    (5, 5, 'primary'),
    (6, 5, 'primary');
"""
