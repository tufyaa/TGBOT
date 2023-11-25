import sqlite3 as sq
import random


async def DataBase_User_Jokes():
    global db, cur

    db = sq.connect('JokesFromUsers.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Jokes(id TEXT PRIMARY KEY, user_id TEXT, anec TEXT, likes TEXT, dislikes TEXT)")

    db.commit()


async def add_user_joke(user_id, joke):
    id = cur.execute("SELECT max(id) FROM Jokes").fetchone()
    print(id[0])
    if id[0] == None:
        id = 0
    else:
        id = int(id[0]) + 1
    cur.execute("INSERT INTO Jokes VALUES(?, ?, ?, ?, ?)",
                (id, user_id,  joke, 0, 0))

    db.commit()
    print("add Ujoke commit")


async def delAllJokes(user_id):
    cur.execute(
        "DELETE FROM Jokes WHERE user_id == '{key}' ".format(key=user_id))
    db.commit()
    print("profile was deleted")


async def get_joke_from_user():
    ids = cur.execute("SELECT id FROM Jokes").fetchall()
    lenn = len(ids)
    rand = random.randint(0, lenn - 1)
    id_joke = int(ids[rand][0])
    joooke = cur.execute("SELECT anec FROM Jokes WHERE id == '{key}' ".format(
        key=id_joke)).fetchone()
    Likes, Dislikes = cur.execute("SELECT likes, dislikes FROM Jokes WHERE id == '{key}' ".format(
        key=id_joke)).fetchone()
    print(Likes, Dislikes)

    joooke = joooke[0]
    db.commit()
    return (joooke, rand, Likes, Dislikes)
