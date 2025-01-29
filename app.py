import os
import streamlit as st
from dotenv import load_dotenv
from utils import loads
from processing.file_handler_processor import FileHandlerProcessor
from processing.file_processor import FileProcessor
from stackspot_ai.prompts_manager import PromptsManager
from stackspot_ai.remote_quick_command_manager import QuickCommandManager
from stackspot_ai.token_manager import TokenManager
from view.business_documentation import BusinessDocumentation
from processing.class_processor import CSharpDependencyAnalyzer
from processing.file_index_processor import CSFileIndexer

# Carregar as variáveis do arquivo .env
load_dotenv()

execute_slug = os.getenv('EXECUTE_SLUG')
account_slug = os.getenv('ACCOUNT_SLUG')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Configuração da página
st.set_page_config(
    page_title="Modernização de Projeto by StackSpot AI", 
    initial_sidebar_state="expanded"
)

# Função para renderizar a página Home
def render_home():
    st.markdown(
        """
        # **Bem-vindo ao Projeto de Documentação Dinâmica de Domínios**

        Este projeto foi idealizado para oferecer uma solução robusta e intuitiva para a criação, organização e gerenciamento de informações relacionadas a domínios de software. Ele foi projetado com o objetivo de simplificar a coleta e estruturação de dados essenciais para o desenvolvimento de sistemas, permitindo que equipes técnicas e de negócios colaborem de forma eficiente e organizada.

        A principal funcionalidade do projeto é proporcionar uma interface dinâmica e amigável, onde os usuários podem preencher informações detalhadas sobre os domínios de seus projetos. A interface foi cuidadosamente planejada para oferecer uma experiência de usuário (UX) fluida e agradável, garantindo que mesmo os usuários menos experientes possam navegar e interagir com facilidade.

        ---

        ## **O que você pode fazer com este projeto?**

        ### 1. **Definir Metadados do Domínio**
        O projeto permite que você insira informações detalhadas sobre o domínio principal, como o nome, descrição e outros metadados relevantes. Esses dados são fundamentais para documentar o propósito e as características gerais do domínio.

        ### 2. **Configurar a Classe Principal do Domínio**
        Você pode especificar a classe principal que representa o domínio, incluindo seu nome, caminho no projeto e uma descrição detalhada de sua funcionalidade. Isso ajuda a centralizar as informações mais importantes do domínio em um único lugar.

        ### 3. **Adicionar Dependências Secundárias**
        O sistema permite que você adicione classes secundárias que compõem o domínio principal. Cada classe secundária pode ser documentada com seu nome, caminho no projeto, descrição e métodos associados. Além disso, você pode adicionar subdependências a essas classes, criando uma estrutura hierárquica que reflete a complexidade do domínio.

        ### 4. **Gerenciar Estruturas Complexas de Dependências**
        Com a possibilidade de adicionar dependências recursivas, o projeto é ideal para documentar sistemas complexos que possuem várias camadas de interdependência. Isso garante que todas as relações entre as classes sejam claramente documentadas e compreendidas.

        ### 5. **Interface Dinâmica e Personalizável**
        A interface foi projetada para ser altamente dinâmica, permitindo que os usuários adicionem novos campos e inputs conforme necessário. Isso significa que você pode expandir a documentação do domínio à medida que o projeto evolui, sem limitações rígidas.
        
        ---
        """
    )

# Sidebar para navegação
tab1, tab2 = st.tabs(["Home", "Documentação de Negócio"])

token_manager = TokenManager(
    account_slug,
    client_id,
    client_secret
)

# Inicializando o QuickCommandManager
quick_command_manager = QuickCommandManager(
    api_url="https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution",
    token_manager=token_manager,
    initial_token=None
)

prompts_manager = PromptsManager()
file_handler_processor = FileHandlerProcessor()

analyzer = CSharpDependencyAnalyzer(loads.load_data("file-to-analyze/index.json"))

# Inicializando o FileProcessor
processor = FileProcessor(
    api_url="https://genai-code-buddy-api.stackspot.com/v1",
    execute_slug=execute_slug,
    token_manager=token_manager,
    prompts_manager=prompts_manager,
    quick_command_manager=quick_command_manager,
    file_handler_processor=file_handler_processor
)

file_index_processor = CSFileIndexer(
    base_path="file-to-analyze"
)

doc = BusinessDocumentation(
    file_processor=processor,
    class_processor=analyzer,
    file_index_processor=file_index_processor
)

with tab1:
    render_home()
with tab2:
    doc.render()