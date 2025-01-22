import re

class FileHandlerProcessor:
    def __init__(self):
        """
        Inicializa a classe com o código a ser processado.
        """
        self.code = None

    def initialize(self, code: str):
        self.code = code

    def remove_comments(self):
        """
        Remove comentários de uma string de código.
        """
        # Remove comentários de linha (// ou #)
        self.code = re.sub(r'#.*', '', self.code)
        self.code = re.sub(r'//.*', '', self.code)
        # Remove comentários de bloco (/* */)
        self.code = re.sub(r'/\*.*?\*/', '', self.code, flags=re.DOTALL)

    def remove_dead_code(self):
        """
        Remove funções ou métodos não utilizados (código morto).
        """
        # Encontra todas as funções/métodos definidos
        functions = re.findall(r'def\s+(\w+)\s*\(', self.code)
        used_functions = set()

        # Verifica quais funções são chamadas no código
        for func in functions:
            if re.search(rf'\b{func}\s*\(', self.code):
                used_functions.add(func)

        # Remove funções não utilizadas
        for func in functions:
            if func not in used_functions:
                self.code = re.sub(rf'def\s+{func}\s*\(.*?\):.*?(?=def|\Z)', '', self.code, flags=re.DOTALL)

    def minify_code(self):
        """
        Minifica o código, removendo espaços desnecessários e colocando tudo em uma única linha.
        """
        # Remove quebras de linha e espaços extras
        self.code = re.sub(r'\s+', ' ', self.code).strip()

    def remove_using_lines_code(self) -> str:
        # Define o padrão para capturar linhas que começam com "using" e terminam com ";"
        pattern = r"^using\s+[a-zA-Z0-9_.]+;\s*$"
        # Usa re.sub para substituir as linhas que correspondem ao padrão por uma string vazia
        cleaned_code = re.sub(pattern, "", self.code, flags=re.MULTILINE)
        # Remove linhas em branco extras
        cleaned_code = re.sub(r"^\s*\n", "", cleaned_code, flags=re.MULTILINE)
        self.code = cleaned_code

    def process(self):
        """
        Processa o código para remover comentários, código morto e minificá-lo.
        """
        self.remove_using_lines_code()
        self.remove_comments()
        self.remove_dead_code()
        self.minify_code()
        return self.code
