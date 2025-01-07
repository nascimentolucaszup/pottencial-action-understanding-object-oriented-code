import requests


class KnowledgeSourcesManager:
    def __init__(self, base_url, token_manager, initial_toekn=None):
        """
        Inicializa a classe para interagir com a API de Knowledge Source.

        :param base_url: URL base da API.
        :param token_manager: Instância de TokenManager para gerenciar tokens.
        """
        self.base_url = base_url
        self.token_manager = token_manager
        self.access_token = initial_toekn or token_manager.get_token()

    def _get_headers(self):
        """
        Retorna os cabeçalhos padrão para as requisições.

        :return: Dicionário com os cabeçalhos.
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _refresh_token(self):
        """
        Atualiza o token de acesso.
        """
        self.token_manager.refresh_token()
        self.access_token = self.token_manager.get_token()

    def create_knowledge_source(self, slug, name, description, ks_type):
        """
        Cria um novo Knowledge Source.

        :param slug: Identificador único do KS.
        :param name: Nome do KS.
        :param description: Descrição do KS.
        :param ks_type: Tipo do KS (API, SNIPPET ou CUSTOM).
        :return: Resposta da API.
        """
        url = f"{self.base_url}/knowledge-sources"
        payload = {
            "slug": slug,
            "name": name,
            "description": description,
            "type": ks_type
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        if response.status_code == 403:
            self._refresh_token()
            return self.create_knowledge_source(slug, name, description, ks_type)
        response.raise_for_status()
        return response.json()

    def upload_file(self, file_name, ks_slug, file_path):
        """
        Faz upload de um arquivo para um Knowledge Source existente.

        :param file_name: Nome do arquivo.
        :param ks_slug: Slug do KS.
        :param file_path: Caminho absoluto do arquivo.
        :return: ID do upload.
        """
        # Passo 1: Obter URL de upload
        url = f"{self.base_url}/file-upload/form"
        payload = {
            "file_name": file_name,
            "target_id": ks_slug,
            "target_type": "KNOWLEDGE_SOURCE",
            "expiration": 600
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        if response.status_code == 403:
            self._refresh_token()
            return self.upload_file(file_name, ks_slug, file_path)
        response.raise_for_status()
        upload_data = response.json()

        # Passo 2: Fazer upload do arquivo
        upload_url = upload_data["url"]
        form_data = upload_data["form"]
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(upload_url, data=form_data, files=files)
            response.raise_for_status()

        return upload_data["id"]

    def check_upload_status(self, upload_id):
        """
        Verifica o status de um upload.

        :param upload_id: ID do upload.
        :return: Status do upload.
        """
        url = f"{self.base_url}/file-upload/@{upload_id}"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 403:
            self._refresh_token()
            return self.check_upload_status(upload_id)
        response.raise_for_status()
        return response.json()

    def upload_snippet(self, ks_slug, use_case, code, language):
        """
        Faz upload de um snippet para um Knowledge Source.

        :param ks_slug: Slug do KS.
        :param use_case: Descrição do caso de uso.
        :param code: Código do snippet.
        :param language: Linguagem do snippet.
        :return: Resposta da API.
        """
        url = f"{self.base_url}/knowledge-sources/{ks_slug}/snippets"
        payload = {
            "use_case": use_case,
            "code": code,
            "language": language
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        if response.status_code == 403:
            self._refresh_token()
            return self.upload_snippet(ks_slug, use_case, code, language)
        response.raise_for_status()
        return response.json()

    def upload_custom_content(self, ks_slug, content):
        """
        Faz upload de conteúdo customizado para um Knowledge Source.

        :param ks_slug: Slug do KS.
        :param content: Conteúdo a ser enviado.
        :return: Resposta da API.
        """
        url = f"{self.base_url}/knowledge-sources/{ks_slug}/custom"
        payload = {"content": content}
        response = requests.post(url, headers=self._get_headers(), json=payload)
        if response.status_code == 403:
            self._refresh_token()
            return self.upload_custom_content(ks_slug, content)
        response.raise_for_status()
        return response.json()

    def delete_objects(self, ks_slug, standalone=None):
        """
        Apaga objetos de um Knowledge Source.

        :param ks_slug: Slug do KS.
        :param standalone: Define se deve apagar apenas standalone (True), apenas uploads (False) ou todos (None).
        :return: Resposta da API.
        """
        url = f"{self.base_url}/knowledge-sources/{ks_slug}/objects"
        if standalone is not None:
            url += f"?standalone={str(standalone).lower()}"
        response = requests.delete(url, headers=self._get_headers())
        if response.status_code == 403:
            self._refresh_token()
            return self.delete_objects(ks_slug, standalone)
        response.raise_for_status()
        return response.json()