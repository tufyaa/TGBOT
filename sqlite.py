import sqlite3 as sq

# создание базы данных юзеров


async def DataBase_start():
    global db, cur

    db = sq.connect('Users.db')
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, photo TEXT, age TEXT, description TEXT, name TEXT)")

    db.commit()
    print("db commit")

# удаление профиля


async def delete_profile(user_id):
    cur.execute(
        "DELETE FROM profile WHERE user_id == '{key}' ".format(key=user_id))
    db.commit()
    print("profile was deleted")

# создание профиля


async def create_profile(user_id):

    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(
        key=user_id)).fetchone()
    WasCreated = False
    if user == None:
        WasCreated = False
    else:
        WasCreated = True
    if not WasCreated:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?)",
                    (user_id, '', '', '', ''))
        db.commit()
        print("create commit")
        WasCreated = False
    else:
        print("u have created profile")
        WasCreated = True
    return WasCreated

# почти создание
# прошлая функция срабатывает при старте боты, чтобы отслеживать создан ли профиль. Если он не создан она создает.
# эта функция добавляет в него все параметры


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET photo = '{}', age = '{}', description = '{}', name = '{}' WHERE user_id == '{}'".format(
            data['photo'], data['age'], data['description'], data['name'], user_id))
        db.commit()

        print("edit commit")
