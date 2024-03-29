//import functionB from './ClasseB.js';
//import pegarValorCripto from './criptoPlanilha.js';
//import pegarValorSaida from './saidaPlanilha.js';
const preview = document.querySelector('.visualizacao'); //botão de upload
const input = document.querySelector('input');//input recebe o file, planilha no caso
const CriptoSim = document.querySelectorAll('input[type="checkbox"]'); //checkbox para pop-up do chekbox
const selecaoCripto = document.querySelectorAll('input[name="emailNao"]');//busca o select de saida no html
const popup = document.querySelector('.popup'); //pop-up de arquivo não feito upload
var selecaoFormato = document.getElementById('formatoSaida');//busca o select de saida no html

var countArchives = 0;
input.style.opacity = 0;

input.addEventListener('change', updateImageDisplay);

function updateImageDisplay() {
  
  while(preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  const curFiles = input.files;
  if(curFiles.length === 0) {
    const para = document.createElement('p');
    para.textContent = 'Nenhum arquivo selecionado para upload';
    preview.appendChild(para);
  } else {
    const list = document.createElement('ol');
    preview.appendChild(list);
  }
  for(const file of curFiles) {
      
    const listItem = document.createElement('li');
    const para = document.createElement('p');

    //var nomePlanilha = file.name;
    //var tipoPlanilha = file.type;
    
    

    if(validFileType(file)) {  
      
      //functionB();
      
      saveFile(file);

      switch (getFileExtension(file.name)){

        case '.csv':

        //functionB(nomePlanilha);

          var leitor = new FileReader();

          leitor.onload = function(e) {
            var linhas = e.target.result.split("\n");
            var colunas = linhas[0].split(",");
            var celula = linhas[1].split(","); // Lê a segunda linha como exemplo
            var nomeColuna = colunas[0]; // Nome da coluna 1
            var numeroLinha = 2; // Número da linha 1
            var conteudoCelula = celula[0]; // Conteúdo da célula 1,1 
            document.getElementById( 
              "demo"+countArchives).innerHTML = (`Arquivo: <strong> ${file.name} n° </strong>`
                + countArchives 
                  + "<br>" 
                    + "Nome da coluna: " 
                      + nomeColuna 
                        + "<br>" 
                          + "Linha N°: "
                            + numeroLinha 
                              + "<br>" 
                                + "Conteudo da celula: " 
                                  + conteudoCelula); 
            return {nomeColuna, numeroLinha, conteudoCelula};
          }

          leitor.readAsText(file, function(nomeColuna, numeroLinha, conteudoCelula){
            console.log(nomeColuna, numeroLinha, conteudoCelula);
          });
        break;
        
        case '.xlsx':

        //functionB(nomePlanilha);
          var reader = new FileReader();
          
          reader.onload = function(e) {
            var data = new Uint8Array(e.target.result);
            var workbook = XLSX.read(data, { type: 'array' });
            
            // seleciona a planilha que deseja ler
            var sheetName = workbook.SheetNames[0];
            var worksheet = workbook.Sheets[sheetName];

            // seleciona a coluna e a linha que deseja mostrar
            var cellAddress = 'A2';
            var colAddress = 'A1';
            var cell = worksheet[cellAddress];
            var colName = worksheet[colAddress];
            //var colIndex = cell ? cell.c : undefined; // obtém o índice da coluna
            //var colName = colIndex !== undefined ? XLSX.utils.decode_col(colIndex) : undefined; // decodifica o índice em nome de coluna
            var value = cell ? cell.v : undefined;
            var valueCol = colName ? colName.v : undefined;

            console.log(`O valor da célula ${cellAddress} é ${value} na coluna ${valueCol}`);

            // exibe o valor na tela
            document.getElementById("demo" +countArchives).innerHTML = (`Arquivo: <strong> ${file.name} n° </strong>`
            + countArchives
                + "<br>" 
                  + ' Nome da coluna: '
                    + valueCol 
                      + "<br>" 
                        +'Linha N°: '
                          + cellAddress 
                            + "<br>"
                              + 'Conteudo da celula: ' 
                                + value);
          };
          reader.readAsArrayBuffer(this.files[0]);

        break;

        case false:
          para.textContent = `Arquivo ${file.name}: Arquivo não compatível. Selecione um arquivo .xls, xlsx, .csv.`;
        break;
      
      }

      para.textContent = `Arquivo ${file.name}, tipo ${getFileExtension(file.name)}, tamanho do arquivo ${returnFileSize(file.size)}.`, countArchives++;
      //alert("File: " + file.listItem);
      //console.log(`Arquivo: ${file.name} n°`+ countArchives);

      listItem.appendChild(para);
      returnFileSize(file);
      //returnQntdArchives(file); 
    } else {
      para.textContent = `Arquivo ${file.name}: Arquivo não compatível. Selecione um arquivo .xls, xlsx, .csv.`;
      listItem.appendChild(para);
    }

    //listItem.appendChild(listItem);
  }
}
  /*function retornarDadosPlanilha(nomePlanilha, teste){
    var nomePlanilha = file.name;
    var teste = file.type;
    return nomePlanilha, teste;
  }*/

  function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 1);
  }

  function saveFile(file) {
    const a = document.createElement('a');
    a.setAttribute('download', file.name);
    a.setAttribute('href', `data quality/${file.name}`);
    a.click();
  }  

  selecaoFormato.addEventListener('change', function(valueSaida){
    var valueSaida = selecaoFormato.value;
    pegarValorSaida(valueSaida);
  })

  selecaoCripto.forEach((name) => {
    name.addEventListener('click', () => {
      var valueSaidaCripto = selecaoCripto.name;
      if(name.checked){
        pegarValorCripto(valueSaidaCripto);
      } else {
        console.log("Marque uma opção!");
      }
    })
  });
        
  const fileTypes = [
      "application/excel", //xls
      "application/vnd.ms-excel",//xls
      "application/msexcel",//xls
      "application/vnd.ms-excel", //xls
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", //xslx
      "text/csv", //csv
      "text/x-comma-separated-values",//csv
      "text/comma-separated-values", //csv
      "application/octet-stream", //csv 
      "text/csv", //csv
  ]

  function validFileType(file) {
    //alert("File: " + file.type);
    //alert("Resultado: " + fileTypes.includes(file.type));
    return fileTypes.includes(file.type);
  }

  function returnFileSize(number) {
    if(number < 1024) {
      return number + 'bytes';
    } else if(number > 1024 && number < 1048576) {
      return (number/1024).toFixed(1) + 'KB';
    } else if(number > 1048576) {
      return (number/1048576).toFixed(1) + 'MB';
    }
  }

  CriptoSim.forEach((radio) => {
    radio.addEventListener('click', () => {
      if(radio.checked){
        alert("O arquivo será criptografado! \n A chave será gerada ao fim do processo.");
      } else {
        popup.style.display = 'none';
      }
    })
  });

  window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;

  window.requestFileSystem(window.TEMPORARY, 5 * 1024 * 1024, function(fs) {
    fs.root.getDirectory('"C:/Users/Ubuntu/Downloads/Data Quality"', {create: true}, function(dirEntry) {
      // aqui você pode copiar o arquivo para a pasta de destino
    });
  });


  /*function mostrarValor() {
    const comboBox = document.getElementById("formatoSaida");
    const valorEscolhido = comboBox.value;
    console.log(valorEscolhido);
    alert(valorEscolhido);
  }*/
