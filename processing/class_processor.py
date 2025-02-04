import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import json
from rapidfuzz import process, fuzz

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
            'object_instantiation': r'new\s+([\w\.]+)\s*(?:\{[^}]*}|\([^\)]*\))?',
            'inheritance': r':\s*(\w+)',
            'using': r"using\s+[\w\.]+\.([\w]+);",
            'class_references': r"typeof\(([\w\.]+)\)|new\s+([\w\.]+)\(|private readonly ([\w\.<>]+)",
            'generic': r"([\w\.]+)<([\w\.]+)>",
        }

    def extract_classes(self, file_path: str) -> List[str]:
        """Extrai dependências de uma classe"""
        dependencies = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                clean_content = self._remove_comments(content)
                
                # Aplicar os padrões de regex para capturar dependências
                for pattern_name, pattern in self._patterns.items():
                    matches = re.findall(pattern, clean_content)
                    for match in matches:
                        # Adicionar todas as capturas não vazias
                        dependencies.update(filter(None, match))
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

def find_similar_matches(query, files, threshold=60):
    """Busca arquivos similares com base no nome"""
    file_names = [file["file_name"] for file in files]
    matches = process.extract(
        query,
        file_names,
        scorer=fuzz.token_set_ratio,
        score_cutoff=threshold,
    )
    results = []
    for match in matches:
        matched_file_name, score, index = match
        results.append({
            "match": files[index],
            "score": score
        })
    return results

# Função auxiliar para limpar nomes de arquivos
def clean_file_name(file_name, stop_words):
    # Remove a extensão do arquivo
    file_name = re.sub(r'\.\w+$', '', file_name)
    
    # Remove as stop_words (case insensitive) em qualquer lugar da sentença
    for word in stop_words:
        pattern = re.compile(re.escape(word), flags=re.IGNORECASE)
        file_name = pattern.sub('', file_name)
    
    # Remove caracteres extras como hífens, underscores e espaços duplicados
    file_name = re.sub(r'[-_.\s]+', ' ', file_name).strip()
    
    return file_name

class CSharpDependencyAnalyzer:
    def __init__(self, json_data: List[Dict[str, str]]):
        self.json_data = json_data
        self.class_analyzer = CSharpClassAnalyzer()
        self.class_files: Dict[str, str] = self._map_classes_from_json()
        self.visited_files = set()  # Rastreamento de arquivos já processados
        self.main_class_name: Optional[str] = None  # Nome da classe principal para análise de similaridade
        self.stop_words = [
            "controller", "model", "view", "api", "service", "resource", "event", "handler",
            "listener", "microservice", "gateway", "proxy", "repository", "entity", "dto",
            "dao", "aggregate", "valueobject", "factory", "specification", "test", "spec",
            "mock", "stub", "fixture", "component", "directive", "module", "widget",
            "middleware", "interceptor", "adapter", "logger", "monitor", "metrics", "auth",
            "authorization", "authentication", "token", "config", "settings", "env",
            "deployment", "schema", "migration", "seeder", "index", "layout", "template",
            "style", "theme", "helper", "util", "common", "base", "core", "Controller", "Model", "View", "Api", "Service", "Resource", "Event", "Handler",
            "Listener", "Microservice", "Gateway", "Proxy", "Repository", "Entity", "Dto",
            "Dao", "Aggregate", "Valueobject", "Factory", "Specification", "Test", "Spec",
            "Mock", "Stub", "Fixture", "Component", "Directive", "Module", "Widget",
            "Middleware", "Interceptor", "Adapter", "Logger", "Monitor", "Metrics", "Auth",
            "Authorization", "Authentication", "Token", "Config", "Settings", "Env",
            "Deployment", "Schema", "Migration", "Seeder", "Index", "Layout", "Template",
            "Style", "Theme", "Helper", "Util", "Common", "Base", "Core"
        ]

    def _map_classes_from_json(self) -> Dict[str, str]:
        """Mapeia as classes para seus arquivos com base no JSON"""
        class_files = {}
        for entry in self.json_data:
            file_path = entry['path']
            class_name = self._extract_class_name(file_path)
            if class_name:
                class_files[class_name] = file_path
        return class_files

    def analyze_dependencies_tree(self, file_path: str, max_depth: int = 0, current_depth: int = 0, selected_patterns = []) -> Optional[Dependency]:
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

        # Definir a classe principal para análise de similaridade na primeira execução
        if current_depth == 0:
            self.main_class_name = class_name

        # Busca dependências por regex
        regex_dependencies = self.class_analyzer.extract_classes(file_path)
        # Busca dependências por similaridade com base na main_class_name
        similar_dependencies = self._find_similar_dependencies(self.main_class_name)

        dependency_objects = []
        
        # Processar dependências encontradas por regex
        for dep_class in regex_dependencies:
            dep_file_path = self.class_files.get(dep_class)
            if dep_file_path and self._is_valid_dependency(dep_file_path, selected_patterns=selected_patterns):
                nested_dependency = self.analyze_dependencies_tree(dep_file_path, max_depth, current_depth + 1, selected_patterns=selected_patterns)
                if nested_dependency:
                    dependency_objects.append(nested_dependency)

        # Processar dependências encontradas por similaridade
        for dep in similar_dependencies:
            dep_file_path = dep["match"]["path"]
            if self._is_valid_dependency(dep_file_path, selected_patterns=selected_patterns):
                nested_dependency = self.analyze_dependencies_tree(dep_file_path, max_depth, current_depth + 1, selected_patterns=selected_patterns)
                if nested_dependency:
                    dependency_objects.append(nested_dependency)

        return Dependency(
            path=file_path,
            methods=[],  # Métodos podem ser extraídos se necessário
            subdependencies=dependency_objects
        )

    def _find_similar_dependencies(self, main_class_name: str) -> List[Dict]:
        """Encontra dependências similares usando a função find_similar_matches"""
        print(f"main_class: {clean_file_name(main_class_name, self.stop_words)}")
        if not main_class_name:
            return []
        files = [{"file_name": key, "path": value} for key, value in self.class_files.items()]
        print(f"similares: {find_similar_matches(clean_file_name(main_class_name, self.stop_words), files, threshold=60)}")
        return find_similar_matches(clean_file_name(main_class_name, self.stop_words), files, threshold=60)

    def _extract_class_name(self, file_path: str) -> Optional[str]:
        """Extrai o nome da classe principal do arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                match = re.search(r'class\s+(\w+)', content)
                return match.group(1) if match else None
        except Exception:
            return None
        
    def _is_valid_dependency(self, file_path: str, selected_patterns = []) -> bool:
        """Verifica se o arquivo atende aos padrões desejados"""
        # Lista de palavras-chave que indicam dependências válidas
        print(f"selected patterns: {selected_patterns}")
        keywords = selected_patterns
        
        # Extrai o nome do arquivo sem o caminho completo
        # file_name = file_path.split("/")[-1]  # Para sistemas Unix-like
        # file_name = file_path.split("\")[-1]  # Para sistemas Windows (se necessário)
        
        # Remove a extensão do arquivo, se houver
        file_name = re.sub(r'\.\w+$', '', file_path)
        
        # Verifica se alguma das palavras-chave está presente no nome do arquivo (case insensitive)
        return any(re.search(rf'\b{keyword}\b', file_name, flags=re.IGNORECASE) for keyword in keywords)

    def generate_json_report(self, main_class_path: str, max_depth: int = 0, selected_patterns = []) -> str:
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
        dependencies = self.analyze_dependencies_tree(main_class_path, max_depth=max_depth, selected_patterns=selected_patterns)
        
        dependency_tree = DependencyTree(
            main_class=main_class,
            dependencies=dependencies.subdependencies if dependencies else []
        )
        return json.dumps(dependency_tree, default=lambda o: o.__dict__, indent=2)