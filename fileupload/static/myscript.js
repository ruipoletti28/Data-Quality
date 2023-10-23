const preview = document.querySelector(".visual");
const input = document.querySelector("input");
const CriptoSim = document.querySelectorAll('input[type="checkbox"]');
const selecaoCripto = document.querySelectorAll('input[name="emailNao"]');
const popup = document.querySelector(".popup");
var selecaoFormato = document.getElementById("formatoSaida");
var countArchives = 1;
input.style.opacity = 0;

input.addEventListener("change", updateImageDisplay);

function updateImageDisplay() {
  while (preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  const curFiles = input.files;
  if (curFiles.length === 0) {
    alert("Nenhum arquivo selecionado para upload");
  } else {
    const list = document.createElement("ol");
    preview.appendChild(list);
  }

  for (let i = 0; i < curFiles.length; i++) {
    const file = curFiles[i];
    const listItem = document.createElement("li");
    const para = document.createElement("p");
  
    if (validFileType(file)) {
      switch (getFileExtension(file.name)) {
        case ".csv":
          var leitor = new FileReader();
  
          leitor.onload = function (e) {
            var linhas = e.target.result.split("\n");
            var colunas = linhas[0].split(",");
            var celula = linhas[1].split(","); // Lê a segunda linha como exemplo
            var nomeColuna = colunas[0]; // Nome da coluna 1
            var numeroLinha = 2; // Número da linha 1
            var conteudoCelula = celula[0]; // Conteúdo da célula 1,1
  
            document.getElementById("demo" + countArchives).innerHTML =
              `Arquivo: <strong> ${file.name} n° </strong>` +
              countArchives +
              "<br>" +
              "Nome da coluna: " +
              nomeColuna +
              "<br>" +
              "Linha N°: " +
              numeroLinha +
              "<br>" +
              "Conteúdo da célula: " +
              conteudoCelula;
  
            countArchives++;
          };
  
          leitor.readAsText(file);
          break;
  
        case ".xlsx":
          var reader = new FileReader();
  
          reader.onload = function (e) {
            var data = new Uint8Array(e.target.result);
            var workbook = XLSX.read(data, { type: "array" });
  
            var sheetName = workbook.SheetNames[0];
            var worksheet = workbook.Sheets[sheetName];
  
            var cellAddress = "A2";
            var colAddress = "A1";
            var cell = worksheet[cellAddress];
            var colName = worksheet[colAddress];
            var value = cell ? cell.v : undefined;
            var valueCol = colName ? colName.v : undefined;
  
            document.getElementById("demo" + countArchives).innerHTML =
              `Arquivo: <strong> ${file.name} n° </strong>` +
              countArchives +
              "<br>" +
              " Nome da coluna: " +
              valueCol +
              "<br>" +
              "Linha N°: " +
              cellAddress +
              "<br>" +
              "Conteúdo da célula: " +
              value;
  
            countArchives++;
          };
  
          reader.readAsArrayBuffer(file);
          break;
  
        default:
          para.textContent = `Arquivo ${file.name}: Arquivo não compatível. Selecione um arquivo .xls, .xlsx, .csv.`;
          listItem.appendChild(para);
          break;
      }
    } else {
      para.textContent = `Arquivo ${file.name}: Arquivo não compatível. Selecione um arquivo .xls, .xlsx, .csv.`;
      listItem.appendChild(para);
    }
  }
  
}

const fileTypes = [
  "application/excel", //xls
  "application/vnd.ms-excel", //xls
  "application/msexcel", //xls
  "application/vnd.ms-excel", //xls
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", //xslx
  "text/csv", //csv
  "text/x-comma-separated-values", //csv
  "text/comma-separated-values", //csv
  "application/octet-stream", //csv
  "text/csv", //csv
];

function validFileType(file) {
  return fileTypes.includes(file.type);
}

function getFileExtension(filename) {
  return filename.slice(((filename.lastIndexOf(".") - 1) >>> 0) + 1);
}

function returnFileSize(number) {
  if (number < 1024) {
    return number + " bytes";
  } else if (number > 1024 && number < 1048576) {
    return (number / 1024).toFixed(1) + " KB";
  } else if (number > 1048576) {
    return (number / 1048576).toFixed(1) + " MB";
  }
}

CriptoSim.forEach((radio) => {
  radio.addEventListener("click", () => {
    if (radio.checked) {
      alert(
        "O arquivo será criptografado!\nA chave será gerada ao fim do processo."
      );
    } else {
      popup.style.display = "none";
    }
  });
});
