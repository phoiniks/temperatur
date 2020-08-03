#!/usr/bin/python3
from os import remove
from os.path import exists
from socket import gethostname
from subprocess import check_output
from sys import argv
from sqlite3 import connect
from time import sleep

if exists("computer.db"):
    remove("computer.db")

con = connect("computer.db")
cur = con.cursor()

tabelle = gethostname()

create = "CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY, temperatur REAL, pwm INTEGER, lokalzeit DATE DEFAULT(DATETIME('NOW', 'LOCALTIME')))".format(tabelle)

cur.execute(create)

insert = "INSERT INTO {} (temperatur, pwm) VALUES(?, ?)".format(tabelle)

# Laufzeit in Minuten als Parameter, z.B.: ./temperatur.py 10 # Programm läuft 10 Minuten
zeit = int(argv[1]) * 60
stunden = zeit / 3600
print("\n" * 60)
print("Laufzeit von {:s}: {:d} Sekunden, also etwa {:.2f} Stunden\n".format(argv[0][2:], zeit, stunden))

countdown = zeit
for s in range(zeit):
    pwm = check_output(["cat", "/sys/devices/pwm-fan/target_pwm"])
    pwm = "{:3d}".format(int(pwm.decode("utf-8")))
    temperatur = check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
    temperatur = "{:.2f}".format(float(temperatur.decode("utf-8")) / 1000)
    print("\r{} Grad Celsius, PWM: {}, noch {} Messungen".format(temperatur, pwm, countdown), end='')
    cur.execute(insert, (temperatur, pwm))
    sleep(1)
    countdown -= 1
    con.commit()

print("\n")
