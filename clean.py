import re

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

# Exemplo de uso
stop_words = [
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

# Testando a função
file_names = [
    "LimiteTaxaController.cs",
    "user-controller-service.py",
    "user.controller.ts",
    "user.repository.ts"
]

cleaned_names = [clean_file_name(name, stop_words) for name in file_names]
print(cleaned_names)