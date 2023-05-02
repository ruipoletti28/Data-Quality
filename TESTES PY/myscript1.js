import xlsx from 'xlsx/xlsx';

console.log("Hello World");

const xlsx = require('xlsx');

// Lê o arquivo XLSX
const workbook = XLSX.readFile('Presidents.xlsx');

// Seleciona a planilha desejada
const worksheet = workbook.Sheets['Presidents.xlsx'];

// Converte a planilha em um objeto JSON
const data = XLSX.utils.sheet_to_json(worksheet);

// Exibe as informações do objeto JSON