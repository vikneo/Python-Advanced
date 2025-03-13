exists = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_hotels'; 
            """

create_table = """CREATE TABLE `table_hotels` (
                    roomId INTEGER PRIMARY KEY AUTOINCREMENT, 
                    floor INTEGER, 
                    beds INTEGER,
                    guestNum INTEGER,
                    price INTEGER,
                    booking BLOB default TRUE
            )"""

added_data = """
    INSERT INTO `table_hotels` (floor, beds, guestNum, price) VALUES (?, ?, ?, ?)
"""

select_all = """
    SELECT * FROM table_hotels
"""

select_by_booking = """
SELECT * FROM table_hotels WHERE booking=?
"""

select_filter = """
    SELECT * FROM table_hotels WHERE roomId = ?
"""

select_roomId = """
    SELECT * FROM table_hotels WHERE roomId = ?
"""

delete_roomId = """
    DELETE FROM table_hotels WHERE roomId = ?
"""

update_room_id = """
    UPDATE table_hotels SET booking = ? WHERE roomId = ?
"""
