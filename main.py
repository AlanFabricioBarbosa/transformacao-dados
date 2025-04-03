import requests
from bs4 import BeautifulSoup
import os
import zipfile
import pdfplumber
import pandas as pd

URL_SITE = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
PASTA_PDFS = "pdfs"
PDF_ANEXO_I = os.path.join(PASTA_PDFS, "Anexo_I.pdf")
CSV_SAIDA = "anexo_I.csv"
ZIP_SAIDA = "Teste_Alan_Fabricio.zip"

def baixar_pdf():
   response = requests.get(URL_SITE)
   if response.status_code != 200:
      print("Erro ao acessar a página.")
      return False

   soup = BeautifulSoup(response.text, 'html.parser')
   links = soup.find_all('a')

   for link in links:
      href = link.get('href')
      if href and 'Anexo_I' in href and href.lower().endswith('.pdf'):
         url_pdf = href if href.startswith("http") else f"https://www.gov.br{href}"
         break
   else:
      print("PDF do Anexo I não encontrado.")
      return False

   os.makedirs(PASTA_PDFS, exist_ok=True)

   print(f"Baixando {PDF_ANEXO_I}...")
   pdf_response = requests.get(url_pdf)
   with open(PDF_ANEXO_I, "wb") as f:
      f.write(pdf_response.content)

   return True

def extrair_tabela_pdf():
   dados = []
   
   with pdfplumber.open(PDF_ANEXO_I) as pdf:
      for pagina in pdf.pages:
         tabelas = pagina.extract_tables()
         for tabela in tabelas:
            for linha in tabela:
               dados.append(linha)

   if not dados:
      print("Nenhuma tabela foi extraída do PDF.")
      return None

   return processar_dados(dados)

def processar_dados(dados):
   df = pd.DataFrame(dados)

   if df.empty:
      return None

   df.columns = df.iloc[0]
   df = df[1:].reset_index(drop=True)

   df.rename(columns={"OD": "Odontologia", "AMB": "Ambulatorial"}, inplace=True)

   return df

def salvar_csv(df):
   df.to_csv(CSV_SAIDA, index=False, encoding="utf-8")
   print(f"Dados extraídos e salvos em {CSV_SAIDA}")

def compactar_csv():
   with zipfile.ZipFile(ZIP_SAIDA, "w") as zipf:
      zipf.write(CSV_SAIDA, os.path.basename(CSV_SAIDA))
   
   print(f"CSV compactado com sucesso em {ZIP_SAIDA}")

def main():
   if baixar_pdf():
      dados_tabela = extrair_tabela_pdf()

      if dados_tabela is not None and not dados_tabela.empty:
         salvar_csv(dados_tabela)
         compactar_csv()
      else:
         print("Nenhuma informação relevante foi extraída do PDF.")

if __name__ == "__main__":
   main()

