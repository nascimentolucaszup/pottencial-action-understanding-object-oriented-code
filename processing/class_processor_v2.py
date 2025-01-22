import os
import re
from typing import Set, Optional, Dict, List
from dataclasses import dataclass
import json

@dataclass
class ClassDependency:
    """Armazena informações de dependência de classes"""
    name: str
    file_path: str
    dependencies: Dict[str, Set[str]]
    interfaces: Set[str] = None  
    level: int = 0

@dataclass
class ImplementationInfo:
    """Armazena informações sobre implementação de interface"""
    class_name: str
    file_path: str
    dependencies: Dict[str, Set[str]]

class CSharpClassAnalyzer:
    def __init__(self):
        self._patterns = {
            'main_class': r'class\s+(\w+)',
            'variable_declaration': r'(\w+)\s+\w+\s*[=;]',
            'generic_declaration': r'(\w+<\w+>)',
            'object_instantiation': r'new\s+(\w+)\s*\(([^)]*)\)',
            'inheritance': r':\s*(\w+)',
            'using_statement': r'using\s+([^;]+);',
            'static_usage': r'(\w+)\.\w+\s*\(|(\w+)\.\w+\s*[^(]',
            'interface_implementation': r'class\s+\w+\s*:\s*(.*?)(?:{|$)'
        }

    def extract_classes(self, file_path: str) -> Dict[str, Set[str]]:
        """Extrai informações sobre classes e interfaces implementadas"""
        dependencies = {'instance': set(), 'static': set(), 'inheritance': set(), 'interfaces': set()}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            clean_content = self._remove_comments(content)
            main_class = self._find_main_class(clean_content)

            self._process_dependencies(clean_content, main_class, dependencies)

        except FileNotFoundError:
            print(f"Erro: Arquivo {file_path} não encontrado")
        except Exception as e:
            print(f"extract_classes -> Erro ao processar arquivo: {str(e)}")

        return dependencies

    def _process_dependencies(self, content: str, main_class: Optional[str], dependencies: Dict[str, Set[str]]) -> None:
        """Processa todas as dependências de uma classe."""
        seen_classes = set()
        for pattern_name, pattern in self._patterns.items():
            if pattern_name in ['main_class', 'interface_implementation']:
                continue

            for match in re.finditer(pattern, content):
                class_name = self._sanitize_generic_class_name(match.group(1))
                if class_name and class_name not in seen_classes:
                    seen_classes.add(class_name)
                    if class_name.startswith('I'):
                        dependencies['interfaces'].add(class_name)
                    elif self._is_valid_dependency(class_name, main_class):
                        dependencies[self._get_dependency_type(pattern_name)].add(class_name)
    
    def _sanitize_generic_class_name(self, class_name: Optional[str]) -> str:
        """Converte a definição genérica do nome da classe para '<T>' se existir."""
        if class_name is None:
            return ""
        return re.sub(r'<.*?>', '', class_name).strip()

    def _get_dependency_type(self, pattern_name: str) -> str:
        """Determina o tipo de dependência baseado no padrão."""
        if pattern_name == 'inheritance':
            return 'inheritance'
        if pattern_name in ['variable_declaration', 'object_instantiation']:
            return 'instance'
        return 'static'

    def _remove_comments(self, content: str) -> str:
        """Remove comentários do código fonte."""
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        return content

    def _is_valid_dependency(self, name: str, main_class: Optional[str]) -> bool:
        """Cheque se uma dependência é válida."""
        return (
            self._is_valid_class_name(name)
            and name != main_class
            and not self._is_config_pattern(name)
        )

    def _find_main_class(self, content: str) -> Optional[str]:
        """Identifica o nome da classe principal do arquivo."""
        main_class_match = re.search(self._patterns['main_class'], content)
        return main_class_match.group(1) if main_class_match else None

    def _is_config_pattern(self, name: str) -> bool:
        """Verifica se o nome é um padrão de configuração."""
        return ':' in name

    def _is_valid_class_name(self, name: str) -> bool:
        """Verifica se o nome encontrado é de uma classe válida."""
        invalid_words = {'var', 'void', 'int', 'string', 'bool', 'float', 'double', 'decimal'}
        return (
            name
            and name not in invalid_words
            and name[0].isupper()
            and name.isalnum()
        )

class CSharpDependencyAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.class_analyzer = CSharpClassAnalyzer()
        self.processed_classes: Dict[str, ClassDependency] = {}
        self.class_files: Dict[str, str] = {}
        self.processed_class_implementations = set()

    def initialize(self):
        """Mapeia todas as classes do projeto para seus arquivos"""
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    class_name = self._extract_class_name(file_path)
                    if class_name:
                        self.class_files[class_name] = file_path

    def analyze_dependencies_tree(self, controller_path: str, max_depth: int = 10) -> ClassDependency:
        """Analisa a árvore de dependências começando de um controller."""
        self.initialize()
        self._process_file(controller_path, 0, max_depth)
        main_class_name = self._extract_class_name(controller_path)
        return self.processed_classes.get(main_class_name, None)

    def _process_file(self, file_path: str, current_level: int, max_depth: int) -> None:
        """Processa recursivamente um arquivo e suas dependências."""
        if current_level >= max_depth:
            return

        class_name = self._extract_class_name(file_path)
        if class_name and class_name not in self.processed_classes:
            dependencies = self.class_analyzer.extract_classes(file_path)
            interfaces = dependencies.get('interfaces', set())
            dependencies.pop('interfaces')
            self.processed_classes[class_name] = ClassDependency(
                name=class_name,
                file_path=file_path,
                dependencies=dependencies,
                interfaces=interfaces,
                level=current_level
            )

            for dep_class in set().union(*dependencies.values()):
                if dep_class in self.class_files:
                    self._process_file(self.class_files[dep_class], current_level + 1, max_depth)

    def _extract_class_name(self, file_path: str) -> Optional[str]:
        """Extrai o nome da classe principal do arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return self.class_analyzer._find_main_class(content)
        except Exception:
            return None

    def generate_controller_json_report(self, controller_dependency: ClassDependency) -> str:
        """Gera um relatório JSON focado no controller e suas dependências"""
        if not controller_dependency:
            return json.dumps({"error": "Controller dependency not found"}, indent=2)

        # Preparar a lista de classes dependentes com seus paths
        dependent_classes = [
            {
                "class_name": dep_class,
                "file_path": self.class_files.get(dep_class, "Unknown")
            }
            for dep_class in set().union(*controller_dependency.dependencies.values())
        ]

        # Preparar a lista de interfaces com suas implementações e paths
        interface_implementations = []
        seen_implementations = set()  # Para rastrear implementações já vistas e evitar duplicatas
        for interface in controller_dependency.interfaces:
            implementations = self.find_interface_implementations(interface)
            for impl in implementations:
                impl_key = (interface, impl.class_name, impl.file_path)  # Chave única para identificar implementações
                if impl_key not in seen_implementations:
                    seen_implementations.add(impl_key)
                    dependent_classes.append({
                        "class_name": impl.class_name,
                        "file_path": impl.file_path
                    })

        controller_json = {
            "controller": {
                "name": controller_dependency.name,
                "file_path": controller_dependency.file_path,
                "dependencies": self.remove_duplicates_by_key(self.remove_unknown_values(dependent_classes), 'class_name'),
            }
        }
        return json.dumps(controller_json, indent=2)
    
    def remove_duplicates_by_key(self, lista_dicts, key_field):
        seen = set()
        unique_dicts = []
        
        for d in lista_dicts:
            # Usa um campo específico como chave de comparação
            if d[key_field] not in seen:
                seen.add(d[key_field])
                unique_dicts.append(d)
        
        return unique_dicts
    
    def remove_unknown_values(self, data):
        """
        Remove elementos que contenham 'Unknown' de uma lista de dicionários
        
        Args:
            data (list): Lista de dicionários para filtrar
            
        Returns:
            list: Nova lista sem elementos contendo 'Unknown'
        """
        if not data:
            return []
        
        # Remove dicionários que contenham 'Unknown' em qualquer valor
        return [
            item for item in data 
            if 'Unknown' not in item.values() 
            and None not in item.values()
        ]

    def find_interface_implementations(self, interface_name: str) -> List[ImplementationInfo]:
        """Encontra todas as implementações de uma interface específica"""
        self.initialize()
        implementations = []

        interface_pattern = re.compile(rf'class\s+(\w+(?:<.*?>)?)\s*:\s*[^:]*\b{interface_name}\b', re.M)

        for file_path in self.class_files.values():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if interface_pattern.search(content):
                        class_name = self.class_analyzer._find_main_class(content)
                        if class_name and class_name not in self.processed_class_implementations:
                            dependencies = self.class_analyzer.extract_classes(file_path)
                            implementations.append(ImplementationInfo(
                                class_name=class_name,
                                file_path=file_path,
                                dependencies=dependencies
                            ))
            except Exception as e:
                print(f"Erro ao processar arquivo {file_path}: {str(e)}")
        
        return implementations

# Exemplo de uso atualizado
if __name__ == "__main__":
    project_path = "./ASPNETCore-WebAPI-Sample-main/SampleWebApiAspNetCore"
    
    analyzer = CSharpDependencyAnalyzer(project_path)

    controller_path = "./ASPNETCore-WebAPI-Sample-main/SampleWebApiAspNetCore/Controllers/v1/FoodsController.cs"
    controller_dependency = analyzer.analyze_dependencies_tree(controller_path, max_depth=5)
    
    json_report = analyzer.generate_controller_json_report(controller_dependency)
    
    print("=== Controller JSON Report ===")
    print(json_report)
    
    # Salvando relatório JSON
    with open("controller_dependency_report.json", "w") as f:
        f.write(json_report)
