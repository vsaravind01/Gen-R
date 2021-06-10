import datetime
from os import path, mkdir

time = datetime.datetime.now()


def log(log=""):
    if not path.isdir(".\\logs"):
        mkdir(".\\logs")

    with open(
        f"""logs\\{time.strftime("%d")}{time.strftime("%b")}{time.strftime("%Y")}.txt""",
        "a",
    ) as file:
        file.write(log)
