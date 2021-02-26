import datetime
time = datetime.datetime.now()

def log(log=""):
	with open(f"""logs\\{time.strftime("%d")}{time.strftime("%b")}{time.strftime("%Y")}.txt""", "a") as file:
		file.write(log)