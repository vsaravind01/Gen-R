import sqlite3
import datetime
import logger
import csv
from os import path, mkdir


def backup():
    if not path.isdir(".\\DB-Backup"):
        mkdir(".\\DB-Backup")
    connection = sqlite3.connect(f"DB-Backup\\RG-Backup.db")
    logger.log(
        log=f"LOGGED INTO THE DATABASE (DB-Backup/RG-Backup.db) : {datetime.datetime.now()}\n"
    )
    cursor = connection.cursor()
    time = datetime.datetime.now()
    with open("records.csv", "r") as file:
        data = csv.reader(file)
        data = next(data)
    subject_1 = data[4]
    subject_2 = data[5]
    subject_3 = data[6]
    subject_4 = data[7]
    subject_5 = data[8]

    cursor.execute(
        f"""
		create Table if not exists "{time.strftime("%d")}{time.strftime("%b")}{time.strftime("%Y")}{time.strftime("%H")}{time.strftime("%M")}{time.strftime("%S")}" (
		name varchar(40),
		class integer(2),
		section char(1),
		admin varchar(8),
		{data[4]} integer(3),
		{data[5]} integer(3),
		{data[6]} integer(3),
		{data[7]} integer(3),
		{data[8]} integer(3))"""
    )
    logger.log(
        log=f"""Table created by the Name : {time.strftime("%d")}{time.strftime("%b")}{time.strftime("%Y")}{time.strftime("%H")}{time.strftime("%M")}{time.strftime("%S")}\n"""
    )
    with open("records.csv", "r") as file:
        values = csv.DictReader(file)
        for value in values:
            cursor.execute(
                f"""insert into "{time.strftime("%d")}{time.strftime("%b")}{time.strftime("%Y")}{time.strftime("%H")}{time.strftime("%M")}{time.strftime("%S")}"
							   (name,class,section,admin,{data[4]},{data[5]},{data[6]},{data[7]},{data[8]})
							   values("{str(value['name'])}",{int(value['class'])},"{str(value['section'])}","{str(value['admin'])}",
							   {int(value[subject_1])},{int(value[subject_2])},{int(value[subject_3])},{int(value[subject_4])},{int(value[subject_5])});"""
            )
    connection.commit()
    connection.close()
    logger.log(
        log=f"""Data successfully uploaded to {time.strftime("%d")}{time.strftime("%b")}{time.strftime("%Y")}{time.strftime("%H")}{time.strftime("%M")}{time.strftime("%S")}\n\n"""
    )


def tableNames():
    connection = sqlite3.connect(f"DB-Backup\\RG-Backup.db")
    logger.log(
        log=f"LOGGED INTO THE DATABASE (DB-Backup/RG-Backup.db) : {datetime.datetime.now()}\n"
    )
    cursor = connection.cursor()
    cursor.execute("select name from sqlite_master where type = 'table';")
    ans = cursor.fetchall()
    print(ans)
    connection.close()

