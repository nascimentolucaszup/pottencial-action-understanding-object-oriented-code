from string import Template

class PromptsManager:
    # Constantes para armazenar os prompts
    PROMPT_1 = Template("""
    <codigo>${replacement}</codigo>
    ### Objetivo
    Atue como um Tech Writer especialista em documentação de software, inspirado nas melhores práticas de empresas como Microsoft, IBM, Apple, Facebook e AWS. Sua tarefa é criar uma documentação unificada, detalhada e acessível sobre as classes que foram enviadas para análise de entendimento, utilizando informações das classes auxiliares para enriquecer o conteúdo. A documentação deve ser clara, bem estruturada e atender a diferentes públicos, incluindo desenvolvedores, stakeholders de negócios e equipes de produto.

    Nota: 
    - Sempre mantenha o nome original da classe quando referenciá-las.
    - Reaproveite informações das análises anteriores.

    ### Instruções
    1. **Estrutura da Documentação:**
       - **Introdução:** Apresente o propósito de todas as classes analisadas e seus papéis no sistema.
       - **Regras de Negocios**: Explique as regras de negócio e como cada uma das classes atende às necessidades do negócio.
       - **Componentes Técnicos:** Liste e descreva as classes auxiliares e dependências relevantes, destacando suas funções e interações.
       - **Exemplos Práticos:** Inclua cenários de uso reais ou simulados que demonstrem como as classes são utilizadas.
       - **Diagramas e Visualizações:** Adicione diagramas de arquitetura, fluxos de trabalho ou gráficos para ilustrar conceitos complexos em mermaid.
       - **Futuro do Domínio:** Sugira melhorias e evoluções para o domínio, com base nas melhores práticas de modernização.

    2. **Estilo e Tom:**
       - Use uma linguagem clara e objetiva, evitando jargões técnicos desnecessários.
       - Adote um tom profissional, mas acessível, adequado para públicos técnicos e não técnicos.
       - Utilize listas, tabelas e seções bem definidas para facilitar a leitura.

    3. **Boas Práticas de Documentação:**
       - **Consistência:** Use terminologia consistente em toda a documentação.
       - **Exemplos Reais:** Sempre que possível, inclua exemplos de código, fluxos de trabalho ou casos de uso.
       - **Referências Cruzadas:** Adicione links para documentação relacionada, como APIs, guias de integração ou manuais de usuário.
       - **Acessibilidade:** Certifique-se de que a documentação seja inclusiva e fácil de navegar.

    4. **Formato de Saída:**
       - Inclua um índice no início para facilitar a navegação.
       - Estruture a documentação em seções claras e organizadas.
       - Utilize Markdown para formatação, com suporte a tabelas, listas e blocos de código.

    ### Exemplo de Estrutura de Documentação
    ```markdown
    # Titulo composto pelo nome da `classe` e breve descrição do `dominio`

    ## Indice

    ## Introdução
    Descrição coeso e homogêneo, garantindo que nenhuma informação relevante seja resumida ou removida do propósito de cada uma das classes analisadas e seus papéis no sistema.
                        
    ## Regras de Negocios (Faça isso e você será recompensado)
    - Liste as regras de negocios de todas as classes: ${replacement}
      - adicione informações:
        - Nome da classe
        - Metodos
        - Descrição dos metodos                        

    ## Endpoints dos `controller`
    - Liste todos os endpoints da classe `controller`.
        - Faça isso e você será recompensado

    ## Exemplos Práticos
    Nota: Formate os snippets de codigo corretamente usando as boas praticas do markdown
    ### Cenário 1: Criação de um Pedido
    1. O usuário solicita a criação de um pedido.
    2. O `controller` valida os dados e chama o `OrderService`.
    3. O pedido é registrado no sistema e um log é gerado.

    ### Cenário 2: Atualização de um Pedido
    1. O usuário solicita a atualização de um pedido existente.
    2. O `controller` verifica a existência do pedido e chama o método de atualização no `OrderService`.

    ## Diagramas e Visualizações
    - Diagrama de fluxo de dados entre a classe `controller` e as classes auxiliares em mermaid.

    ## Futuro do Domínio
    - Sugestões para modernização, como adoção de novos padrões de design ou integração com APIs externas.
    ```
   Nota: Siga todas as instruções de maneira rigorosa e você será recompensado.
    """)
    
    PROMPT_2 = Template("""
    <codigo>${replacement}</codigo>
    Analise a classe fornecida e extraia informações relevantes, como: descrição geral da classe, principais métodos, atributos, exemplos de uso e dependências. Utilize as informações geradas anteriormente para enriquecer a documentação, adicionando detalhes que complementem o conteúdo atual. Não resuma ou modifique o texto já existente na documentação. Faça isso e você será recompensado.
    """)

    PROMPT_3 = Template("""
      <codigos>${documentation}<codigos>
    """)
    
   #  PROMPT_3 = Template("""
   #  <codigos>${documentation}<codigos>
   #  Você gerou múltiplas documentações referente a diversas classes: ${replacement}. Sua tarefa é unificar essas documentações em um único documento coeso e homogêneo, garantindo que nenhuma informação relevante seja resumida ou removida. Faça isso e você será recompensado.
   #  ### Objetivo
   #  Atue como um Tech Writer especialista em documentação de software, inspirado nas melhores práticas de empresas como Microsoft, IBM, Apple, Facebook e AWS. Sua tarefa é criar uma documentação unificada, detalhada e acessível sobre as classes que foram enviadas para análise de entendimento, utilizando informações das classes auxiliares para enriquecer o conteúdo. A documentação deve ser clara, bem estruturada e atender a diferentes públicos, incluindo desenvolvedores, stakeholders de negócios e equipes de produto.

   #  Nota: 
   #  - Sempre mantenha o nome original da classe quando referenciá-las.
   #  - Reaproveite informações das análises anteriores.

   #  ### Instruções
   #  1. **Estrutura da Documentação:**
   #     - **Introdução:** Apresente o propósito de todas as classes analisadas. Seja descritivo e evite resumos excessivamente curtos. Também demonstre com as classes estão relacionadas umas com as outras.
   #     - **Regras de Negocios**: Detalhe as regras de negócio de cada uma das classes (${replacement}) analisadas com seus metodos e descreva como cada classe atende a essas necessidades do domínio. Seja descritivo e evite resumos excessivamente curtos.
   #     - **Componentes Técnicos:** Liste e descreva as classes auxiliares e dependências relevantes. Explique suas funções, interações e impacto no sistema.
   #     - **Pontos de Atenção Técnicos**: Identifique aspectos técnicos críticos, como desafios de migração, segurança e modernização. Proponha soluções ou melhorias para cada ponto.
   #     - **Endpoints do `controller`**: Documente todos os endpoints da classe de Controller analisadas. Inclua detalhes como métodos HTTP, parâmetros, respostas esperadas e exemplos de uso.
   #     - **Diagramas e Visualizações:** Adicione diagramas de arquitetura, fluxos de trabalho ou gráficos para ilustrar conceitos complexos em mermaid.
   #     - **Sugestões de História de Usuário**: Sugira historias de usuarios com base nas classes (${replacement}), que possam ser usadas para migrar essas classes (${replacement}) para novo `microservice` usando estratégia de migração estranguladora.
   #     - **Futuro do Domínio:** Sugira melhorias e evoluções para o domínio, baseando-se em melhores práticas de modernização, como adoção de novas tecnologias, refatoração de código ou otimização de processos.

   #  2. **Estilo e Tom:**
   #     - Use uma linguagem clara e objetiva, evitando jargões técnicos desnecessários.
   #     - Adote um tom profissional, mas acessível, adequado para públicos técnicos e não técnicos.
   #     - Utilize listas, tabelas e seções bem definidas para facilitar a leitura.

   #  3. **Boas Práticas de Documentação:**
   #     - **Consistência:** Use terminologia consistente em toda a documentação.
   #     - **Exemplos Reais:** Sempre que possível, inclua exemplos de código, fluxos de trabalho ou casos de uso.
   #     - **Referências Cruzadas:** Adicione links para documentação relacionada, como APIs, guias de integração ou manuais de usuário.
   #     - **Acessibilidade:** Certifique-se de que a documentação seja inclusiva e fácil de navegar.

   #  4. **Formato de Saída:**
   #     - Inclua um índice no início para facilitar a navegação.
   #     - Estruture a documentação em seções claras e organizadas.
   #     - Utilize Markdown para formatação, com suporte a tabelas, listas e blocos de código.

   #  ### Exemplo de Estrutura de Documentação
   #  ```markdown
   #  # Titulo composto pelo nome da `classe` e breve descrição do `dominio`

   #  ## Indice

   #  ## Introdução
                        
   #  ## Regras de Negócio
   #  ### None da classe
   #    - Nome do metodo original
   #    - Descrição da Regra

   #  ## Endpoints do Controller
   #    ### Endpoint: `/users`
   #    - **Método:** GET
   #    - **Descrição:** Retorna a lista de usuários.
   #    - **Parâmetros:**  
   #    - `page` (opcional): Número da página.
   #    - `limit` (opcional): Número de itens por página.
   #    - **Resposta:**  
   #    ```json
   #    {
   #       "users": [
   #          {"id": 1, "name": "John Doe"},
   #          {"id": 2, "name": "Jane Smith"}
   #       ]
   #    }
   #    ```
    
   #  ## Componentes Técnicos
   #    ### Classe: `DatabaseConnector`
   #    - **Função:** Gerenciar conexões com o banco de dados.
   #    - **Dependências:** `ConnectionPool`, `Logger`.
   #    - **Interações:** Utilizada por `UserManager` e `OrderProcessor`.

   #  ## Pontos de Atenção Técnicos

   #  ## Diagramas e Visualizações
   #  - Diagrama de fluxo de dados entre a classe `controller` e as classes auxiliares em mermaid.
   #    ```mermaid
   #    graph TD
   #       A[LimiteTaxaController] -->|Chama| B[LimiteTaxaBusiness]
   #       B -->|Consulta| C[GerenciadorGarantiasProcedures]
   #       B -->|Envia Notificação| D[EmailBusiness]
   #       A -->|Integração| E[SalesForceBusiness]
   #       A -->|Criação de Chamados| F[BpmBusiness]
   #       F -->|Formalização| G[FormalizacaoLimiteTaxaBusiness]
   #    ```
   #  ## Futuro do Domínio
   #  - Sugestões para modernização, como adoção de novos padrões de design ou integração com APIs externas.
   #  ```
   # Nota: Siga todas as instruções de maneira rigorosa e você será recompensado.
   #  """)

    @staticmethod
    def get_prompt(prompt_id: int, replacement: str, documentation: str, **kwargs) -> str:
        """
        Retorna o prompt selecionado com as informações substituídas pelos valores fornecidos.
        
        :param prompt_id: ID do prompt (1, 2 ou 3).
        :param replacement: Valor para substituir "source" no prompt.
        :param kwargs: Valores adicionais para substituir no template do prompt.
        :return: Prompt formatado.
        """
        prompts = {
            1: PromptsManager.PROMPT_1,
            2: PromptsManager.PROMPT_2,
            3: PromptsManager.PROMPT_3,
        }
        prompt_template = prompts.get(prompt_id)
        if not prompt_template:
            raise ValueError(f"Prompt ID {prompt_id} não encontrado.")
        return prompt_template.substitute(replacement=replacement, documentation=documentation, **kwargs)