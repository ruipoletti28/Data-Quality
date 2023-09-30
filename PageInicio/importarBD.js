const csv = require('csv-parser');
const xlsx = require('xlsx');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();

//var nomePlanilha = functionB(nomePlanilha);
var nomePlanilha = functionB.nomePlanilha;

console.log("teste " + nomePlanilha);

function csvImport(){
  // Cria uma conexão com o banco de dados
  const db = new sqlite3.Database('./database.db');

  const csvFilePath = './'+ nomePlanilha;

  const tableName = 'tabela';

  //Cria a tabela no banco de dados
  db.run(`CREATE TABLE ${tableName} (name TEXT, birhday INTEGER)`);

// Lê a planilha em formato CSV
fs.createReadStream(csvFilePath)
  .pipe(csv())
  .on('data', (data) => {
    db.run(`INSERT INTO ${tableName} (name, birthday) VALUES (?, ?)`, [data.Name, data.Birthday], (err) => {
      if (err) {
        console.error(err.message);
      }
    });
  })
  .on('end', () => {
    console.log('Dados inseridos com sucesso!');
    // Fecha a conexão com o banco de dados
    db.close();
  });
}

function xlsxImport(){
    // Cria uma conexão com o banco de dados
  const db = new sqlite3.Database('./database1.db');

  // Lê a planilha em formato XLSX
  const workbook = xlsx.readFile('./Presidents.xlsx');

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
}
  
