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
    dependencies: List[Dict] = None  # Lista de dependências aninhadas

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
                # print(f"content: {content}")

            clean_content = self._remove_comments(content)
            for pattern in ['object_instantiation', 'inheritance']:
                matches = re.findall(self._patterns[pattern], clean_content)
                dependencies.update(matches)
                # print(f"dependencies: {dependencies}")

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
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.class_analyzer = CSharpClassAnalyzer()
        self.class_files: Dict[str, str] = {}

    def initialize(self):
        """Mapeia todas as classes do projeto para seus arquivos"""
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    class_name = self._extract_class_name(file_path)
                    if class_name:
                        self.class_files[class_name] = file_path

    def analyze_dependencies_tree(self, file_path: str, max_depth: int = 0, current_depth: int = 0) -> Optional[ClassDependency]:
        """Analisa recursivamente as dependências de uma classe"""
        if current_depth > max_depth:
            return None

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
                    dependency_objects.append({
                        "class_name": nested_dependency.name,
                        "file_path": nested_dependency.file_path,
                        "dependencies": nested_dependency.dependencies
                    })

        return ClassDependency(
            name=class_name,
            file_path=file_path,
            dependencies=dependency_objects
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
            # or file_path.endswith("Repository.cs")

    def generate_controller_json_report(self, controller_dependency: ClassDependency) -> str:
        """Gera um relatório JSON focado no controller e suas dependências"""
        if not controller_dependency:
            return json.dumps({"error": "Controller dependency not found"}, indent=2)

        controller_json = {
            "controller": {
                "name": controller_dependency.name,
                "file_path": controller_dependency.file_path,
                "dependencies": controller_dependency.dependencies
            }
        }
        return json.dumps(controller_json, indent=2)