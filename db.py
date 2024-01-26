import sqlite3

class BotDB:
    # название базы напишите сюда
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def check_username(self, user):
        re = self.cursor.execute(f'SELECT EXISTS(SELECT * FROM "tg_bot" WHERE "username"="{user}")')
        if re.fetchone()[0] == False:
            self.cursor.execute(f'INSERT INTO "tg_bot" ("username") VALUES ("{user}")')
            return self.conn.commit()

    def edit_org_car(self, user, org_car):
        self.cursor.execute(f'UPDATE "tg_bot" SET "org_car"="{org_car}" WHERE "username"="{user}"')
        return self.conn.commit()

    def edit_phone_car(self, user, phone_car):
        self.cursor.execute(f'UPDATE "tg_bot" SET "phone_car"="{phone_car}" WHERE "username"="{user}"')
        return self.conn.commit()

    def edit_brand(self, user, brand):
        self.cursor.execute(f'UPDATE "tg_bot" SET "brand"="{brand}" WHERE "username"="{user}"')
        return self.conn.commit()

    def edit_number(self, user, numbers):
        self.cursor.execute(f'UPDATE "tg_bot" SET "numbers"="{numbers}" WHERE "username"="{user}"')
        return self.conn.commit()

    def edit_arrivaldate(self, user, dates):
        self.cursor.execute(f'UPDATE "tg_bot" SET "dates"="{dates}" WHERE "username"="{user}"')
        return self.conn.commit()

    def sends_data(self, user):
        result = self.cursor.execute(f'SELECT * FROM "tg_bot" WHERE "username"="{user}"')
        return result.fetchone()

    def close(self):
        self.connection.close()
