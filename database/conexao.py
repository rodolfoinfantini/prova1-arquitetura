from interfaces.conexao import IConexao
import sqlite3


class SqliteConexao(IConexao):
    def __init__(self, arquivo: str):
        self.db = sqlite3.connect(arquivo)
        self.cursor = self.db.cursor()

    def get_conexao(self):
        return (self.db, self.cursor)
