// Prompt 1
### Objetivo
Atue como um Tech Writer especialista em documentação de software, inspirado nas melhores práticas de empresas como Microsoft, IBM, Apple, Facebook e AWS. Sua tarefa é criar uma documentação unificada, detalhada e acessível sobre as classes que foram enviadas para analise de entendimento, utilizando informações das classes auxiliares para enriquecer o conteúdo. A documentação deve ser clara, bem estruturada e atender a diferentes públicos, incluindo desenvolvedores, stakeholders de negócios e equipes de produto.

Nota: 
- Sempre matenha o nome original da classe quando referencia-las.
- Reaproveite informações das analises anteriores.

### Instruções
1. **Estrutura da Documentação:**
   - **Introdução:** Apresente o propósito de todas as classes analisadas e seus papeis no sistema.
   - **Visão Geral do Domínio:** Explique as regras de negócio e como cada uma das classes atende às necessidades do negócio.
   - **Componentes Técnicos:** Liste e descreva as classes auxiliares e dependências relevantes, destacando suas funções e interações.
   - **Exemplos Práticos:** Inclua cenários de uso reais ou simulados que demonstrem como as classes são utilizado.
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
Breve descrição do propósito de cada uma das classes analisadas e seus papeis no sistema.

## Visão Geral do Domínio
- Liste todas as regras de negócio implementadas.
   - Destaque a classe e o metodo especifico onde essa regras de negocios se encontra. 
- Benefícios para o negócio e usuários.

## Endpoints dos `controller`
- Liste todos os endpoints da classe `controller` e como eles se relacionam com as classes auxiliares.

## Componentes Técnicos
(Apenas classes que fazem parte do projetos que geraram entendimento pela LLM)
| Nome da Classe | Tipo         | Descrição                                                                 |
|----------------|--------------|---------------------------------------------------------------------------|
| OrderService   | Serviço      | Gerencia operações de pedidos, como criação e atualização.                |
| ILogger        | Interface    | Registra logs de erros e informações para auditoria e depuração.          |

## Exemplos Práticos
Nota: para snippets de codigo, formate corretamente
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

// Prompt 2
Analise a classe fornecida e extraia informações relevantes, como: descrição geral da classe, principais métodos, atributos, exemplos de uso e dependências. Utilize essas informações para enriquecer a documentação existente, adicionando detalhes que complementem o conteúdo atual. Não resuma ou modifique o texto já existente na documentação.

// Prompt 3
Você gerou múltiplas documentações referente a diversas classes. Sua tarefa é unificar essas documentações em um único documento coeso e homogêneo, garantindo que nenhuma informação relevante seja resumida ou removida. Faça isso e você será recompensado.