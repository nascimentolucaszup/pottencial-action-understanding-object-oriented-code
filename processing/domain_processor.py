import yaml
from typing import List, Optional


class Dependency:
    def __init__(self, name: str, path: str, description: str, methods: Optional[List[str]] = None, dependencies: Optional[List['Dependency']] = None):
        self.name = name
        self.path = path
        self.description = description
        self.methods = methods or []
        self.dependencies = dependencies or []

    def __repr__(self):
        return (f"Dependency(name={self.name}, path={self.path}, description={self.description}, "
                f"methods={self.methods}, dependencies={self.dependencies})")


class MainDomain:
    def __init__(self, name: str, path: str, description: str, methods: Optional[List[str]] = None, dependencies: Optional[List[Dependency]] = None):
        self.name = name
        self.path = path
        self.description = description
        self.methods = methods or []
        self.dependencies = dependencies or []

    def __repr__(self):
        return (f"MainDomain(name={self.name}, path={self.path}, description={self.description}, "
                f"methods={self.methods}, dependencies={self.dependencies})")


class DomainLoader:
    @staticmethod
    def load_from_yaml(file_path: str) -> MainDomain:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        main_class_data = data['spec']['main-class']
        dependencies = DomainLoader._parse_dependencies(main_class_data.get('dependencies', []))

        return MainDomain(
            name=main_class_data['name'],
            path=main_class_data['path'],
            description=main_class_data['description'],
            methods=main_class_data.get('methods', []),
            dependencies=dependencies
        )

    @staticmethod
    def _parse_dependencies(dependencies_data: List[dict]) -> List[Dependency]:
        dependencies = []
        for dep in dependencies_data:
            sub_dependencies = DomainLoader._parse_dependencies(dep.get('dependencies', []))
            dependencies.append(Dependency(
                name=dep['name'],
                path=dep['path'],
                description=dep['description'],
                methods=dep.get('methods', []),
                dependencies=sub_dependencies
            ))
        return dependencies


# Exemplo de uso
if __name__ == "__main__":
    # Salve o YAML atualizado em um arquivo chamado "domain.yaml" antes de executar este código
    domain = DomainLoader.load_from_yaml("domain.yaml")
    print(domain)