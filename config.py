token = 'token'

LOGIN = 'User_01'
PASSWORD = '1234'
DB = 'tel_reminder'
HOST = 'localhost'

USERS_TABLE = 'users'

USERS_TABLE_DATA = "("\
    "num int NOT NULL AUTO_INCREMENT, "\
    "user_id int(11) unsigned NOT NULL DEFAULT 0 UNIQUE, "\
    "user_name varchar(256) NOT NULL DEFAULT '', "\
    "PRIMARY KEY (num)"\
    ")"


# ----------------------------------------------------------------------------------------------------------------------
USER_NOT = 'empty'

USER_NOT_DATA = "("\
    "num int NOT NULL DEFAULT 0, "\
    "time DATETIME NOT NULL DEFAULT 0, "\
    "notification varchar(512) NOT NULL DEFAULT ''"\
    ")"
