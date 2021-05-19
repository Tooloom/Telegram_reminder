from masterclass_database import WorkDB
import config


class UsersDB(WorkDB):
    def __init__(self):
        super().__init__(config.USERS_TABLE, config.USERS_TABLE_DATA)

    def new_table(self):
        self._create_table()

    def new_user(self, user_id, user_name=None):
        if user_name is None:
            user_name = user_id
        query = f'INSERT INTO {self.table} SET user_id={user_id}, user_name="{user_name}"'
        self._execute_query_without_return(query)

    def get_users(self):
        query = f'SELECT * FROM {self.table}'
        return self._execute_query_with_return(query)


class UsersNotifications(WorkDB):
    def __init__(self):
        super().__init__(config.USER_NOT, config.USER_NOT_DATA, with_create=False)

    def new_table(self, user_id):
        table_name = f'table_{user_id}'
        self.table = table_name
        self._create_table()

    def new_not(self, user_id, time, notification):
        table_name = f'table_{user_id}'
        self.table = table_name
        query_0 = f'SELECT max(num) FROM {self.table}'
        max_num = self._execute_query_with_return(query_0)[0][0]
        if max_num:
            query = f'INSERT INTO {self.table} SET num={max_num + 1}, time="{time}", notification="{notification}"'
        else:
            query = f'INSERT INTO {self.table} SET num=1, time="{time}", notification="{notification}"'
        self._execute_query_without_return(query)

    def del_not(self, user_id, num):
        table_name = f'table_{user_id}'
        self.table = table_name
        query = f'DELETE FROM {self.table} WHERE num={num}'
        self._execute_query_without_return(query)

    def get_not(self, user_id):
        table_name = f'table_{user_id}'
        self.table = table_name
        query = f'SELECT * FROM {self.table} ORDER BY time'
        return self._execute_query_with_return(query)

    def generic(self, user_id):
        table_name = f'table_{user_id}'
        self.table = table_name
        query = f'SELECT COUNT(*) FROM {self.table}'
        return self._execute_query_with_return(query)

    def not_update(self, user_id):
        table_name = f'table_{user_id}'
        self.table = table_name
        query_1 = f'SET @a:=0'
        query_2 = f'UPDATE {self.table} SET num=@a:=@a+1 WHERE num IS NOT NULL ORDER BY time'
        self._execute_query_without_return(query_1, query_2)

