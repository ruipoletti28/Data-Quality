const express = require('express');
const app = express();
const router = express.Router();

//const fs = require('fs');
//const dir = "C:/Temp/Data Quality"; 
export default function functionB(){
  router.post('/', (req, res, next) => {
    const formidable = require('formidable');
    const fs = require('fs');
    const form = new formidable.IncomingForm();
  
    form.parse(req, (err, fields, files) => {
  
      const path = require('path');
      const oldpath = files.filetoupload.path;
      const newpath = path.join(__dirname, '..', files.filetoupload.name);
      
      fs.renameSync(oldpath, newpath);
      res.send('File uploaded and moved!');
    });
  });
app.use('/api', router);
}

//import retornarDadosPlanilha from './myscript.js';

/*export default function functionB(nomePlanilha){
  var nomePlanilha = nomePlanilha;
  console.log("Tessteeeee " + nomePlanilha);
  return nomePlanilha;
}*/

/*export default function sum(a, b) {
  return a + b;
}*/

