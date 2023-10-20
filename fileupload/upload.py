from flask import Flask, request, render_template
from cryptography.fernet import Fernet
import os
import pandas as pd

# caminho da pasta onde salva os arquivos editados
UPLOAD_FOLDER = 'fileupload/uploads'
# um array com as extensões de arquivos permitidos
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILES = 4  # limite de uploads de arquivos

# configuração do app e de arquivos estáticos como script em JS e CSS
app = Flask(__name__, static_folder='static')
# configurar página instaciada acima usando config.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gere uma chave aleatória


def generate_key():
    return Fernet.generate_key()

# Salve a chave em um arquivo para uso posterior


def save_key(key, key_file):
    key_path = os.path.join('fileupload/uploads', key_file)
    with open(key_path, 'wb') as keyfile:
        keyfile.write(key)


class FileDecryptor:
    def __init__(self, key, encrypted_file_path, output_file_path):
        self.key = key
        self.encrypted_file_path = encrypted_file_path
        self.output_file_path = output_file_path

    def decrypt_file(self):
        fernet = Fernet(self.key)
        with open(self.encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
        with open(self.output_file_path, 'wb') as file:
            file.write(decrypted_data)


@app.route('/')  # quando estiver com a url vazia direciona para pagina home
def index():
    return render_template('home.html')  # Página home


# metodo chamado após envio do formulário
@app.route('/upload', methods=['POST'])
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
    uploaded_files = request.files.getlist(
        'arquivo')  # variavel recebe do metodo post com id/name arquivo em uma lista.
    # instancia um array de arquivos processados para tratar depois no combined.xlsx ou .csv
    processed_files = []
    # recebe parametro do metodo post o formato da saída escolhido pelo usuário
    formato_saida = request.form.get('formatoSaida')
    # recebe parametro para realizar ou não a criptografia
    criptografia = request.form.get('CriptoSim')

    # verifica se a quantidade de arquivos é menor ou igual à quantidade de arquivos definido logo acima
    if len(uploaded_files) <= MAX_FILES:
        combined_df = pd.DataFrame()  # Crie um DataFrame vazio para combinar as planilhas
        FileXlsx = None  # criamos uma váriavel nula para utilizar dentro da condição se a plalinha for XLSX
        FileCsv = None  # criamos uma váriavel nula para utilizar dentro da condição se a plalinha for CSV
        for uploaded_file in uploaded_files:  # enquanto tiver arquivos feitos uploads ele executa as condições abaixo
            if uploaded_file.filename != '':  # se o arquivo não for vazio ele vazio
                # ele pega todo conteúdo depois do ponto, o esperado é que seja XLSX ou CSV
                file_extension = uploaded_file.filename.split('.')[-1]
                # verifica se a extensão estiver previamente declarada no array ALLOWED_EXTENSIONS
                if file_extension in ALLOWED_EXTENSIONS:
                    if file_extension in ['csv']:
                        # metodo para varivavel FileCSV receber pandas lendo o CSV e como parametro o arquivo feito upload
                        FileCsv = pd.read_csv(uploaded_file)

                        # Tratamento de dados aqui (Classes de Limpeza, Identificação de erros e concatenação de Colunas)

                        # print(FileCsv.head())  # Mostra as primeiras linhas do DataFrame
                        # print(FileCsv.tail())  # Mostra as últimas linhas do DataFrame
                        # concatena o DF existente com DataFrame novo gerado acima
                        combined_df = pd.concat(
                            [combined_df, FileCsv], ignore_index=True)

                    elif file_extension in ['xlsx']:

                        # metodo verificar se varivavel FileXlsx receber pandas lendo o XLSX e como parametro o arquivo feito upload
                        FileXlsx = pd.read_excel(uploaded_file)

                        # Tratamento de dados aqui (Classes de Limpeza, Identificação de erros e concatenação de Colunas)

                        # concatena o DF existente com DataFrame novo gerado acima
                        combined_df = pd.concat(
                            [combined_df, FileXlsx], ignore_index=True)

        if formato_saida == "xlsx":  # verifica no form o valor de formato de saída definido pelo usuário
            if criptografia == "CriptoSim":

                key = generate_key()
                save_key(key, 'encryption_key.key')

                # Caminho para planilha combinada em formato XLSX no caminho (path) alterando nome do arquivo
                combined_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'combined.xlsx')
                # converte para XLSX
                combined_df.to_excel(combined_file_path, index=False)

                # Lê o arquivo combinado em bytes
                with open(combined_file_path, 'rb') as file:
                    data = file.read()

                # Criptografa os dados
                fernet = Fernet(key)
                encrypted_data = fernet.encrypt(data)

                # Salva o arquivo criptografado
                encrypted_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'encrypted_combined.xlsx')
                with open(encrypted_file_path, 'wb') as file:
                    file.write(encrypted_data)

                # Adicione o arquivo criptografado
                processed_files.append(encrypted_file_path)

                # Imprima a chave gerada
                # print("Chave de criptografia:", key)

                mensagem = key
                return render_template('aviso.html', mensagem=mensagem)

            else:
                # Caminho para planilha combinada em formato XLSX no caminho (path) alterando nome do arquivo
                combined_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'combined.xlsx')
                # converte para XLSX
                combined_df.to_excel(combined_file_path, index=False)
                # salva o arquivo convertido
                processed_files.append(combined_file_path)

        elif formato_saida == "csv":  # verifica no form o valor de formato de saída definido pelo usuário
            if criptografia == "CriptoSim":

                key = generate_key()
                save_key(key, 'encryption_key.key')

                # Caminho para a planilha combinada em formato CSV no caminho (path) alterando nome do arquivo
                combined_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'combined.csv')
                # converte para CSV
                combined_df.to_csv(combined_file_path, index=False)

                # Lê o arquivo combinado em bytes
                with open(combined_file_path, 'rb') as file:
                    data = file.read()

                # Criptografa os dados
                fernet = Fernet(key)
                encrypted_data = fernet.encrypt(data)

                # Salva o arquivo criptografado
                encrypted_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'encrypted_combined.csv')
                with open(encrypted_file_path, 'wb') as file:
                    file.write(encrypted_data)

                # Adicione o arquivo criptografado
                processed_files.append(encrypted_file_path)
                mensagem = key
                return render_template('aviso.html', mensagem=mensagem)

            else:
                # Caminho para a planilha combinada em formato CSV no caminho (path) alterando nome do arquivo
                combined_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'combined.csv')
                # converte para CSV
                combined_df.to_csv(combined_file_path, index=False)
                # salva o arquvio convertido
                processed_files.append(combined_file_path)

        mensagem = "Gerado com sucesso seu arquivo."
        # retorna para a página de download
        return render_template('aviso.html', mensagem=mensagem)

    # caso ultrapsse valor de arquivos retorna uma mensagem
    return 'Número de arquivos excede o limite permitido.'


@app.route('/descriptografar', methods=['POST'])
def descriptografar():
    chave = request.form.get('chave')
    formato_saida = request.form.get('formatoSaida')
    if formato_saida == "xlsx":
        encrypted_file_path = 'fileupload/uploads/encrypted_combined.xlsx'
        output_file_path = 'fileupload/uploads/decrypted_combined.xlsx'
        if os.path.exists(encrypted_file_path):
            decryptor = FileDecryptor(chave, encrypted_file_path, output_file_path)
            decryptor.decrypt_file()

            notificacao = "Arquivo descriptografado com sucesso!"
            return render_template('info.html', notificacao=notificacao)
        notificacao = "Arquivo Não Encontrado, faça upload e criptografe antes, ou selecione extensão do arquivo criptografado"
        return render_template('info.html', notificacao=notificacao)

    elif formato_saida == "csv":
        encrypted_file_path = 'fileupload/uploads/encrypted_combined.csv'
        output_file_path = 'fileupload/uploads/decrypted_combined.csv'
        if os.path.exists(encrypted_file_path):
            decryptor = FileDecryptor(chave, encrypted_file_path, output_file_path)
            decryptor.decrypt_file()

            notificacao = "Arquivo descriptografado com sucesso!"
            return render_template('info.html', notificacao=notificacao)
        notificacao = "Arquivo Não Encontrado, faça upload e criptografe antes, ou selecione extensão do arquivo criptografado"
        return render_template('info.html', notificacao=notificacao)
    return 'Erro?'

if __name__ == '__main__':
    app.run(debug=True)
