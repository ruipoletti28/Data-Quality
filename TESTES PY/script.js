function lerArquivo() {
    var arquivo = document.getElementById("arquivo").files[0];
    if (arquivo) {
        var leitor = new FileReader();
        leitor.onload = function(e) {
            var linhas = e.target.result.split("\n");
            var colunas = linhas[0].split(",");
            var celula = linhas[1].split(","); // Lê a segunda linha como exemplo
            var nomeColuna = colunas[1]; // Nome da coluna 2
            var numeroLinha = 2; // Número da linha 2
            var conteudoCelula = celula[1]; // Conteúdo da célula 2,2
            document.getElementById("resultado").innerHTML = "Nome da coluna: " + nomeColuna + "<br>" +
                                                             "Número da linha: " + numeroLinha + "<br>" +
                                                             "Conteúdo da célula: " + conteudoCelula;
        }
        leitor.readAsText(arquivo);
    }
}
