from processing.file_processor import FileProcessor
from stackspot_ai.token_manager import TokenManager
from stackspot_ai.knowledge_sources_manager import KnowledgeSourcesManager
from stackspot_ai.remote_quick_command_manager import QuickCommandManager

def run(metadata):
    # Obtendo informações dos metadados
    folder_path = metadata.inputs.get('folder_path')
    execute_slug = metadata.inputs.get('execution_slug')
    account_slug = metadata.inputs.get('account_slug')
    client_id = metadata.inputs.get('client_id')
    client_secret = metadata.inputs.get('client_secret')
    extension_file = metadata.inputs.get('extension_file')

    token_manager = TokenManager(
        account_slug,
        client_id,
        client_secret
    )

    token_manager.refresh_token()
    token = token_manager.get_token()

    # Inicializando o QuickCommandManager
    quick_command_manager = QuickCommandManager(
        api_url="https://api.example.com",
        token_manager=token_manager,
        initial_token=token
    )

    # Inicializando o FileProcessor
    file_processor = FileProcessor(
        folder_path=folder_path,
        execute_slug=execute_slug,
        quick_command_manager=quick_command_manager,
        allowed_extension=extension_file
    )

    # Processando os arquivos
    file_processor.process_files()