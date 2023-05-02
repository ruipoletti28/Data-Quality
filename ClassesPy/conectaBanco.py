import sqlite3

class ConectaBanco:
    def conectarNoBancoBD(self):
        self.connection = sqlite3.connect("tabelaTeste1.db")
        self.cursor = self.connection.cursor()

    def criarTabelaBD(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tabela';")
        tabela_existe = self.cursor.fetchone() is not None
        if tabela_existe:
            print("A tabela já existe no banco de dados.")
        else:
            print("A tabela não existe no banco de dados.")
            self.cursor.execute("CREATE TABLE tabela (name TEXT, species TEXT, tank_number INTEGER)")
            self.connection.commit()

    def inserirDados(self):
        self.cursor.execute("""INSERT INTO tabela (name, species, tank_number ) VALUES ('Sammy', 'shark', 1)""")
        self.cursor.execute("""INSERT INTO tabela (name, species, tank_number ) VALUES ('Le', 'hooker', 1)""")
        self.connection.commit()
    
    def printDados(self):
        self.rows = self.cursor.execute("SELECT name, species, tank_number FROM tabela").fetchall()
        print(self.rows)
    
    def deletarDados(self):
        dado_vazio = "Sammy" #dadoVazio
        dado_vazio = "Le" #dadoVazio

        self.cursor.execute(
        "DELETE FROM tabela WHERE name = ?",(dado_vazio,))
        
        self.cursor.execute(
        "DELETE FROM tabela WHERE name = ?",(dado_vazio,))
        self.connection.commit()

    def totalMudancas(self):
        print(self.connection.total_changes)

    def fecharConexao(self):
        self.cursor.close()
        self.connection.close()
    
        
testInstance = ConectaBanco()
testInstance.conectarNoBancoBD()
testInstance.criarTabelaBD()
testInstance.inserirDados()
testInstance.printDados()
testInstance.deletarDados()
testInstance.printDados()
testInstance.totalMudancas()
testInstance.fecharConexao()



    