#!/usr/bin/python3
from socket import gethostname
from subprocess import check_output
from sqlite3 import connect
from time import sleep

con = connect("computer.db")
cur = con.cursor()

tabelle = gethostname()

create = "CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY, temperatur REAL, lokalzeit DATE DEFAULT(DATETIME('NOW', 'LOCALTIME')))".format(tabelle)

cur.execute(create)

insert = "INSERT INTO {} (temperatur) VALUES(?)".format(tabelle)

while True:
    temperatur = check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
    temperatur = float("{:2.2f}".format(float(temperatur.decode("utf-8")) / 1000))
    cur.execute(insert, (temperatur,))
    sleep(1)
    con.commit()
