from flask import Flask, request, render_template, send_file
import os
import pyautogui as pag
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')  # Página de upload

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_extension = uploaded_file.filename.split('.')[-1]
        if file_extension in ['csv']:
            df = pd.read_csv(uploaded_file)
            # Processar e editar o DataFrame df conforme necessário
            
            df['MES_ANIVERSARIO'] = 1
            
            # Salvar DataFrame editado em um novo arquivo CSV
            df.to_csv('edited_data.csv', index=False)
            
            return render_template('upload.html')
        
        if file_extension in ['xlsx']:
            df = pd.read_excel(uploaded_file)
            # Processar e editar o DataFrame df conforme necessário

            df['Mes de Aniversario'] = 2

            df.to_excel('data_edited_xslx.xlsx', index=False)

            #pag.alert(text="Hello World", title="The Hello World Box")

            return render_template('upload.html')
    
    return 'Formato de arquivo não suportado.'


@app.route('/download')
def download():
    edited_file_path = 'data_edited_xslx.xlsx'  # Altere o nome do arquivo conforme necessário
    try:
        return send_file(edited_file_path, as_attachment=True)
    finally:
        os.remove(edited_file_path)  # Exclui o arquivo após o download
 

if __name__ == '__main__':
    app.run(debug=True)

