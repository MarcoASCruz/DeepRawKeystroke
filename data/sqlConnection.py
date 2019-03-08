import mysql.connector

class SqlConnection:
    def __init__(self, configConnectionDB):
        self.configConnectionDB = configConnectionDB
        self._connection = ""
        self._inTransaction = False

    def getConnection(self):
        return self._connection

    def getCursor(self):
        return self._connection.cursor()

    def getTransactionStatus(self):
        return self._inTransaction

    def beginTransaction(self):
        if self.getTransactionStatus() == False:
            self.open()
            self._connection.start_transaction()
            self._inTransaction = True

    def closeTransaction(self):
        if self.getTransactionStatus():
            self.commit()
            self._inTransaction = False

    def open(self):
        self._connection = mysql.connector.connect(**self.configConnectionDB)

    def select(self, query, callbackSerielizer, parameters = {}):
        models = []
        cursor = self._connection.cursor()
        cursor.execute(query, parameters)
        models = callbackSerielizer(cursor)
        cursor.close()
        return models

    def execute(self, sqlCommand, parameters):
        cursor = self.getCursor()
        cursor.execute(sqlCommand, parameters)
        self.commit()
        lastId = cursor.lastrowid
        cursor.close()
        return lastId

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()