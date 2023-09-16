import datetime

def info(message):
	print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [INFO] {message}")