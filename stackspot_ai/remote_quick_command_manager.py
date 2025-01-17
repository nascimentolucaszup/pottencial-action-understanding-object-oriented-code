import requests
import time


class QuickCommandManager:
    def __init__(self, api_url, token_manager, use_conversation_id=True, initial_token=None):
        """
        Inicializa o executor de comandos rápidos.

        :param api_url: URL base da API da StackSpot.
        :param token_manager: Instância de TokenManager para gerenciar tokens.
        :param use_conversation_id: Indica se o conversation_id deve ser usado.
        :param initial_token: Token inicial válido, se disponível.
        """
        self.api_url = api_url
        self.token_manager = token_manager
        self.use_conversation_id = use_conversation_id
        self.access_token = initial_token  # Token inicial válido
        self.last_403_method = None  # Armazena o último método que recebeu erro 403
        self.conversation_id = None  # Gerencia o conversation_id internamente

    def execute_quick_command(self, execute_slug, file_data):
        """
        Executa um comando rápido na API da StackSpot.

        :param execute_slug: Slug do comando a ser executado.
        :param file_data: Dados a serem enviados no payload.
        :return: ID da execução do comando.
        """
        def make_request(token):
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            command_payload = {"input_data": file_data}
            url = f"{self.api_url}/{execute_slug}"
            if self.use_conversation_id and self.conversation_id:
                url = f"{url}?conversation_id={self.conversation_id}"
            print(f"url: {url}")
            return requests.post(url, headers=headers, json=command_payload)

        if not self.access_token:
            self.access_token = self.token_manager.get_token()

        response = None
        try:
            response = make_request(self.access_token)
        except Exception as e:
            print("0 Erro ao converter o corpo da resposta para JSON:", e)

        if response.status_code == 200:
            response_data = response.json()
            execution_id = response_data.strip('"')
            if not execution_id:
                raise Exception("execution_id não encontrado na resposta da API.")
            # Reseta o conversation_id após a execução
            self.conversation_id = None
            return execution_id
        elif response.status_code == 403:  # Token expirado
            print("execute_quick_command: Token expirado. Atualizando...")
            self.last_403_method = "execute_quick_command"
            access_token = self._refresh_token()
            try:
                response = make_request(access_token)
            except Exception as e:
                print("1 Erro ao converter o corpo da resposta para JSON:", e)
            if response.status_code == 200:
                response_data = response.json()
                execution_id = response_data.strip('"')
                if not execution_id:
                    raise Exception("execution_id não encontrado na resposta da API.")
                # Reseta o conversation_id após a execução
                self.conversation_id = None
                return execution_id
            else:
                raise Exception(f"Erro ao executar comando após atualização do token: {response.status_code} - {response.text}")
        else:
            raise Exception(f"Erro ao executar comando: {response.status_code} - {response.text}")

    def poll_quick_command_status(self, callback_url, polling_interval=25, max_retries=30):
        """
        Verifica o status de execução de um Quick Command na API de Callback.

        :param callback_url: URL de callback para verificar o status.
        :param polling_interval: Intervalo entre as tentativas de polling.
        :param max_retries: Número máximo de tentativas.
        :return: Dados da execução do comando.
        """
        def make_request(token):
            headers = {"Authorization": f"Bearer {token}"}
            return requests.get(callback_url, headers=headers)

        if not self.access_token:
            self.access_token = self.token_manager.get_token()

        for attempt in range(max_retries):
            response = make_request(self.access_token)

            if response.status_code == 200:
                data = response.json()
                status = data.get("progress").get("status")
                if status == "COMPLETED":
                    print("Comando finalizado com sucesso.")
                    # Atualiza o conversation_id com base no callback, se necessário
                    if self.use_conversation_id:
                        self.conversation_id = data.get("conversation_id")
                    return data
                elif status in ["RUNNING", "CREATED"]:
                    print(f"Comando ainda em execução. Tentativa {attempt + 1}/{max_retries}.")
                else:
                    raise Exception(f"Status inesperado: {status}")
            elif response.status_code == 403:  # Token expirado
                print(f"poll_quick_command_status: Token expirado. Atualizando: {response.text}")
                self.last_403_method = "poll_quick_command_status"
                self.access_token = self._refresh_token()
            else:
                raise Exception(f"Erro ao consultar status: {response.status_code} - {response.text}")

            time.sleep(polling_interval)

        raise Exception("Número máximo de tentativas atingido. O comando não foi concluído.")

    def _refresh_token(self):
        """
        Atualiza o token de acesso usando o TokenManager.
        """
        self.token_manager.refresh_token()
        return self.token_manager.get_token()