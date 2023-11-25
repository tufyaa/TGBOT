import random
from bs4 import BeautifulSoup as BS
import requests
import sqlite3 as sq


url = 'https://www.anekdot.ru/random/anekdot/'


anectodes = []


def DataBase_Jokes():
    global db, cur

    db = sq.connect('JokesFromBot.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Jokes(id TEXT PRIMARY KEY, anec TEXT, likes TEXT, dislikes TEXT)")

    db.commit()


def add_joke(id, joke):
    cur.execute("INSERT INTO Jokes VALUES(?, ?, ?, ?)",
                (id, joke, 0, 0))

    db.commit()


async def get_joke():

    db1 = sq.connect('JokesFromBot.db')
    cur1 = db1.cursor()
    ran = random.randint(0, 1049)
    joooke = cur1.execute("SELECT anec FROM Jokes WHERE id == '{key}'".format(
        key=ran)).fetchone()
    Likes, Dislikes = cur1.execute("SELECT likes, dislikes FROM Jokes WHERE id == '{key}'".format(
        key=ran)).fetchone()
    print(Likes, Dislikes)

    return (str(joooke), ran, Likes, Dislikes)


def parser(url, anec):
    req = requests.get(url)

    soup = BS(req.text, 'html.parser')
    anectemp = soup.find_all('div', class_='text')
    for t in anectemp:
        anec.append(t.text)


def ParsAll(url):
    global anectodes
    for i in range(50):
        parser(url, anectodes)


def start_pars():
    DataBase_Jokes()
    ParsAll(url)
    count = 0
    print("sttr")
    for i in anectodes:
        add_joke(count, i)
        count += 1
