from flask import Flask, request, render_template, send_file, Response
import os
import pandas as pd

UPLOAD_FOLDER = 'fileupload/uploads' #caminho da pasta onde salva os arquivos editados
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'} #um array com as extensões de arquivos permitidos
MAX_FILES = 4 #limite de uploads de arquivos

app = Flask(__name__, static_folder='static') #configuração do app e de arquivos estáticos como script em JS e CSS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configurar página instaciada acima usando config.


@app.route('/') #quando estiver com a url vazia direciona para pagina home
def index():
    return render_template('home.html')  # Página de upload


@app.route('/upload', methods=['POST']) #metodo chamado após envio do formulário
def upload(): 
    """
    Esta função lida com uploads e processamento de arquivos. Ele aceita solicitações POST com arquivos anexados e os processa
    com base em sua extensão de arquivo. Os arquivos CSV e XLSX  são lidos em um Pandas DataFrame, edição de dados e são salvos como um novo
    Arquivo sendo XLSX ou CSV. Os DataFrames resultantes são combinados em um único DataFrame, que é salvo como um arquivo CSV. Finalmente, o usuário é
    redirecionado para uma página de download.

    Retorna:
        Se o número de arquivos enviados estiver dentro do limite permitido, a função retornará um download.html renderizado
        modelo. Caso contrário, retorna uma string indicando que o número de arquivos excede o limite.
    """
    uploaded_files = request.files.getlist('arquivo') #variavel recebe do metodo post com id/name arquivo em uma lista.
    processed_files = [] #instancia um array de arquivos processados para tratar depois no combined.xlsx ou .csv
    formato_saida = request.form.get('formatoSaida') #recebe parametro do metodo post o formato da saída escolhido pelo usuário

    if len(uploaded_files) <= MAX_FILES: #verifica se a quantidade de arquivos é menor ou igual à quantidade de arquivos definido logo acima
        combined_df = pd.DataFrame()  # Crie um DataFrame vazio para combinar as planilhas
        FileXlsx = None #criamos uma váriavel nula para utilizar dentro da condição se a plalinha for XLSX
        FileCsv = None  #criamos uma váriavel nula para utilizar dentro da condição se a plalinha for CSV
        for uploaded_file in uploaded_files: #enquanto tiver arquivos feitos uploads ele executa as condições abaixo
            if uploaded_file.filename != '': #se o arquivo não for vazio ele vazio
                file_extension = uploaded_file.filename.split('.')[-1] #ele pega todo conteúdo depois do ponto, o esperado é que seja XLSX ou CSV
                if file_extension in ALLOWED_EXTENSIONS: #verifica se a extensão estiver previamente declarada no array ALLOWED_EXTENSIONS
                    if file_extension in ['csv']:
                        FileCsv = pd.read_csv(uploaded_file) #metodo para varivavel FileCSV receber pandas lendo o CSV e como parametro o arquivo feito upload

                        #Tratamento de dados aqui (Classes de Limpeza, Identificação de erros e concatenação de Colunas)
                        FileCsv['MES_ANIVERSARIO'] = 2

                        #edited_file_name = uploaded_file.filename.replace('.csv', '_Editado.csv')
                        #edited_file_path = os.path.join(app.config['UPLOAD_FOLDER'], edited_file_name)
                        #FileCsv.to_csv(edited_file_path, index=False)
                        #processed_files.append(edited_file_path)
                        
                        #print(FileCsv.head())  # Mostra as primeiras linhas do DataFrame
                        #print(FileCsv.tail())  # Mostra as últimas linhas do DataFrame
                        combined_df = pd.concat([combined_df, FileCsv], ignore_index=True) #concatena o DF existente com DataFrame novo gerado acima

                    elif file_extension in ['xlsx']: 

                        FileXlsx = pd.read_excel(uploaded_file) #metodo verificar se varivavel FileXlsx receber pandas lendo o XLSX e como parametro o arquivo feito upload

                        #Tratamento de dados aqui (Classes de Limpeza, Identificação de erros e concatenação de Colunas)
                        FileXlsx['Mes de Aniversario'] = 3

                        #edited_file_name = uploaded_file.filename.replace('xlsx', '_Editado.xlsx')
                        #edited_file_path = os.path.join(app.config['UPLOAD_FOLDER'], edited_file_name)
                        #FileXlsx.to_excel(edited_file_path, index=False)
                        #processed_files.append(edited_file_path)

                        combined_df = pd.concat([combined_df, FileXlsx], ignore_index=True) #concatena o DF existente com DataFrame novo gerado acima

        if formato_saida == "xlsx": #verifica no form o valor de formato de saída definido pelo usuário
            
            combined_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.xlsx') # Caminho para planilha combinada em formato XLSX no caminho (path) alterando nome do arquivo
            combined_df.to_excel(combined_file_path, index=False) #converte para XLSX
            processed_files.append(combined_file_path) #salva o arquivo convertido

        elif formato_saida == "csv": #verifica no form o valor de formato de saída definido pelo usuário
            
            combined_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.csv')# Caminho para a planilha combinada em formato CSV no caminho (path) alterando nome do arquivo
            combined_df.to_csv(combined_file_path, index=False) #converte para CSV
            processed_files.append(combined_file_path) #salva o arquvio convertido

        return render_template('download.html') #retorna para a página de download

    return 'Número de arquivos excede o limite permitido.' #caso ultrapsse valor de arquivos retorna uma mensagem


"""@app.route('/download')
def download(processed_files):
    if len(processed_files) > 0:
        zip_filename = 'Alteração.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in processed_files:
                zipf.write(file, os.path.basename(file))

        def generate():
            with open(zip_filename, 'rb') as f:
                yield from f.read()
            os.remove(zip_filename)
        
        response = Response(generate(), content_type='application/zip')
        response.headers['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return response
    
    return 'Nenhum arquivo processado para download.'"""

if __name__ == '__main__':
    app.run(debug=True)
