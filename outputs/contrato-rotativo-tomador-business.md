# Documentação do Sistema de Contratos Rotativos

## 1. Introdução

O sistema de **Contratos Rotativos** é responsável por gerenciar operações relacionadas a contratos financeiros de tomadores, incluindo a verificação de pendências, obtenção de informações sobre contratos existentes e a criação de novos contratos. Ele utiliza uma base de dados para realizar consultas e atualizações, garantindo que as regras de negócio sejam aplicadas corretamente.

Este sistema é essencial para a gestão de contratos rotativos, especialmente em cenários que envolvem classificações específicas, como contratos de término de obras.

---

## 2. Responsabilidades do Código

O código implementa as seguintes funcionalidades principais:

### 2.1 Verificação de Pendências
- **`isCCGPendente`**: Verifica se há pendências de CCG (Contrato de Garantia) para uma empresa, considerando a modalidade de término de obras, se aplicável.
- **`possuiPendenciaConjuge`**: Verifica se há pendências relacionadas ao cônjuge de acionistas de uma empresa.

### 2.2 Obtenção de Informações
- **`obterCnpjMatriz`**: Retorna o CNPJ da matriz de uma empresa, caso o CNPJ fornecido seja de uma filial.
- **`ObterDataPrimeiroDocumentoEmitido`**: Obtém a data do primeiro documento emitido para uma empresa.

### 2.3 Gerenciamento de Contratos
- **`getContratoRotativoTomador`**: Recupera informações sobre o contrato rotativo mais recente de um tomador, considerando a modalidade de término de obras, se aplicável.
- **`GerarContratoRotativoTomador`**: Cria um novo contrato rotativo para um tomador, com base em informações fornecidas, como cliente, data de início e modalidade.

### 2.4 Atualizações
- **`atualizaDataInicioContratoRotativo`**: Atualiza a data de início de um contrato rotativo existente.

### 2.5 Utilitários Internos
- **`obterIdContratoTerminoObras`**: Obtém o identificador do contrato padrão para a modalidade de término de obras.
- **`obterIdContratoPadrao`**: Obtém o identificador do contrato padrão.
- **`ObterProximoNumeroContrato`**: Calcula o próximo número de contrato para o ano atual.

---

## 3. Regras de Negócio

### 3.1 Regras Explícitas
- **Pendências de CCG**:
  - Um contrato é considerado pendente se não houver data de retorno registrada.
  - Apenas contratos de término de obras com uma modalidade específica são considerados.
- **Pendências de Cônjuge**:
  - São verificadas apenas para acionistas que sejam pessoas físicas, com estado civil específico (casado, separado judicialmente ou divorciado).
  - O cônjuge deve estar registrado no sistema.
- **CNPJ da Matriz**:
  - Um CNPJ é considerado matriz se os dígitos correspondentes indicarem "0001".
- **Criação de Contratos**:
  - Contratos de término de obras utilizam uma modalidade específica.
  - A data final de contratos é fixada em 06/06/2079.

### 3.2 Regras Implícitas
- **Validação de Dados**:
  - O sistema assume que os dados fornecidos, como CNPJ e identificadores, são válidos e existentes no banco de dados.
- **Persistência de Dados**:
  - Todas as operações de criação e atualização são persistidas diretamente no banco de dados.

---

## 4. Pontos de Atenção

### 4.1 Riscos e Dependências
- **Dependência de Banco de Dados**:
  - O sistema depende de uma conexão ativa com o banco de dados para todas as operações.
  - Alterações na estrutura do banco de dados podem impactar diretamente o funcionamento do sistema.
- **Dependência de Regras de Negócio**:
  - Alterações nas regras de negócio, como critérios para pendências ou modalidades de contrato, exigem atualizações no código.
- **Validação de Dados**:
  - Não há validação explícita para os dados de entrada, como CNPJ ou identificadores. Dados inválidos podem causar falhas.

### 4.2 Áreas Críticas
- **Consultas SQL**:
  - As consultas SQL são construídas dinamicamente, o que pode expor o sistema a vulnerabilidades, como injeção de SQL, se os dados de entrada não forem tratados adequadamente.
- **Manutenção de Contratos**:
  - A lógica para determinar o próximo número de contrato e a modalidade de término de obras é sensível a alterações nos dados do banco.
- **Escalabilidade**:
  - O sistema pode enfrentar problemas de desempenho em cenários com grandes volumes de dados, devido ao uso de consultas complexas e sem otimização.

---

## 5. Tabela de Funções e Objetivos

| **Função**                          | **Descrição**                                                                 |
|-------------------------------------|-------------------------------------------------------------------------------|
| `isCCGPendente`                     | Verifica pendências de CCG para uma empresa.                                  |
| `possuiPendenciaConjuge`            | Verifica pendências relacionadas ao cônjuge de acionistas.                    |
| `obterCnpjMatriz`                   | Retorna o CNPJ da matriz de uma empresa.                                      |
| `ObterDataPrimeiroDocumentoEmitido` | Obtém a data do primeiro documento emitido para uma empresa.                  |
| `getContratoRotativoTomador`        | Recupera informações sobre o contrato rotativo mais recente de um tomador.    |
| `GerarContratoRotativoTomador`      | Cria um novo contrato rotativo para um tomador.                               |
| `atualizaDataInicioContratoRotativo`| Atualiza a data de início de um contrato rotativo existente.                  |
| `obterIdContratoTerminoObras`       | Obtém o identificador do contrato padrão para término de obras.               |
| `obterIdContratoPadrao`             | Obtém o identificador do contrato padrão.                                     |
| `ObterProximoNumeroContrato`        | Calcula o próximo número de contrato para o ano atual.                        |

---

## 6. Conclusão

O sistema de **Contratos Rotativos** é uma ferramenta robusta para a gestão de contratos financeiros, com funcionalidades que atendem a regras de negócio específicas. No entanto, é essencial garantir a integridade dos dados de entrada e monitorar possíveis alterações nas dependências externas, como o banco de dados e as regras de negócio.

Essa documentação pode ser utilizada como base para a criação de **Histórias de Usuário**, garantindo que os requisitos técnicos e de negócio sejam atendidos de forma clara e objetiva.