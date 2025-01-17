import json
from processing.file_processor import FileProcessor
from stackspot_ai.token_manager import TokenManager
from stackspot_ai.knowledge_sources_manager import KnowledgeSourcesManager
from stackspot_ai.remote_quick_command_manager import QuickCommandManager
from stackspot_ai.prompts_manager import PromptsManager
from processing.class_processor import CSharpDependencyAnalyzer

def run(metadata):
    # Obtendo informações dos metadados
    project_path = metadata.inputs.get('project_path')
    execute_slug = metadata.inputs.get('execute_slug')
    account_slug = metadata.inputs.get('account_slug')
    client_id = metadata.inputs.get('client_id')
    client_secret = metadata.inputs.get('client_secret')
    controller_path = metadata.inputs.get('controller_path')

    analyzer = CSharpDependencyAnalyzer(project_path)
    analyzer.initialize()

    controller_dependency = analyzer.analyze_dependencies_tree(controller_path, max_depth=2)
    json_data = analyzer.generate_controller_json_report(controller_dependency)

    print("=== Controller JSON Report ===")
    print(json_data)

    token_manager = TokenManager(
        account_slug,
        client_id,
        client_secret
    )

    token_manager.refresh_token()
    token = token_manager.get_token()

    # Inicializando o QuickCommandManager
    quick_command_manager = QuickCommandManager(
        api_url="https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution",
        token_manager=token_manager,
        initial_token=token
    )

    prompts_manager = PromptsManager()

    # Inicializando o FileProcessor
    processor = FileProcessor(
        api_url="https://genai-code-buddy-api.stackspot.com/v1",
        execute_slug=execute_slug,
        token_manager=token_manager,
        prompts_manager=prompts_manager,
        quick_command_manager=quick_command_manager,
    )

    # Processando os arquivos
    processor.process_json(json.loads(json_data))