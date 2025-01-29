import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class FileProcessor:
    def __init__(
        self,
        api_url,
        execute_slug,
        token_manager,
        quick_command_manager,
        file_handler_processor,
        prompts_manager,
        max_file_workers=4,
        use_parallel=False,
    ):
        """Inicializa o processador de arquivos baseado em JSON."""
        self.api_url = api_url
        self.execute_slug = execute_slug
        self.token_manager = token_manager
        self.quick_command_manager = quick_command_manager
        self.file_handler_processor = file_handler_processor
        self.prompts_manager = prompts_manager
        self.max_file_workers = max_file_workers
        self.use_parallel = use_parallel
        self.metadata = None
        self.main_class = None
        self.main_class_code = None
        self.execution_mode = None
        self.documentation_type = None
        self.dependencies = []
        self.processed_files = []

    def process_json(self, json_data):
        """Processa os arquivos com base no JSON fornecido."""
        try:
            print(f"json: {json_data}")
            # Extraindo os objetos principais
            self.metadata = json_data.get("metadata", {})
            self.main_class = json_data.get("main_class", {})
            self.dependencies = json_data.get("dependencies", [])
            self.execution_mode = json_data.get("execution_mode", None)
            self.documentation_type = json_data.get("documentation_type", None)
            print(f"tipo documento {self.documentation_type}")
    
            # Processa o arquivo principal
            self.main_class_code = self._read_file(self.main_class.get("path", ""))
            self.file_handler_processor.initialize(self.main_class_code)
            self.main_class_code = self.file_handler_processor.process()
    
            # Inicializa variáveis para armazenar os conteúdos processados
            self.dependency_contents = {}
            self.subdependency_contents = {}
    
            # Processa as dependências
            self._process_dependencies(self.dependencies)
    
            # Chamada extra para StackSpot AI após a leitura completa do JSON
            self._call_stackspot_ai()
        except Exception as e:
            print(f"Erro durante o processamento do JSON: {e}")
    
    def _process_dependencies(self, dependencies):
        """Processa as dependências recursivamente."""
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
        """Processa uma única dependência, incluindo subdependências."""
        try:
            # Processa o arquivo da dependência
            dependency_path = dependency.get("path", "")
            if dependency_path:
                processed_content = self._process_file(dependency_path)
                self.dependency_contents[dependency_path] = processed_content
    
            # Processa as subdependências, se existirem
            subdependencies = dependency.get("subdependencies", [])
            if subdependencies:
                print(f"Processando subdependências de {dependency_path}...")
                for subdependency in subdependencies:
                    subdependency_path = subdependency.get("path", "")
                    if subdependency_path:
                        subprocessed_content = self._process_file(subdependency_path)
                        self.subdependency_contents[subdependency_path] = subprocessed_content
        except Exception as e:
            print(f"Erro ao processar dependência '{dependency.get('path', '')}': {e}")
    
    def _process_file(self, file_path):
        """Processa um único arquivo."""
        if not file_path or not os.path.exists(file_path):
            print(f"Arquivo '{file_path}' não encontrado. Pulando...")
            return None
    
        file_name = os.path.basename(file_path)
        try:
            file_data = self._read_file(file_path)
            self.file_handler_processor.initialize(file_data)
            processed_data = self.file_handler_processor.process()
            return processed_data
        except Exception as e:
            print(f"Erro ao processar o arquivo '{file_name}': {e}")
            return None
    
    def _read_file(self, file_path):
        """Lê o conteúdo de um arquivo, tentando diferentes codificações."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Erro ao decodificar '{file_path}' como UTF-8. Tentando com 'latin-1'...")
            with open(file_path, "r", encoding="latin-1") as file:
                return file.read()

    def _call_stackspot_ai(self):
        """Realiza uma chamada extra para StackSpot AI após a leitura completa do JSON."""
        try:
            # Ajusta o execute_slug com base no tipo de documentação
            if self.documentation_type == "Negócio":
                self.execute_slug = "rqc-domain-documentation"
            elif self.documentation_type == "Técnica":
                self.execute_slug = "rqc-tech-documentation"

            # Construindo o prompt com os dados extraídos
            prompt = self._build_prompt()
            print(f"prompt: {prompt}")
            execution_id = self.quick_command_manager.execute_quick_command(
                self.execute_slug, prompt
            )
            callback_url = f"{self.api_url}/quick-commands/callback/{execution_id}"
            response = self.quick_command_manager.poll_quick_command_status(callback_url)

            # Salva a resposta em um arquivo Markdown
            self._save_to_markdown(response.get("result", ""))
        except Exception as e:
            print(f"Erro ao realizar a chamada para StackSpot AI: {e}")

    def _build_prompt(self):
        """Constrói o prompt para a StackSpot AI com base nos dados processados."""
        if self.documentation_type == "Negócio":
            # Prompt para documentação de negócio
            prompt = f"""
            # {self.metadata.get('name', '')}
            {self.metadata.get('description', '')}.Extrair ou realizar um recorte as funcionalidades específica do domínio, como parte de uma estratégia de modernização do ecossistema. Utilize a abordagem de estrangulamento para realizar essa extração, garantindo que o escopo e os critérios sejam bem definidos. Certifique-se de documentar o processo, os desafios enfrentados e os resultados esperados.

            Principal Domínio:
            Classe:
            {self.main_class_code}
            Methods: {', '.join(self.main_class.get('methods', []))}

            Domínios Secundários:
            """
            for dependency in self.dependencies:
                prompt += self._build_dependency_prompt(dependency)
        elif self.documentation_type == "Técnica":
            # Prompt para documentação técnica (apenas classes)
            prompt = f"""
            Classe:
            {self.main_class_code}
            """
            for dependency in self.dependencies:
                prompt += self._build_dependency_prompt(dependency)
        else:
            raise ValueError("Tipo de documentação inválido ou não especificado.")
        
        return prompt

    def _build_dependency_prompt(self, dependency):
        """Constrói o prompt para uma dependência, incluindo subdependências."""
        dependency_path = dependency.get("path", "")
        dependency_code = self.dependency_contents.get(dependency_path, "Código não encontrado ou não processado.")
        
        prompt = f"""
        Classe:
        {dependency_code}
        Methods: {', '.join(dependency.get('methods', []))}
        Subdependencies:
        """
        for subdependency in dependency.get("subdependencies", []):
            prompt += self._build_subdependency_prompt(subdependency)
        return prompt

    def _build_subdependency_prompt(self, subdependency):
        """Constrói o prompt para uma subdependência."""
        subdependency_path = subdependency.get("path", "")
        subdependency_code = self.subdependency_contents.get(subdependency_path, "Código não encontrado ou não processado.")
        
        prompt = f"""
            Classe:
            {subdependency_code}
            Methods: {', '.join(subdependency.get('methods', []))}
        """
        return prompt

    def _save_to_markdown(self, response):
        """Salva a resposta em um arquivo Markdown."""
        # Define o diretório de saída com base no tipo de documentação
        if self.documentation_type == "Negócio":
            output_dir = "output/business"
        elif self.documentation_type == "Técnica":
            output_dir = "output/technical"
        else:
            raise ValueError("Tipo de documentação inválido ou não especificado.")

        # Cria o diretório de saída, se necessário
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define o nome do arquivo com base em metadata.name
        file_name = self.metadata.get("name", "default_name").replace(" ", "_").lower()
        file_path = os.path.join(output_dir, f"{file_name}.md")

        # Salva o conteúdo no arquivo
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response)
        print(f"Arquivo Markdown '{file_path}' salvo com sucesso.")