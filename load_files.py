import os
import re
import requests
from bs4 import BeautifulSoup 

# Caminho principal
_PATH = os.getenv['_PATH']
RAW = os.path.join(_PATH, 'raw')  # Criar caminho para a pasta 'raw'
root_url = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2023-05/"


def get_link_files(root_url):
    response = requests.get(root_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    zip_links = [link.get('href') for link in soup.find_all('a', href=True) if link['href'].endswith('.zip')]

    return zip_links     

def generate_files_path(path, root_url):
    zip_links = get_link_files(root_url)
    paths = []
    for name in zip_links:
        name = name.split('.zip')[0]
        paths.append(f"{path}\{name}")
    return paths

def generate_csv_files():
    files_paths = generate_files_path(_PATH, root_url)
    
    for paths in files_paths:
     
        if os.path.isdir(paths):       
            print(f'{paths} é uma pasta')
            
      
        if not os.path.isfile(paths):
            print(f'{paths} não é um arquivo')
        print('------------------------------------=================------------------------------------')
        
        try:
            for files in paths:
                files = os.listdir(paths)
                print(f"A pasta {paths} foi aberta com sucesso!")
                base_name = files[0]
                name = re.sub(r"\.\w+$", '', base_name)
                csv_name = name + '.csv'
                print(f" O arquivo {csv_name} foi salvo com sucesso")
                print('------------------------------------=================------------------------------------')

        except Exception as e:
            print(f'Erro ao abrir o {paths}:', e)
            

def save_files(path):
    pass

# def rename_files():
#         # Remover a extensão do nome do arquivo
#         base_name = re.sub(r"\.\w+$", '', file)  # Remove a extensão original
#         new_name = base_name + '.csv'  # Define a nova extensão como CSV
#         new_file_path = os.path.join(RAW, new_name)  # Caminho para mover o arquivo renomeado

#         # Renomeia e move o arquivo
#         os.rename(file_path, new_file_path)
#         print(f"✅ {file} renomeado para {new_name} e movido para {RAW}")

def main():
    generate_csv_files()
  
    # for file in files_name:
    #     print(os.path.isdir(file))
    #     print(file)
    

if __name__ == '__main__':
    main()
