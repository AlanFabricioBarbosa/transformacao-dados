# Script de Extração de Dados de PDF

Este script faz **web scraping** na página da ANS para baixar o **Anexo I** em PDF, extrair tabelas contidas nele e salvar os dados em um **arquivo CSV**, que posteriormente é compactado em um **arquivo ZIP**.

---

## Como Funciona?
1. **Acessa a página da ANS** e obtém o link do PDF do Anexo I.
2. **Baixa o arquivo PDF** e o armazena na pasta `pdfs/`.
3. **Extrai tabelas do PDF** e organiza os dados.
4. **Salva os dados** extraídos em um arquivo `CSV`.
5. **Compacta o CSV** em um ZIP chamado `Teste_Alan_Fabricio.zip`.

---

## Criando o `requirements.txt`
Se ainda não criou o `requirements.txt`, execute:
```bash
pip freeze > requirements.txt
```

## Como Executar
### Criar um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate     # No Windows
```

### Rodar o script
```bash
python3 script.py
```

## Explicação do Código

### Baixando o PDF
#### O script acessa a página da ANS, encontra o link do PDF do Anexo I e faz o download para a pasta `pdfs/`.

### Extraindo Dados do PDF
#### O `pdfplumber` é usado para ler o PDF e extrair as tabelas presentes nele.

### Processando os Dados
#### Os dados extraídos são organizados em um `DataFrame` do Pandas, formatados e limpos.

### Salvando em CSV
#### O DataFrame é salvo como um arquivo CSV chamado `anexo_I.csv`.

### Compactando o Arquivo
#### O script cria um ZIP chamado `Teste_Alan_Fabricio.zip`, contendo o arquivo CSV extraído.