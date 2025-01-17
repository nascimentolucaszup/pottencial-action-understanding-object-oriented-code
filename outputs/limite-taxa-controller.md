# Documentação do Controlador de Limite de Taxa

## 1. Introdução

O **Controlador de Limite de Taxa** é responsável por gerenciar e expor endpoints relacionados à manipulação de limites de taxa para empresas e tomadores. Ele fornece funcionalidades para consulta, geração de hiperlinks, decodificação de parâmetros e busca de informações específicas, como motivos de declínio e classificações de limite de taxa. Este controlador é parte de uma API que integra regras de negócio específicas para o domínio financeiro.

---

## 2. Responsabilidades do Código

### Principais Funcionalidades

1. **Consulta de Limites de Taxa**:
   - Permite buscar o último limite de taxa aprovado manualmente para um tomador específico.
   - Oferece métodos para obter limites de taxa com base em diferentes classificações, como:
     - Classificação geral.
     - Classificação por raiz de CNPJ.
     - Classificação por sócio.
     - Classificação por grupo.

2. **Busca de Motivos de Declínio**:
   - Retorna os motivos de declínio associados a um cliente ou situação específica.

3. **Geração e Decodificação de Hiperlinks**:
   - Gera hiperlinks para formalização de limites de taxa.
   - Decodifica parâmetros recebidos em hiperlinks para validação e processamento.

4. **Listagem de Limites de Taxa**:
   - Retorna uma lista de limites de taxa associados a uma empresa específica.

5. **Montagem de Respostas HTTP**:
   - Cria respostas HTTP personalizadas, incluindo redirecionamentos e mensagens de erro.

---

## 3. Regras de Negócio

### Regras Explícitas

- **Validação de Parâmetros**:
  - Parâmetros obrigatórios, como `cnpjTomador`, `classificacaoCodigo` e outros, devem ser fornecidos para que as operações sejam realizadas.
  - Hiperlinks devem conter exatamente 6 ou 7 parâmetros para serem considerados válidos.

- **Mensagens de Retorno**:
  - Em caso de sucesso, as respostas incluem os dados solicitados.
  - Em caso de erro, mensagens detalhadas são retornadas, indicando o problema ocorrido.

- **Geração de Hiperlinks**:
  - Hiperlinks são gerados com base em informações específicas, como IDs de formalização, CNPJ do tomador e códigos de cliente.

- **Decodificação de Hiperlinks**:
  - Parâmetros decodificados são validados antes de serem processados.
  - Caso os parâmetros sejam inválidos ou ausentes, mensagens de erro são retornadas.

### Regras Implícitas

- **Segurança**:
  - O cabeçalho `UserAgent` é verificado para garantir que as chamadas de hiperlinks sejam realizadas por navegadores.
  - Respostas HTTP incluem redirecionamentos seguros quando necessário.

- **Estrutura de Dados**:
  - As respostas seguem um padrão consistente, utilizando objetos como `RetornoListaDTO` e `RetornoObjetoDTO` para encapsular mensagens e dados.

---

## 4. Pontos de Atenção

### Riscos e Dependências

1. **Dependências Externas**:
   - O controlador depende de classes de negócio, como `LimiteTaxaBusiness`, para realizar operações. Alterações nessas classes podem impactar o funcionamento do controlador.
   - Utiliza bibliotecas externas, como `Serilog`, para registro de logs. Problemas na configuração de logs podem dificultar a rastreabilidade de erros.

2. **Validação de Parâmetros**:
   - A validação de parâmetros é crítica para evitar erros de processamento. Parâmetros ausentes ou inválidos podem gerar respostas inadequadas.

3. **Mensagens de Erro**:
   - Mensagens de erro detalhadas são úteis para depuração, mas podem expor informações sensíveis se não forem tratadas adequadamente.

4. **Redirecionamentos**:
   - URLs de redirecionamento devem ser verificadas para evitar vulnerabilidades, como ataques de redirecionamento malicioso.

### Áreas Críticas

- **Manutenção de Regras de Negócio**:
  - Alterações nas regras de negócio implementadas em `LimiteTaxaBusiness` podem exigir atualizações nos métodos do controlador.

- **Sobrecarga de Endpoints**:
  - Métodos como `BuscaMotivosDeclinio` possuem sobrecarga (mesmo nome com diferentes assinaturas). Isso pode causar confusão ou erros de roteamento.

- **Conflitos de Rotas**:
  - Rotas como `buscamotivosdeclinio` são definidas mais de uma vez, o que pode gerar conflitos ou comportamento inesperado.

---

## 5. Estrutura de Endpoints

| **Método** | **Rota**                                      | **Descrição**                                                                 |
|------------|-----------------------------------------------|-------------------------------------------------------------------------------|
| GET        | `{cnpjTomador}/ultimoAprovadoManual/{classificacaoCodigo}` | Retorna o último limite de taxa aprovado manualmente para um tomador.        |
| GET        | `obterUltimoPorClassificacao`                 | Retorna o último limite de taxa com base na classificação geral.             |
| GET        | `obterUltimoPorClassificacaoRaizCnpj`         | Retorna o último limite de taxa com base na raiz do CNPJ.                    |
| GET        | `obterUltimoPorClassificacaoSocio`            | Retorna o último limite de taxa com base no sócio.                           |
| GET        | `obterUltimoPorClassificacaoGrupo`            | Retorna o último limite de taxa com base no grupo.                           |
| GET        | `buscamotivosdeclinio`                        | Retorna os motivos de declínio com base em cliente ou situação específica.   |
| GET        | `buscalistalimitetaxas`                       | Retorna uma lista de limites de taxa associados a uma empresa.               |
| GET        | `gerahiperlink`                               | Gera um hiperlink para formalização de limite de taxa.                       |
| GET        | `decodificahiperlink`                         | Decodifica e valida parâmetros de um hiperlink.                              |
| GET        | `{parametro}`                                 | Processa ações com base em parâmetros fornecidos.                            |
| GET        | `obterUltimoPorEmpresa`                       | Retorna o último limite de taxa associado a uma empresa.                     |

---

## 6. Exemplos de Uso

### Exemplo 1: Consulta de Limite de Taxa
**Requisição**:
GET /api/limiteTaxa/12345678901234/ultimoAprovadoManual/10

**Resposta**:
{
  "id": 1,
  "cnpjTomador": "12345678901234",
  "classificacaoCodigo": 10,
  "limite": 50000.00,
  "status": "Aprovado"
}

### Exemplo 2: Geração de Hiperlink
**Requisição**:
GET /api/limiteTaxa/gerahiperlink?pkMovFilaFormalizacao=1&solicitacaoId=100&limiteTaxa=1&cnpjCpfTomador=12345678901&nChamado=123&codCliente=456&fkCodSalesForce=SF123

**Resposta**:
"https://sistema.com/hiperlink/12345678901/1/100"

---

## 7. Conclusão

O **Controlador de Limite de Taxa** é uma peça central para a gestão de limites de taxa no sistema, oferecendo funcionalidades robustas e flexíveis. No entanto, atenção especial deve ser dada à validação de parâmetros, tratamento de erros e manutenção de dependências externas para garantir a confiabilidade e segurança da aplicação.