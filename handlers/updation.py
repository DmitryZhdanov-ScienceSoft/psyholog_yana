from database import Database


db = Database()


def updation2():
    list_users_subscribe = db.select_users_tarif(1)

    if list_users_subscribe != ():
        for user in list_users_subscribe:
            db.update_usage(user_id=user[0], usage=100)

    list_users_without_subscribe = db.select_users_tarif(0)

    if list_users_without_subscribe != ():
        for user in list_users_without_subscribe:
            db.update_usage(user_id=user[0], usage=20)
