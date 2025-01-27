import os
import json
import streamlit as st

class CSFileIndexer:
    def __init__(self, base_path=None, save_full_path=True):
        """
        Inicializa o indexador de arquivos .cs.

        Args:
            base_path (str): Caminho base do projeto. Se None, será solicitado ao usuário.
            save_full_path (bool): Se True, salva o caminho completo dos arquivos. Caso contrário, salva apenas os nomes.
        """
        self.base_path = base_path
        self.save_full_path = save_full_path
        self.cs_files = []

    def collect_cs_files(self):
        """
        Percorre todas as pastas do projeto e coleta arquivos com extensão .cs.

        Returns:
            list: Lista de dicionários contendo os arquivos .cs e seus caminhos.
        """
        if not self.base_path or not os.path.exists(self.base_path):
            st.error("O caminho base fornecido não existe. Por favor, forneça um caminho válido.")
            return []

        cs_files = []
        for root, _, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    cs_files.append({
                        "file_name": file,
                        "path": file_path if self.save_full_path else file
                    })
        self.cs_files = cs_files
        return cs_files

    def save_as_json(self, output_path):
        """
        Salva os dados coletados no formato JSON.

        Args:
            output_path (str): Caminho do arquivo de saída.
        """
        if not self.cs_files:
            st.warning("Nenhum arquivo .cs foi coletado para salvar.")
            return

        try:
            with open(output_path, "w", encoding="utf-8") as json_file:
                json.dump(self.cs_files, json_file, indent=4, ensure_ascii=False)
            st.success(f"Índice salvo em: {output_path}")
        except Exception as e:
            st.error(f"Erro ao salvar o arquivo JSON: {e}")
