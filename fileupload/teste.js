const express = require('express');
const multer = require('multer');
const app = express();
const upload = multer({ dest: 'uploads/', limits: { fileSize: 5 * 1024 * 1024 }});

app.post('/upload', upload.single('myFile'), (req, res) => {
  
  const fs = require('fs');

  // Obtém o arquivo enviado pelo usuário
  const file = req.files.uploadedFile;

  // Cria um stream de leitura do arquivo enviado
  const readStream = fs.createReadStream(file.path);

  // Cria um stream de gravação para salvar o arquivo em uma pasta local
  const writeStream = fs.createWriteStream('./' + file.name);

  // Copia o arquivo enviado para a pasta local
  readStream.pipe(writeStream);

  // Manipula o evento de conclusão da cópia do arquivo
  writeStream.on('close', () => {
    // Retorna a resposta para o usuário
    res.status(200).send('Arquivo salvo com sucesso!');
  });

  res.send('Arquivo recebido com sucesso!');
});

