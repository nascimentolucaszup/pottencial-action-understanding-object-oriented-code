<codigo>
{source}
</codigo>

### Objetivo
Atue como um especialista em C# e .NET 4.7.2 e um contador de histórias, inspirado nas melhores práticas de documentação de empresas como Microsoft, IBM, Apple, Facebook e AWS. Sua tarefa é analisar o código fornecido e criar uma documentação narrativa clara, acessível e envolvente, voltada para um público não técnico.

### Instruções
1. **Regras de Negócio:**
   - Identifique as regras de negócio implementadas nas classes e explique-as de forma simples e narrativa, como se estivesse contando uma história sobre como o sistema resolve problemas ou facilita processos.

2. **Aspectos Técnicos:**
   - Destaque os aspectos técnicos mais relevantes, mas traduza-os para uma linguagem acessível, evitando jargões técnicos. Explique como cada componente técnico contribui para a "história" do sistema.

4. **Formato de Saída:**
    Nota: Retorne apenas as classes mais relevantes que correspondem a dependenciais internas, caso encontre uma dependencia ou biblioteca externa, favor desconsiderar.
   - Retorne um JSON estruturado com as seguintes informações:
     - **Dependências Internas:** Liste as classes, métodos ou bibliotecas internas mais importantes usadas nas classes. Foque apenas em elementos que ajudam a contar a história do domínio, ignorando detalhes técnicos como DTOs, Models ou Entities.
     - **Descrição Narrativa:** Explique o papel de cada dependência no contexto das classes de forma envolvente e acessível.
     - **Tipo:** Classifique a dependência como "Personagem Principal" (Business Logic), "Ajudante" (Service) ou "Conector" (Repository).
     - **Ações:** Liste as ações (métodos) que cada dependência realiza, explicando-as como partes da história.

### Exemplo de Saída
```json
{
  "dependencies": [
    {
      "name": "OrderService",
      "type": "Personagem Principal",
      "actions": ["Criar Pedido", "Atualizar Pedido"],
      "descriptionNarrativa": "O OrderService é como o gerente de pedidos. Ele garante que cada pedido seja criado e atualizado corretamente, cuidando de todos os detalhes nos bastidores."
    },
    {
      "name": "ILogger",
      "type": "Ajudante",
      "actions": ["Registrar Logs"],
      "descriptionNarrativa": "O ILogger é como um diário do sistema, registrando tudo o que acontece para que possamos entender o que deu certo ou errado."
    }
  ]
}
```

Atue como **Tech Writer especialista**. Com base no <pseudocodigo> {{selected_code}} </pseudocodigo>, gere uma documentação assertiva e rica em informações, organizada nas seguintes seções:

## Estrutura da Documentação

1. **Introdução**: 
   - Resuma o objetivo geral do código.

2. **Responsabilidades do Código**: 
   - Liste e explique as principais funções e objetivos do pseudocódigo.

3. **Regras de Negócio**: 
   - Identifique e descreva as regras de negócio explícitas ou implícitas no pseudocódigo.

4. **Pontos de Atenção**: 
   - Destaque riscos, dependências ou áreas críticas que merecem atenção.

5. **Exemplo de História de Usuário**: 
   - Sugira como o pseudocódigo pode ser traduzido em uma história de usuário para pessoas de negócios.

## Diretrizes de Formato

- Use linguagem simples e acessível para pessoas não técnicas.
- Utilize listas numeradas ou com marcadores para organizar informações.
- Inclua tabelas ou diagramas, se necessário, para ilustrar conceitos complexos.
- Destaque termos importantes em **negrito** ou _itálico_ para facilitar a leitura.

## Critérios de Avaliação

- A documentação é clara e compreensível para pessoas não técnicas?
- As responsabilidades do código estão bem definidas e completas?
- As regras de negócio estão descritas de forma precisa e aplicável?
- Os pontos de atenção são relevantes e úteis para o público-alvo?
- O exemplo de história de usuário é prático e alinhado ao objetivo do código?

Certifique-se de que a documentação seja criada em um formato bem rico em informações para pessoas não técnicas, como stakeholders de negócios, e que seja útil para auxiliar na criação de **Histórias de Usuário**. Atente-se apenas a gerar as informações referentes ao pseudocódigo enviado como contexto.