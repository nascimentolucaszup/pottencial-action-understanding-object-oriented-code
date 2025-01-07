from concurrent.futures import ThreadPoolExecutor, as_completed
import os


class FileProcessor:
    def __init__(
            self,
            folder_path,
            api_url,
            execute_slug,
            token_manager,
            quick_command_manager,
            max_file_workers=4,
            use_parallel=True
        ):
        """
        Inicializa o processador de Quick Commands.

        :param folder_path: Caminho da pasta contendo os arquivos.
        :param api_url: URL base da API.
        :param execute_slug: Slug do comando a ser executado.
        :param token_manager: Instância de TokenManager para gerenciar tokens.
        :param max_file_workers: Número máximo de threads para processar arquivos.
        :param use_parallel: Define se o processamento será paralelo ou sequencial.
        """
        self.folder_path = folder_path
        self.api_url = api_url
        self.execute_slug = execute_slug
        self.token_manager = token_manager
        self.quick_command_manager = quick_command_manager
        self.max_file_workers = max_file_workers
        self.use_parallel = use_parallel

    def process_files(self):
        """
        Processa todos os arquivos na pasta especificada.
        """
        try:
            self._validate_folder()

            # Obter todos os arquivos na pasta
            files = self._get_files()

            if self.use_parallel:
                # Processa os arquivos em paralelo
                self._process_files_in_parallel(files)
            else:
                # Processa os arquivos de forma sequencial
                self._process_files_sequentially(files)

        except Exception as e:
            print(f"Erro durante o processamento: {e}")

    def _process_files_in_parallel(self, files):
        """
        Processa os arquivos em paralelo.
        """
        with ThreadPoolExecutor(max_workers=self.max_file_workers) as file_executor:
            file_futures = [file_executor.submit(self._process_file, file_path) for file_path in files]
            for future in as_completed(file_futures):
                future.result()  # Aguarda a conclusão de cada tarefa

    def _process_files_sequentially(self, files):
        """
        Processa os arquivos de forma sequencial.
        """
        for file_path in files:
            self._process_file(file_path)

    def _validate_folder(self):
        """
        Valida se a pasta existe e é válida.
        """
        if not os.path.exists(self.folder_path):
            raise FileNotFoundError(f"A pasta '{self.folder_path}' não foi encontrada.")
        if not os.path.isdir(self.folder_path):
            raise NotADirectoryError(f"O caminho '{self.folder_path}' não é uma pasta válida.")

    def _get_files(self, allowed_extension=None):
        """
        Retorna uma lista de arquivos na pasta com a extensão permitida.
        :param allowed_extension: Extensão do arquivo permitida (ex: '.py', '.java'). Se None, retorna todos os arquivos.
        """
        return [
            os.path.join(self.folder_path, file_name)
            for file_name in os.listdir(self.folder_path)
            if os.path.isfile(os.path.join(self.folder_path, file_name)) and
            (allowed_extension is None or file_name.endswith(allowed_extension))
        ]

    def _process_file(self, file_path):
        """
        Processa um único arquivo.

        :param file_path: Caminho do arquivo a ser processado.
        """
        file_name = os.path.basename(file_path)
        try:
            file_data = self._read_file(file_path)

            # Executa o Quick Command no conteúdo do arquivo
            response = self._execute_and_poll(file_data)

            # Salva a resposta em um arquivo Markdown
            self._save_to_markdown(file_name, response)

        except Exception as e:
            print(f"Erro ao processar o arquivo '{file_name}': {e}")

    def _read_file(self, file_path):
        """
        Lê o conteúdo de um arquivo, tentando diferentes codificações.

        :param file_path: Caminho do arquivo.
        :return: Conteúdo do arquivo.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Erro ao decodificar '{file_path}' como UTF-8. Tentando com 'latin-1'...")
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()

    def _execute_and_poll(self, file_data):
        """
        Executa o Quick Command e verifica o status até a conclusão.

        :param file_data: Conteúdo do arquivo.
        :return: Resposta final do Quick Command.
        """
        execution_id = self.quick_command_manager.execute_quick_command(self.execute_slug, file_data)
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