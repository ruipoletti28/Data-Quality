const xlsx = require('xlsx');
const sqlite3 = require('sqlite3').verbose();

// Cria uma conexão com o banco de dados
const db = new sqlite3.Database('./teste2.db');

// Lê a planilha em formato XLSX
const workbook = xlsx.readFile('C:/Users/Ubuntu/Documents/Data Quality/ClassesJS/Presidents.xlsx');

// Seleciona a primeira planilha do arquivo
const worksheet = workbook.Sheets[workbook.SheetNames[0]];

// Converte a planilha para um array de objetos
const data = xlsx.utils.sheet_to_json(worksheet);

// Insere cada objeto da planilha na tabela
data.forEach((item) => {
  db.run(`INSERT INTO tabela (Name, Birthday) VALUES (?, ?)`, [item.Name, item.Birthday], (err) => {
    if (err) {
      console.error(err.message);
    }
  });
});

console.log('Dados inseridos com sucesso!');
// Fecha a conexão com o banco de dados
db.close();