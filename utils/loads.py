import json
import os

# Função para carregar os dados do JSON
def load_data(file_path):
    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        print(f"Arquivo '{file_path}' não encontrado.")
        return None

    # Carrega os dados do arquivo JSON
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o JSON: {e}")
        return None