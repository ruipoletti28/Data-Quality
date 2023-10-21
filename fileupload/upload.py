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

class DataCleaner:
    def __init__(self, data):
        self.data = data

    def remove_duplicacao(self):
        self.data = self.data.drop_duplicates()

    def remove_linha_vazia(self):
        self.data = self.data.dropna()

    def limpeza_dado(self):
        self.remove_duplicacao()
        self.remove_linha_vazia()

    def get_dados_clean(self):
        return self.data

# Gere uma chave aleatória
def generate_key():
    return Fernet.generate_key()

# Salve a chave em um arquivo para uso posterior
def salvar_key(key, key_file):
    key_path = os.path.join('fileupload/uploads', key_file)
    with open(key_path, 'wb') as keyfile:
        keyfile.write(key)
class DescriptografarArquivo:
    def __init__(self, key, arquivo_criptografado_caminho, local_arquivo_caminho):
        self.key = key
        self.arquivo_criptografado_caminho = arquivo_criptografado_caminho
        self.local_arquivo_caminho = local_arquivo_caminho

    def decrypt_file(self):
        fernet = Fernet(self.key)
        with open(self.arquivo_criptografado_caminho, 'rb') as file:
            criptografado_dado = file.read()
            decrypted_data = fernet.decrypt(criptografado_dado)
        with open(self.local_arquivo_caminho, 'wb') as file:
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
    uploaded_files = request.files.getlist('arquivo')  # variavel recebe do metodo post com id/name arquivo em uma lista.
    # instancia um array de arquivos processados para tratar depois no combined.xlsx ou .csv
    arquivos_processados = []
    # recebe parametro do metodo post o formato da saída escolhido pelo usuário
    formato_saida = request.form.get('formatoSaida')
    # recebe parametro para realizar ou não a criptografia
    criptografia = request.form.get('CriptoSim')

    # verifica se a quantidade de arquivos é menor ou igual à quantidade de arquivos definido logo acima
    if len(uploaded_files) <= MAX_FILES:
        combinado_df = pd.DataFrame()  # Crie um DataFrame vazio para combinar as planilhas
        FileXlsx = None  # criamos uma váriavel nula para utilizar dentro da condição se a plalinha for XLSX
        FileCsv = None  # criamos uma váriavel nula para utilizar dentro da condição se a plalinha for CSV
        for uploaded_file in uploaded_files:  # enquanto tiver arquivos feitos uploads ele executa as condições abaixo
            if uploaded_file.filename != '':  # se o arquivo não for vazio ele vazio
                # ele pega todo conteúdo depois do ponto, o esperado é que seja XLSX ou CSV
                extensao_arquivo = uploaded_file.filename.split('.')[-1]
                # verifica se a extensão estiver previamente declarada no array ALLOWED_EXTENSIONS
                if extensao_arquivo in ALLOWED_EXTENSIONS:
                    if extensao_arquivo in ['csv']:
                        # metodo para varivavel FileCSV receber pandas lendo o CSV e como parametro o arquivo feito upload
                        FileCsv = pd.read_csv(uploaded_file)

                        # Tratamento de dados aqui (Classes de Limpeza, Identificação de erros e concatenação de Colunas)
                        cleaner = DataCleaner(FileCsv)
                        cleaner.limpeza_dado()

                        FileCsv = cleaner.get_dados_clean()
                        
                        # concatena o DF existente com DataFrame novo gerado acima
                        combinado_df = pd.concat([combinado_df, FileCsv], ignore_index=True)

                    elif extensao_arquivo in ['xlsx']:

                        # metodo verificar se varivavel FileXlsx receber pandas lendo o XLSX e como parametro o arquivo feito upload
                        FileXlsx = pd.read_excel(uploaded_file)

                        # Tratamento de dados aqui (Classes de Limpeza, Identificação de erros e concatenação de Colunas)
                        cleaner = DataCleaner(FileXlsx)
                        cleaner.limpeza_dado()

                        FileXlsx = cleaner.get_dados_clean()
                        # concatena o DF existente com DataFrame novo gerado acima
                        combinado_df = pd.concat([combinado_df, FileXlsx], ignore_index=True)

        if formato_saida == "xlsx":  # verifica no form o valor de formato de saída definido pelo usuário
            if criptografia == "CriptoSim":

                key = generate_key()
                salvar_key(key, 'encryption_key.key')

                # Caminho para planilha combinada em formato XLSX no caminho (path) alterando nome do arquivo
                combinado_arquivo_caminho = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.xlsx')
                # converte para XLSX
                combinado_df.to_excel(combinado_arquivo_caminho, index=False)

                # Lê o arquivo combinado em bytes
                with open(combinado_arquivo_caminho, 'rb') as file:
                    data = file.read()

                # Criptografa os dados
                fernet = Fernet(key)
                criptografado_dado = fernet.encrypt(data)

                # Salva o arquivo criptografado
                arquivo_criptografado_caminho = os.path.join(
                    app.config['UPLOAD_FOLDER'], 'criptografado_combinado.xlsx')
                with open(arquivo_criptografado_caminho, 'wb') as file:
                    file.write(criptografado_dado)

                # Adicione o arquivo criptografado
                arquivos_processados.append(arquivo_criptografado_caminho)

                mensagem = key
                return render_template('aviso.html', mensagem=mensagem)

            else:
                # Caminho para planilha combinada em formato XLSX no caminho (path) alterando nome do arquivo
                combinado_arquivo_caminho = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.xlsx')
                # converte para XLSX
                combinado_df.to_excel(combinado_arquivo_caminho, index=False)
                # salva o arquivo convertido
                arquivos_processados.append(combinado_arquivo_caminho)

        elif formato_saida == "csv":  # verifica no form o valor de formato de saída definido pelo usuário
            if criptografia == "CriptoSim":

                key = generate_key()
                salvar_key(key, 'encryption_key.key')

                # Caminho para a planilha combinada em formato CSV no caminho (path) alterando nome do arquivo
                combinado_arquivo_caminho = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.csv')
                # converte para CSV
                combinado_df.to_csv(combinado_arquivo_caminho, index=False)

                # Lê o arquivo combinado em bytes
                with open(combinado_arquivo_caminho, 'rb') as file:
                    data = file.read()

                # Criptografa os dados
                fernet = Fernet(key)
                criptografado_dado = fernet.encrypt(data)

                # Salva o arquivo criptografado
                arquivo_criptografado_caminho = os.path.join(app.config['UPLOAD_FOLDER'], 'criptografado_combinado.csv')
                with open(arquivo_criptografado_caminho, 'wb') as file:
                    file.write(criptografado_dado)

                # Adicione o arquivo criptografado
                arquivos_processados.append(arquivo_criptografado_caminho)
                mensagem = key
                return render_template('aviso.html', mensagem=mensagem)

            else:
                # Caminho para a planilha combinada em formato CSV no caminho (path) alterando nome do arquivo
                combinado_arquivo_caminho = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.csv')
                # converte para CSV
                combinado_df.to_csv(combinado_arquivo_caminho, index=False)
                # salva o arquvio convertido
                arquivos_processados.append(combinado_arquivo_caminho)

        mensagem = "Gerado com sucesso seu arquivo."
        return render_template('aviso.html', mensagem=mensagem)

    # caso ultrapsse valor de arquivos retorna uma mensagem
    notificacao = "Número de arquivos excede o limite permitido."
    return render_template('info.html', notificacao=notificacao)


@app.route('/descriptografar', methods=['POST'])
def descriptografar():
    """
    Descriptografa um arquivo criptografado com base na entrada do usuário.

    A função recebe uma solicitação POST com a entrada do usuário, incluindo a chave de criptografia e o formato de saída desejado.
    Se o formato de saída for xlsx ou csv, a função verifica se o arquivo criptografado existe e o descriptografa usando a chave fornecida.
    Se a descriptografia for bem-sucedida, a função retornará uma mensagem de sucesso ao usuário.
    Caso o arquivo criptografado não seja encontrado, a função retorna uma mensagem de erro ao usuário.

    Retorna:
        Um modelo HTML renderizado com uma mensagem de sucesso ou de erro, dependendo do resultado do processo de descriptografia.
    """
    chave = request.form.get('chave') #varivavel chave recebe parametro do HTML chave
    formato_saida = request.form.get('formatoSaida') #varivavel formato_saida recebe parametro do HTML formatoSaida
    if formato_saida == "xlsx": #se formato XLSX ele pega o caminho variavél do arquivo criptografado com extensão XLSX.
        arquivo_criptografado_caminho = 'fileupload/uploads/criptografado_combinado.xlsx'
        local_arquivo_caminho = 'fileupload/uploads/descriptografado_combinado.xlsx'
        if os.path.exists(arquivo_criptografado_caminho): #verificar se o arquivo definido no caminho acima existe
            descriptografador = DescriptografarArquivo(chave, arquivo_criptografado_caminho, local_arquivo_caminho) #variavel recebe o resultado do método DescriptografarArquivo passando os parametros CHAVE, CAMINHO DE ENTRADA E SAÍDA DO ARQUIVO
            descriptografador.decrypt_file() 
            notificacao = "Arquivo descriptografado com sucesso!"
            return render_template('info.html', notificacao=notificacao) #retorna mensagem no HTML INFO.HTML notificando o sucesso
        notificacao = "Arquivo Não Encontrado, faça upload e criptografe antes, ou selecione extensão do arquivo criptografado" 
        return render_template('info.html', notificacao=notificacao) #caso não encontre o caminho retorna no html INFO.HTML notificando que não foi encontrado o caminho ou arquivo

    elif formato_saida == "csv":
        arquivo_criptografado_caminho = 'fileupload/uploads/criptografado_combinado.csv'
        local_arquivo_caminho = 'fileupload/uploads/descriptografado_combinado.csv'
        if os.path.exists(arquivo_criptografado_caminho):
            descriptografador = DescriptografarArquivo(chave, arquivo_criptografado_caminho, local_arquivo_caminho)
            descriptografador.decrypt_file()
            notificacao = "Arquivo descriptografado com sucesso!"
            return render_template('info.html', notificacao=notificacao)
        notificacao = "Arquivo Não Encontrado, faça upload e criptografe antes, ou selecione extensão do arquivo criptografado"
        return render_template('info.html', notificacao=notificacao)
    notificacao = "Erro, volte do inicio"
    return render_template('info.html', notificacao=notificacao)


if __name__ == '__main__':
    app.run(debug=True)
