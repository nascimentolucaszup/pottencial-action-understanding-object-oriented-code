import streamlit as st

class BusinessDocumentation:
    def __init__(self, file_processor):
        # Inicializar estado
        if "dependencies" not in st.session_state:
            st.session_state.dependencies = []
        if "active_dependency_index" not in st.session_state:
            st.session_state.active_dependency_index = None
        self.file_processor = file_processor

    def manage_subdependencies(self, main_dependency_index):
        """Gerenciar subdependências de uma dependência principal."""
        st.sidebar.title(f"Gerenciar Subdependências - Dependência {main_dependency_index + 1}")
        main_dependency = st.session_state.dependencies[main_dependency_index]

        # Formulário para adicionar nova subdependência
        with st.sidebar.form(key=f"add_subdependency_form_{main_dependency_index}"):
            st.subheader("Adicionar Nova Subdependência")
            new_path = st.text_input("Caminho da Subdependência", placeholder="Exemplo: src/subdependency.py")
            new_description = st.text_area("Descrição da Subdependência")
            new_methods = st.text_area("Métodos (separados por vírgula)").split(",")
            submitted = st.form_submit_button("Adicionar")

            if submitted:
                main_dependency["subdependencies"].append({
                    "path": new_path,
                    "description": new_description,
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

    def render_main_class_section(self):
        """Renderizar a seção da classe principal."""
        with st.expander("Classe Principal", expanded=True):
            self.main_class = {
                "path": st.text_input("Caminho da Classe Principal", placeholder="Exemplo: src/main_class.py"),
                "description": st.text_area("Descrição da Classe Principal", ""),
                "methods": st.text_area("Métodos da Classe Principal (separados por vírgula)").split(", ")
            }

    def render_dependencies_section(self):
        """Renderizar a seção de dependências principais."""
        st.header("Dependências Principais")
        for i, dependency in enumerate(st.session_state.dependencies):
            with st.expander(f"Dependência Principal {i + 1}", expanded=True):
                dependency["path"] = st.text_input(
                    f"Caminho da Dependência {i + 1}",
                    dependency.get("path", ""),
                    placeholder="Exemplo: src/dependency.py"
                )
                dependency["description"] = st.text_area(f"Descrição da Dependência {i + 1}", dependency.get("description", ""))
                dependency["methods"] = st.text_area(
                    f"Métodos da Dependência {i + 1} (separados por vírgula)",
                    ", ".join(dependency.get("methods", []))
                ).split(",")

                if st.button(f"Gerenciar Subdependências {i + 1}", key=f"manage_sub_{i}"):
                    st.session_state.active_dependency_index = i

        # Gerenciar subdependências na sidebar
        if st.session_state.active_dependency_index is not None:
            self.manage_subdependencies(st.session_state.active_dependency_index)

    def render_actions(self):
        """Renderizar os botões de ação no final da página."""
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Adicionar Dependência Principal"):
                st.session_state.dependencies.append({
                    "path": "",
                    "description": "",
                    "methods": [],
                    "subdependencies": []
                })
                st.rerun()

        with col2:
            if st.button("Salvar Configurações"):
                # Estrutura final
                domain_structure = {
                    "metadata": self.metadata,
                    "main_class": self.main_class,
                    "dependencies": st.session_state.dependencies
                }
                st.success("Configurações salvas com sucesso!")
                st.json(domain_structure)
                self.file_processor.process_json(domain_structure)

    def render(self):
        """Renderizar toda a interface da documentação de negócio."""
        st.title("Documentação de Negócio")
        self.render_metadata_section()
        self.render_main_class_section()
        self.render_dependencies_section()
        self.render_actions()