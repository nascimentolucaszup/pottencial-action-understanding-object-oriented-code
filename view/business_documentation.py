import json
import os
import shutil
import zipfile
import streamlit as st
from utils.loads import load_data

class BusinessDocumentation:
    def __init__(self, file_processor, class_processor, file_index_processor):
        # Inicializar estado
        if "dependencies" not in st.session_state:
            st.session_state.dependencies = []
        if "active_dependency_index" not in st.session_state:
            st.session_state.active_dependency_index = None
        if "execution_mode" not in st.session_state:
            st.session_state.execution_mode = "Manual"
        if "documentation_type" not in st.session_state:
            st.session_state.documentation_type = "Negócio"
        self.file_processor = file_processor
        self.class_processor = class_processor
        self.file_index_processor = file_index_processor
        self.files_indexrs = load_data("file-to-analyze/index.json") or None

    def handle_zip_upload(self):
        """Gerenciar o upload e descompactação de arquivos .zip."""
        st.subheader("Upload de Arquivo ZIP")
        uploaded_file = st.file_uploader(
            "Faça o upload de um arquivo .zip para análise",
            type="zip",
            help="O objetivo deste input é descompactar o projeto para que possa ser usado para análises."
        )

        # Verificar se a pasta "file-to-analyze" já contém arquivos
        target_dir = "file-to-analyze"
        if os.path.exists(target_dir) and os.listdir(target_dir):
            st.warning(
                "A pasta 'file-to-analyze' já contém arquivos. "
                "Fazer o upload de um novo arquivo irá substituir o conteúdo atual."
            )

        if uploaded_file:
            # Excluir arquivos existentes na pasta
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir, exist_ok=True)

            # Salvar e descompactar o arquivo .zip
            with open(os.path.join(target_dir, "uploaded.zip"), "wb") as f:
                f.write(uploaded_file.getbuffer())
            with zipfile.ZipFile(os.path.join(target_dir, "uploaded.zip"), "r") as zip_ref:
                zip_ref.extractall(target_dir)
                os.remove(os.path.join(target_dir, "uploaded.zip"))
                self.files_indexrs = self.files_indexrs = self.file_index_processor.collect_cs_files()
                self.file_index_processor.save_as_json(
                    os.path.join(target_dir, "index.json")
                )

            st.success("Arquivo descompactado com sucesso!")
            st.info(f"Os arquivos foram extraídos para a pasta '{target_dir}'.")

    def validate_inputs(self):
        """Validar os inputs obrigatórios com base no modo de execução."""
        errors = []

        # Validação do campo "Nome do Domínio"
        if not self.metadata.get("name"):
            errors.append("O campo 'Nome do Domínio' é obrigatório.")

        # Validação do campo "Caminho da Classe Principal"
        if not self.main_class.get("path"):
            errors.append("O campo 'Caminho da Classe Principal' é obrigatório.")

        # Validação de dependências no modo Manual
        if st.session_state.execution_mode == "Manual":
            for i, dependency in enumerate(st.session_state.dependencies):
                if not dependency.get("path"):
                    errors.append(f"O campo 'Caminho da Dependência {i + 1}' é obrigatório.")

        # Exibir erros, se houver
        if errors:
            for error in errors:
                st.error(error)
            return False
        return True

    def render_controls(self):
        """Renderizar os controles iniciais no início da página e torná-los obrigatórios."""
        st.header("Configurações Iniciais")
    
        # Controle para o modo de execução
        st.subheader("Modo de Execução")
        st.session_state.execution_mode = st.segmented_control(
            "Selecione o modo de execução:",
            options=["Manual", "Automatizado"],
            help=(
                "Execução Manual: O usuário preenche todas as informações.\n"
                "Execução Automatizada: O usuário adiciona apenas as informações iniciais e do domínio principal (geralmente o controller)."
            )
        )
    
        # Controle para o tipo de documentação
        st.subheader("Tipo de Documentação")
        st.session_state.documentation_type = st.segmented_control(
            "Selecione o objetivo da documentação:",
            options=["Técnica", "Negócio"],
            help=(
                "Documentação Técnica: Focada em detalhes técnicos, como classes, métodos e dependências.\n"
                "Documentação de Negócio: Focada em descrever o domínio e os objetivos de negócio."
            )
        )
    
        # Validação para garantir que o usuário selecione as opções
        if not st.session_state.execution_mode or not st.session_state.documentation_type:
            st.error("Por favor, selecione o modo de execução e o tipo de documentação antes de prosseguir.")
            st.stop()  # Interrompe a execução até que o usuário preencha os campos obrigatórios

    def manage_subdependencies(self, main_dependency_index):
        """Gerenciar subdependências de uma dependência principal."""
        st.sidebar.title(f"Gerenciar Subdependências - Dependência {main_dependency_index + 1}")
        main_dependency = st.session_state.dependencies[main_dependency_index]

        # Formulário para adicionar nova subdependência
        with st.sidebar.form(key=f"add_subdependency_form_{main_dependency_index}"):
            st.subheader("Adicionar Nova Subdependência")
            new_path = st.text_input("Caminho da Subdependência", placeholder="Exemplo: src/subdependency.py")
            new_methods = st.text_area("Métodos (separados por vírgula)").split(",")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                main_dependency["subdependencies"].append({
                    "path": new_path,
                    "methods": new_methods
                })
                st.success("Subdependência adicionada com sucesso!")
                st.rerun()

        # Exibir lista de subdependências
        st.sidebar.subheader("Subdependências Adicionadas")
        for i, subdependency in enumerate(main_dependency["subdependencies"]):
            st.sidebar.markdown(f"**{i + 1}. {subdependency.get('name', 'Nova Subdependência')}**")
            if st.sidebar.button(f"Excluir Subdependência {i + 1}", key=f"delete_sub_{main_dependency_index}_{i}"):
                main_dependency["subdependencies"].pop(i)
                st.rerun()

    def render_metadata_section(self):
        """Renderizar a seção de metadados."""
        with st.expander("Metadados", expanded=True):
            self.metadata = {
                "name": st.text_input("Nome do Domínio", ""),
                "description": st.text_area("Descrição do Domínio", "")
            }
    def search_file(self, query):
        """Buscar arquivos pelo nome."""
        if not query:
            return []
        query = query.lower()
        return [file for file in self.files_indexrs if query in file["file_name"].lower()]
    
    def render_main_class_section(self):
        """Renderizar a seção da classe principal."""
        with st.expander("Classe Principal", expanded=True):
            query = st.text_input("Pesquise pelo nome da Classe Principal", "")
            search_results = self.search_file(query)
            print(f"search_results: {search_results}, query: {query}")

            if search_results:
                selected_file = st.selectbox(
                    "Classe Principal Selecionada",
                    [file["file_name"] for file in search_results],
                    disabled=True
                )
                # Obter o caminho completo do arquivo selecionado
                selected_path = next(
                    (file["path"] for file in search_results if file["file_name"] == selected_file),
                    None
                )
                self.main_class = {
                    "path": selected_path,
                    "methods": st.text_area("Métodos da Classe Principal (separados por vírgula)").split(", ")
                }
                st.write(f"Caminho Selecionado: {selected_path}")
            else:
                st.write("Nenhum arquivo encontrado.")

    def render_dependencies_section(self):
        """Renderizar a seção de dependências principais."""
        if st.session_state.execution_mode == "Manual":
            st.header("Dependências Principais")
            for i, dependency in enumerate(st.session_state.dependencies):
                with st.expander(f"Dependência Principal {i + 1}", expanded=True):
                    query = st.text_input(
                        f"Pesquise pelo nome da Dependência {i + 1}",
                        key=f"dependency_search_{i}"
                    )
                    search_results = self.search_file(query)

                    if search_results:
                        selected_file = st.selectbox(
                            f"Selecione a Dependência {i + 1}:",
                            [file["file_name"] for file in search_results],
                            key=f"dependency_select_{i}"
                        )
                        # Obter o caminho completo do arquivo selecionado
                        selected_path = next(
                            (file["path"] for file in search_results if file["file_name"] == selected_file),
                            None
                        )
                        dependency["path"] = selected_path
                        dependency["methods"] = st.text_area(
                            f"Métodos da Dependência {i + 1} (separados por vírgula)",
                            ", ".join(dependency.get("methods", []))
                        ).split(",")
                        st.write(f"Caminho Selecionado: {selected_path}")
                    else:
                        st.write("Nenhum arquivo encontrado.")

                    if st.button(f"Gerenciar Subdependências {i + 1}", key=f"manage_sub_{i}"):
                        st.session_state.active_dependency_index = i

            # Gerenciar subdependências na sidebar
            if st.session_state.active_dependency_index is not None:
                self.manage_subdependencies(st.session_state.active_dependency_index)

    def render_actions(self):
        """Renderizar os botões de ação no final da página."""
        col1, col2 = st.columns(2)
        if st.session_state.execution_mode == "Manual":
            with col1:
                if st.button("Adicionar Dependência Principal"):
                    st.session_state.dependencies.append({
                        "path": "",
                        "methods": [],
                        "subdependencies": []
                    })
                    st.rerun()
        with col2:
            if st.button("Salvar Configurações"):
                if self.validate_inputs():
                    # Estrutura final
                    domain_structure = {
                        "metadata": self.metadata,
                        "main_class": self.main_class,
                        "dependencies": st.session_state.dependencies,
                        "execution_mode": st.session_state.execution_mode,
                        "documentation_type": st.session_state.documentation_type
                    }
                    st.success("Configurações salvas com sucesso!")
                    json_data = None
                    print(f"{self.main_class.get('path', None)}")
                    if st.session_state.execution_mode == "Automatizado":
                        json_data = self.class_processor.generate_json_report(self.main_class.get('path', None), 2)
                        # Certifique-se de que json_data seja um dicionário
                        if isinstance(json_data, str):
                            try:
                                json_data = json.loads(json_data)  # Converte a string JSON para um dicionário
                            except json.JSONDecodeError as e:
                                print(f"Erro ao decodificar JSON: {e}")
                                json_data = {}  # Define um dicionário vazio como fallback
                        domain_structure["dependencies"] = json_data.get('dependencies', {})
                    st.json(domain_structure)
                    self.file_processor.process_json(domain_structure)

    def render(self):
        """Renderizar toda a interface da documentação de negócio."""
        st.title("Documentações")
        self.handle_zip_upload()
        self.render_controls()  # Adicionar os controles no início
        self.render_metadata_section()
        self.render_main_class_section()
        self.render_dependencies_section()
        self.render_actions()
