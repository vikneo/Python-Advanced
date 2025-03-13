import os
import logging.config
import sqlite3
from random import randint
from typing import Optional, List

from . import commands_sql as cmd
from .log_config import dict_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

logging.config.dictConfig(dict_config)
logger = logging.getLogger(__name__)

name_db = "hotel.db"
path_name_db = os.path.join(BASE_DIR, name_db)


class HotelBase:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connect = self.__connection()
        self.cursor = self.connect.cursor()

        self.cursor.execute(cmd.exists)
        exists: Optional[tuple[str,]] = self.cursor.fetchone()
        if not exists:
            self.cursor.execute(cmd.create_table)
            logger.info("Table `table_hotel` created successfully")

            self.cursor.executemany(
                cmd.added_data,
                [
                    (randint(1, 10), randint(1, 4), randint(1, 4), randint(1000, 4000))
                    for _ in range(20)
                ]
            )
            logger.info(f"The `table_hotel` table has been successfully filled with hotel rooms")
            self.save()

    def __connection(self) -> sqlite3.Connection:
        with sqlite3.connect(self.name, check_same_thread = False) as connect:
            logger.info("Connection established with the database {}".format(self.name))
            return connect

    def all(self, **kwargs: dict) -> List[dict]:
        if 'booking' in kwargs:
            rooms = self.cursor.execute(cmd.select_by_booking, (kwargs['booking'],))
            logger.info("Data from all available rooms has been received")
        else:
            logger.info("Data from all rooms has been received")
            rooms = self.cursor.execute(cmd.select_all)
        return rooms.fetchall()

    def update(self, **kwargs: dict) -> None:
        self.cursor.execute(cmd.update_room_id, (kwargs['booking'], kwargs['room_id']))
        logger.info(f"Room `ID-{kwargs['room_id']}` has been updated")
        self.save()

    def filter(self, **kwargs: dict) -> List[dict]:
        if 'room_id' in kwargs:
            room = self.cursor.execute(cmd.select_roomId, (kwargs['room_id'],))
            logger.info(f"Room data was received with the ID-{kwargs['room_id']}")
            return room.fetchall()

    def get(self, data: int) -> List[dict]:
        hotels = self.cursor.execute(cmd.select_roomId, (data,))
        logger.info(f"Room data was received with the ID-{data}")
        return hotels.fetchone()

    def create(self, data: dict) -> None:
        self.cursor.execute(
            cmd.added_data,
            (data['floor'], data['beds'], data['guestNum'], data['price']))
        self.save()

    def delete(self, data: str) -> None:
        self.cursor.execute(cmd.delete_roomId, (data,))
        logger.info(f"Room `ID-{data}` has been deleted")
        self.save()

    def save(self) -> None:
        logger.info(f'Saving data to database `table_hotel`')
        self.connect.commit()


object_db = HotelBase(path_name_db)

