import os
from concurrent.futures import ThreadPoolExecutor, as_completed


class FileProcessor:
    def __init__(
        self,
        api_url,
        execute_slug,
        token_manager,
        quick_command_manager,
        prompts_manager,
        max_file_workers=4,
        use_parallel=False,
    ):
        """
        Inicializa o processador de arquivos baseado em JSON.

        :param api_url: URL base da API.
        :param execute_slug: Slug do comando a ser executado.
        :param token_manager: Instância de TokenManager para gerenciar tokens.
        :param quick_command_manager: Instância para gerenciar Quick Commands.
        :param max_file_workers: Número máximo de threads para processar arquivos.
        :param use_parallel: Define se o processamento será paralelo ou sequencial.
        """
        self.api_url = api_url
        self.execute_slug = execute_slug
        self.token_manager = token_manager
        self.quick_command_manager = quick_command_manager
        self.prompts_manager = prompts_manager
        self.max_file_workers = max_file_workers
        self.use_parallel = use_parallel
        self.first_file_name = None  # Armazena o nome do primeiro arquivo processado
        self.processed_files = []  # Lista para armazenar os nomes dos arquivos processados
        self.processed_docs = []

    def process_json(self, json_data):
        """
        Processa os arquivos com base no JSON fornecido.

        :param json_data: Dados JSON contendo informações dos arquivos e dependências.
        """
        try:
            controller = json_data.get("controller")
            if not controller:
                raise ValueError("JSON inválido: 'controller' não encontrado.")

            # Processa o arquivo do controller
            self._process_file(controller["file_path"], prompt_value=1)

            # Processa as dependências do controller
            self._process_dependencies(controller.get("dependencies", []))

            # Chamada extra para StackSpot AI após a leitura completa do JSON
            self._call_stackspot_ai()

        except Exception as e:
            print(f"Erro durante o processamento do JSON: {e}")

    def _process_dependencies(self, dependencies):
        """
        Processa as dependências recursivamente.

        :param dependencies: Lista de dependências a serem processadas.
        """
        if not dependencies:
            return

        if self.use_parallel:
            with ThreadPoolExecutor(max_workers=self.max_file_workers) as executor:
                futures = [
                    executor.submit(self._process_dependency, dependency)
                    for dependency in dependencies
                ]
                for future in as_completed(futures):
                    future.result()
        else:
            for dependency in dependencies:
                self._process_dependency(dependency)

    def _process_dependency(self, dependency):
        """
        Processa uma única dependência.

        :param dependency: Dependência a ser processada.
        """
        try:
            self._process_file(dependency["file_path"], prompt_value=2)
            self._process_dependencies(dependency.get("dependencies", []))
        except Exception as e:
            print(f"Erro ao processar dependência '{dependency['class_name']}': {e}")

    def _process_file(self, file_path, prompt_value):
        """
        Processa um único arquivo.

        :param file_path: Caminho do arquivo a ser processado.
        :param prompt_value: Valor do prompt a ser utilizado.
        """
        if not os.path.exists(file_path):
            print(f"Arquivo '{file_path}' não encontrado. Pulando...")
            return

        file_name = os.path.basename(file_path)
        try:
            file_data = self._read_file(file_path)
            data = self.prompts_manager.get_prompt(prompt_value, replacement=file_data, documentation="")
            # Executa o Quick Command no conteúdo do arquivo
            response = self._execute_and_poll(data)

            # Salva a resposta em um arquivo Markdown
            self._save_to_markdown(file_name.replace(".cs", ""), response.get('result').replace("```markdown", "").replace("```", ""))
            self.processed_docs.append(response.get('result'))

            # Armazena o nome do primeiro arquivo processado
            if self.first_file_name is None:
                self.first_file_name = file_name

            # Adiciona o nome do arquivo à lista de arquivos processados
            self.processed_files.append(file_name)

        except Exception as e:
            print(f"Erro ao processar o arquivo '{file_name}': {e}")

    def _read_file(self, file_path):
        """
        Lê o conteúdo de um arquivo, tentando diferentes codificações.

        :param file_path: Caminho do arquivo.
        :return: Conteúdo do arquivo.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Erro ao decodificar '{file_path}' como UTF-8. Tentando com 'latin-1'...")
            with open(file_path, "r", encoding="latin-1") as file:
                return file.read()

    def _execute_and_poll(self, file_data):
        """
        Executa o Quick Command e verifica o status até a conclusão.

        :param file_data: Conteúdo do arquivo.
        :return: Resposta final do Quick Command.
        """
        execution_id = self.quick_command_manager.execute_quick_command(
            self.execute_slug, file_data
        )
        callback_url = f"{self.api_url}/quick-commands/callback/{execution_id}"
        return self.quick_command_manager.poll_quick_command_status(callback_url)

    def _save_to_markdown(self, file_name, response):
        """
        Salva a resposta em um arquivo Markdown.

        :param file_name: Nome do arquivo.
        :param response: Resposta a ser salva.
        """
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, f"{file_name}.md")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response)
        print(f"Arquivo Markdown '{file_path}' salvo com sucesso.")

    def _call_stackspot_ai(self):
        """
        Realiza uma chamada extra para StackSpot AI após a leitura completa do JSON.
        """
        try:
            data = self.prompts_manager.get_prompt(3, replacement=self.get_processed_files_as_string(), documentation=self.get_processed_docs_as_string())
            print("ultimo prompt: {data}")
            execution_id = self.quick_command_manager.execute_quick_command(
                self.execute_slug, data
            )
            callback_url = f"{self.api_url}/quick-commands/callback/{execution_id}"
            response = self.quick_command_manager.poll_quick_command_status(callback_url)
            # Salva a resposta em um arquivo Markdown usando o nome do primeiro arquivo processado
            if self.first_file_name:
                self._save_to_markdown(f"{self.first_file_name.replace('Controller.cs', '')}_Doc_Unificada", response.get('result').replace("```markdown", "").replace("```", ""))
            else:
                print("Nenhum arquivo foi processado para salvar a resposta.")

            print(f"Chamada para StackSpot AI concluída com sucesso: {response}")
        except Exception as e:
            print(f"Erro ao realizar a chamada para StackSpot AI: {e}")

    def get_processed_files_as_string(self):
        """ Retorna os nomes dos arquivos processados como uma string. """
        return ", ".join(self.processed_files)
    
    def get_processed_docs_as_string(self):
        """ Retorna os nomes dos arquivos processados como uma string. """
        return "\n".join(self.processed_docs)