from config import user, host, db_name, password
import pymysql, cryptography


class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
        )
        self.cursor = self.connection.cursor()

    def select_all_users(self):
        self.__init__()

        select = f'SELECT user_id FROM users;'
        self.cursor.execute(select)

        info = self.cursor.fetchall()

        list_user = []

        if info != ():
            for i in info:
                list_user.append(i[0])

        return list_user

    def add_user(self, name, user_id):
        self.__init__()

        insert_into = f'INSERT INTO `users` (name, user_id) VALUES ("{name}", "{user_id}");'

        self.cursor.execute(insert_into)
        self.connection.commit()

    def select_thread_id(self, user_id):
        self.__init__()

        select = f'SELECT thread_id FROM `users` WHERE user_id = "{user_id}";'
        self.cursor.execute(select)

        order_id = self.cursor.fetchall()[0][0]

        return order_id

    def update_thread_id(self, user_id, thread):
        self.__init__()

        update = f'UPDATE `users` SET thread_id = "{thread}" WHERE user_id = {user_id};'
        self.cursor.execute(update)

        self.connection.commit()

    def select_usage(self, user_id):
        self.__init__()

        select = f'SELECT `usage` FROM `users` WHERE user_id = "{user_id}";'
        self.cursor.execute(select)

        usage = self.cursor.fetchall()[0][0]

        return usage

    def update_usage(self, user_id, usage):
        self.__init__()

        update = f'UPDATE `users` SET `usage` = {usage} WHERE user_id = "{user_id}";'
        self.cursor.execute(update)

        self.connection.commit()

    def update_field(self, user_id, field, value):
        self.__init__()

        update = f'UPDATE `users` SET `{field}` = "{value}" WHERE user_id = "{user_id}";'
        self.cursor.execute(update)

        self.connection.commit()

    def select_personal_info(self, user_id):
        self.__init__()

        select = f'SELECT male, name, age, description FROM `users` WHERE user_id = "{user_id}";'
        self.cursor.execute(select)

        order_id = self.cursor.fetchall()[0]

        return order_id

    def update_buying_usage(self, user_id, usage, if_tarif):
        self.__init__()

        update = f'UPDATE `users` SET `usage` = {usage}, `if_tarif` = {if_tarif} WHERE user_id = "{user_id}";'
        self.cursor.execute(update)

        self.connection.commit()

    def select_order_id(self, user_id):
        self.__init__()

        select = f'SELECT order_id FROM `users` WHERE user_id = "{user_id}";'
        self.cursor.execute(select)

        order_id = self.cursor.fetchall()[0][0]

        return order_id

    def update_order_id(self, user_id, order_id):
        self.__init__()

        update = f'UPDATE `users` SET order_id = "{order_id}" WHERE user_id = {user_id};'
        self.cursor.execute(update)

        self.connection.commit()

    def select_users_tarif(self, tarif):
        self.__init__()

        select = f'SELECT user_id FROM `users` WHERE if_tarif = {tarif};'
        self.cursor.execute(select)

        info = self.cursor.fetchall()

        return info
