import os
import re
import requests
import shutil
import zipfile
from bs4 import BeautifulSoup
from datetime import date

_PATH = r'C:\banco-de-dados-receita'

def get_link_files(root_url):
    """ Obtém os links dos arquivos ZIP disponíveis na página. """
    response = requests.get(root_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    zip_links = [link.get('href') for link in soup.find_all('a', href=True) if link['href'].endswith('.zip')]

    return zip_links


def download_zip_file(root_url, zip_file):
    """ Faz o download de um arquivo ZIP e salva localmente. """
    
    # Verifica e cria a pasta se necessário
    if not os.path.exists(_PATH):
        print(f"📁 Criando pasta: {_PATH}")
        os.makedirs(_PATH, exist_ok=True)
    else:
        print(f"📁 Pasta já existe: {_PATH}")

    local_zip_path = os.path.join(_PATH, zip_file)

    if os.path.exists(local_zip_path):
        print(f"✅ Arquivo {zip_file} já existe, pulando download.")
        return local_zip_path

    download_url = root_url + zip_file
    print(f"⬇️ Baixando {zip_file} de {download_url}...")

    response = requests.get(download_url, stream=True)
    
    if response.status_code == 200:
        with open(local_zip_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f"✅ Download concluído: {local_zip_path}")
    else:
        print(f"❌ Erro ao baixar {zip_file}: HTTP {response.status_code}")
    
    return local_zip_path


def unzip_files(zip_file_path):
    """ Extrai um arquivo ZIP e retorna o caminho do primeiro arquivo extraído. """
    
    extract_path = os.path.join(_PATH, os.path.splitext(os.path.basename(zip_file_path))[0])
    os.makedirs(extract_path, exist_ok=True)  # Garante que a pasta de extração existe

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        extracted_files = zip_ref.namelist()

    print(f" Arquivos extraídos em: {extract_path}")
    return extract_path if extracted_files else None


def save_doc(local_file_path, file_ext):
    """ Cria um caminho para salvar os arquivos extraídos. """
    dt = date.today()
    domain = os.path.basename(local_file_path).replace('.zip', '').lower()
    domain = re.sub(r"\d+", '', domain)

    return os.path.join(_PATH, f'dt={dt}', f'{domain}.{file_ext}')


def main():
    root_url = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2023-05/"
    
    print("🔍 Buscando links de arquivos ZIP...")
    zip_files = get_link_files(root_url)

    print("Links extraídos:", zip_files)  # Debug para verificar se os links estão corretos

    if not zip_files:
        print("❌ Nenhum arquivo ZIP encontrado. Verifique a URL ou o site da Receita Federal.")
        return

    for zip_file in zip_files:
        zip_path = download_zip_file(root_url, zip_file)

        # Criando caminho para salvar os arquivos extraídos
        landing_path = save_doc(zip_path, file_ext='zip')
        raw_path = save_doc(zip_path, file_ext='csv')

        print(f"📥 Arquivo salvo em {landing_path}")

        extract_path = unzip_files(zip_path)
        print(f"📂 Arquivo descompactado em {extract_path}")

        print(f"📊 Dados processados e salvos em {raw_path}")

    print("✅ Processo concluído.")


if __name__ == '__main__':
    main()
