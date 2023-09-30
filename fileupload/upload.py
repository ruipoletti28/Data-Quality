from flask import Flask, request, render_template, send_file, Response
import os
import pandas as pd

UPLOAD_FOLDER = 'fileupload/uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILES = 4

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('home.html')  # Página de upload


@app.route('/upload', methods=['POST'])
def upload():
    """
    This function handles file uploads and processing. It accepts POST requests with files attached, and processes them
    based on their file extension. CSV files are read into a Pandas DataFrame, have a column added, and are saved as a new
    CSV file. XLSX files are also read into a Pandas DataFrame, have a column added, and are saved as a new XLSX file.
    The resulting DataFrames are combined into a single DataFrame, which is saved as a CSV file. Finally, the user is
    redirected to a download page.

    Returns:
        If the number of uploaded files is within the allowed limit, the function returns a rendered download.html
        template. Otherwise, it returns a string indicating that the number of files exceeds the limit.
    """
    uploaded_files = request.files.getlist('arquivo')
    processed_files = []
    formato_saida = request.form.get('formatoSaida')

    if len(uploaded_files) <= MAX_FILES:
        combined_df = pd.DataFrame()  # Crie um DataFrame vazio para combinar as planilhas
        FileXlsx = None
        FileCsv = None
        for uploaded_file in uploaded_files:
            if uploaded_file.filename != '':
                file_extension = uploaded_file.filename.split('.')[-1]
                if file_extension in ALLOWED_EXTENSIONS:
                    if file_extension in ['csv']:
                        FileCsv = pd.read_csv(uploaded_file)
                        FileCsv['MES_ANIVERSARIO'] = 2
                        #edited_file_name = uploaded_file.filename.replace('.csv', '_Editado.csv')
                        #edited_file_path = os.path.join(app.config['UPLOAD_FOLDER'], edited_file_name)
                        #FileCsv.to_csv(edited_file_path, index=False)
                        #processed_files.append(edited_file_path)
                        
                        #print(FileCsv.head())  # Mostra as primeiras linhas do DataFrame
                        #print(FileCsv.tail())  # Mostra as últimas linhas do DataFrame
                        combined_df = pd.concat([combined_df, FileCsv], ignore_index=True)

                    elif file_extension in ['xlsx']:

                        FileXlsx = pd.read_excel(uploaded_file)
                        FileXlsx['Mes de Aniversario'] = 3
                        #edited_file_name = uploaded_file.filename.replace('xlsx', '_Editado.xlsx')
                        #edited_file_path = os.path.join(app.config['UPLOAD_FOLDER'], edited_file_name)
                        #FileXlsx.to_excel(edited_file_path, index=False)
                        #processed_files.append(edited_file_path)

                        combined_df = pd.concat([combined_df, FileXlsx], ignore_index=True)

        if formato_saida == "xlsx":
            # Salvar a planilha combinada em formato XLSX
            combined_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.xlsx')
            combined_df.to_excel(combined_file_path, index=False)
            processed_files.append(combined_file_path)
        elif formato_saida == "csv":
            # Salvar a planilha combinada em formato XLSX
            combined_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.csv')
            combined_df.to_csv(combined_file_path, index=False)
            processed_files.append(combined_file_path)

        return render_template('download.html')

    return 'Número de arquivos excede o limite permitido.'


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
