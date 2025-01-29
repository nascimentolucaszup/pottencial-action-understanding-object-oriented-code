import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class Dependency:
    """Representa uma dependência de classe"""
    path: str
    methods: List[str]
    subdependencies: List['Dependency']

@dataclass
class MainClass:
    """Representa a classe principal"""
    path: str
    methods: List[str]

@dataclass
class DependencyTree:
    """Representa a estrutura completa do JSON"""
    main_class: MainClass
    dependencies: List[Dependency]

class CSharpClassAnalyzer:
    def __init__(self):
        self._patterns = {
            'main_class': r'class\s+(\w+)',
            'object_instantiation': r'new\s+(\w+(?:<[\w,<>]+>)?)\s*\(',
            'inheritance': r':\s*(\w+)',
        }

    def extract_classes(self, file_path: str) -> List[str]:
        """Extrai dependências de uma classe"""
        dependencies = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                clean_content = self._remove_comments(content)
                for pattern in ['object_instantiation', 'inheritance']:
                    matches = re.findall(self._patterns[pattern], clean_content)
                    dependencies.update(matches)
        except FileNotFoundError:
            print(f"Erro: Arquivo {file_path} não encontrado")
        except Exception as e:
            print(f"Erro ao processar arquivo {file_path}: {str(e)}")
        return list(dependencies)

    def _remove_comments(self, content: str) -> str:
        """Remove comentários do código fonte"""
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        return content

class CSharpDependencyAnalyzer:
    def __init__(self, json_data: List[Dict[str, str]]):
        self.json_data = json_data
        self.class_analyzer = CSharpClassAnalyzer()
        self.class_files: Dict[str, str] = self._map_classes_from_json()
        self.visited_files = set()  # Rastreamento de arquivos já processados

    def _map_classes_from_json(self) -> Dict[str, str]:
        """Mapeia as classes para seus arquivos com base no JSON"""
        class_files = {}
        for entry in self.json_data:
            file_path = entry['path']
            class_name = self._extract_class_name(file_path)
            if class_name:
                class_files[class_name] = file_path
        return class_files

    def analyze_dependencies_tree(self, file_path: str, max_depth: int = 0, current_depth: int = 0) -> Optional[Dependency]:
        """Analisa recursivamente as dependências de uma classe"""
        if current_depth > max_depth:
            return None

        # Evitar processar o mesmo arquivo mais de uma vez
        if file_path in self.visited_files:
            return None
        self.visited_files.add(file_path)

        class_name = self._extract_class_name(file_path)
        if not class_name:
            return None

        dependencies = self.class_analyzer.extract_classes(file_path)
        dependency_objects = []
        for dep_class in dependencies:
            dep_file_path = self.class_files.get(dep_class)
            if dep_file_path and self._is_valid_dependency(dep_file_path):
                nested_dependency = self.analyze_dependencies_tree(dep_file_path, max_depth, current_depth + 1)
                if nested_dependency:
                    dependency_objects.append(nested_dependency)

        return Dependency(
            path=file_path,
            methods=[],  # Métodos podem ser extraídos se necessário
            subdependencies=dependency_objects
        )

    def _extract_class_name(self, file_path: str) -> Optional[str]:
        """Extrai o nome da classe principal do arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                match = re.search(self.class_analyzer._patterns['main_class'], content)
                return match.group(1) if match else None
        except Exception:
            return None
        
    def _is_valid_dependency(self, file_path: str) -> bool:
        """Verifica se o arquivo atende aos padrões desejados"""
        return file_path.endswith("Business.cs") or file_path.endswith("Service.cs") 

    def generate_json_report(self, main_class_path: str, max_depth: int = 0) -> str:
        """Gera o JSON na estrutura solicitada"""
        main_class_name = self._extract_class_name(main_class_path)
        if not main_class_name:
            return json.dumps({"error": "Main class not found"}, indent=2)

        main_class = MainClass(
            path=main_class_path,
            methods=[]  # Métodos podem ser extraídos se necessário
        )

        # Limpar o conjunto de arquivos visitados antes de iniciar a análise
        self.visited_files.clear()
        dependencies = self.analyze_dependencies_tree(main_class_path, max_depth=max_depth)

        dependency_tree = DependencyTree(
            main_class=main_class,
            dependencies=dependencies.subdependencies if dependencies else []
        )
        return json.dumps(dependency_tree, default=lambda o: o.__dict__, indent=2)
