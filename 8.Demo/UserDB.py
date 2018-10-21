#!/usr/bin/python
import sqlite3
import hashlib

class UserDB():
    def __init__(self):
        conn = sqlite3.connect('user.sqlite')
        print("Opened database successfully")
        c = conn.cursor()
        c.execute('''CREATE TABLE  IF NOT EXISTS UserInfo
               (ID INT PRIMARY KEY     NOT NULL,
               USERNAME           TEXT    NOT NULL,
               PASSWORD           TEXT     NOT NULL);''')
        print("Table created successfully")

        res = c.execute("SELECT COUNT(*) FROM UserInfo")
        info = list()
        for row in res:
            info.append(row)
        self.ID = info[0][0]
        print(self.ID)
        conn.commit()
        conn.close()

    def insert(self, User, Password):
        conn = sqlite3.connect('user.sqlite')
        c = conn.cursor()
        self.ID += 1
        cursor = c.execute("SELECT USERNAME, PASSWORD from UserInfo WHERE \
        USERNAME = ?", (User,))

        pwd = hashlib.md5()
        pwd.update(Password.encode('utf-8'))
        pwd = pwd.hexdigest()

        info = list()
        for row in cursor:
            info.append(row)
        if len(info) == 0: # insert
            c.execute("INSERT INTO UserInfo (ID, USERNAME, PASSWORD) \
              VALUES (?, ?, ?)", (self.ID, User, pwd));
              conn.commit()
              conn.close()
              return True
        else:
            conn.commit()
            conn.close()
            return False
    
    def check(self, User, Password):
        conn = sqlite3.connect('user.sqlite')
        c = conn.cursor()
        cursor = c.execute("SELECT USERNAME, PASSWORD from UserInfo WHERE \
        USERNAME = ?", (User,))
        info = list()
        for row in cursor:
            info.append(row)

        if len(info) == 0:
            conn.commit()
            conn.close()
            return False

        pwd = hashlib.md5()
        pwd.update(Password.encode('utf-8'))
        pwd = pwd.hexdigest()
        if info[0][1] != pwd:
            conn.commit()
            conn.close()
            return False

        conn.commit()
        conn.close()
        return True

if __name__ == '__main__':
    userdb = UserDB()
    userdb.insert('Xavier', '12345678')
    userdb.insert('Eric', '12345678')
    userdb.check('Patrick', '12345678')
    userdb.insert('Patrick', '12345678')
    userdb.check('Patrick', '12345678')
    userdb.check('Patrick', 'abcdefg')

    print('new password')
    userdb.insert('Patrick', 'abcdefg')
    userdb.check('Patrick', '12345678')
    userdb.check('Patrick', 'abcdefg')
