import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    def add_queue(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` (user_id) VALUES (?)", (user_id,))

    def delete_queue(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE user_id = ?", (user_id,))

    def get_queue(self):
        with self.connection:
            queue = self.cursor.execute("SELECT * FROM `queue`").fetchmany(1)

            if bool(len(queue)):
                for row in queue:
                    return row[1]
            else:
                return False

    def create_chat(self, user_id, partner_id):
        if partner_id != 0:
            with self.connection:
                self.cursor.execute("INSERT INTO `chats` (user, partner) VALUES (?, ?)", (user_id, partner_id))
                return True

        return False

    def get_chat(self, user_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE user = ? OR partner = ?", (user_id, user_id))

            for i in chat:
                return [i[0], i[1] if i[1] != user_id else i[2]]

            return False

    def delete_chat(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE user = ? OR partner = ?", (user_id, user_id))
