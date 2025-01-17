 
# Documentação Unificada do Domínio de Limite de Taxa, BPM e Garantias

## Índice
1. [Introdução](#introdução)
2. [Regras de Negócios](#regras-de-negócios)
3. [Visão Geral do Domínio](#visão-geral-do-domínio)
4. [Endpoints dos Controllers](#endpoints-dos-controllers)
5. [Componentes Técnicos](#componentes-técnicos)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Diagramas e Visualizações](#diagramas-e-visualizações)
8. [Futuro do Domínio](#futuro-do-domínio)

---

## Introdução
Este documento unifica a documentação das classes `LimiteTaxaController`, `LimiteTaxaBusiness`, `BpmBusiness`, `EmailBusiness`, `FormalizacaoLimiteTaxaBusiness`, `ContratoRotativoTomadorBusiness` e `SalesForceBusiness`. Essas classes compõem o domínio de Limite de Taxa, BPM e Garantias, sendo responsáveis por gerenciar operações como criação e manipulação de chamados, envio de e-mails, formalização de limites de taxa e integração com APIs externas e serviços SOAP.

Cada classe desempenha um papel específico no sistema, garantindo que as regras de negócio sejam aplicadas corretamente e que os dados sejam processados de forma consistente.

---

## Regras de Negócios

### Classe `LimiteTaxaController`
| Método | Descrição |
|--------|-----------|
| `UltimoAprovadoManual` | Retorna o último limite de taxa aprovado manualmente para um tomador específico. |
| `ObterUltimoPorClassificacao` | Obtém o último limite de taxa por classificação. |
| `BuscaMotivosDeclinio` | Retorna os motivos de declínio associados a um cliente ou situação específica. |
| `GerarHiperLink` | Gera um hiperlink para formalização de limite de taxa. |
| `DecodificaHiperLink` | Decodifica um hiperlink para validação de parâmetros. |

### Classe `LimiteTaxaBusiness`
| Método | Descrição |
|--------|-----------|
| `ProcessarFormalizacaoLimiteTaxa` | Processa a formalização de limites de taxa. |
| `EnviarEmailValidacao` | Envia e-mails de validação para os responsáveis. |
| `ObterUltimoPorClassificacao` | Retorna o último limite de taxa com base em classificações específicas. |
| `GeraHiperLink` | Gera um hiperlink para formalização ou validação de limites de taxa. |

### Classe `BpmBusiness`
| Método | Descrição |
|--------|-----------|
| `RetornaAnexoNovoMetodoDetalhe` | Retorna os detalhes dos anexos de um chamado. |
| `SalvaComentarioHistorico` | Salva um comentário no histórico de um chamado. |
| `ChamadoStatus` | Atualiza o status de um chamado. |
| `GeraChamadoLimiteTaxa` | Gera um chamado para limite de taxa. |
| `CriarChamadoSolicitacaoGarantia` | Cria um chamado para solicitação de garantia. |

### Classe `EmailBusiness`
| Método | Descrição |
|--------|-----------|
| `EnviarEmailFatura` | Gera relatórios de faturas e envia e-mails com os arquivos anexados. |
| `EnviarEmailHiperLink` | Envia e-mails contendo hiperlinks para ações específicas. |
| `ReprocessarEmails` | Atualiza o status de e-mails com falha para reprocessamento. |

---

## Visão Geral do Domínio
O domínio de Limite de Taxa, BPM e Garantias lida com a gestão de limites e taxas aplicáveis a empresas, sócios e grupos, além de gerenciar chamados e notificações. As regras de negócio implementadas garantem que os dados sejam processados de forma consistente e que as operações atendam aos requisitos do negócio.

### Benefícios para o Negócio
- **Automação de Processos**: Redução de erros manuais e aumento da eficiência operacional.
- **Integração com APIs Externas**: Suporte a SalesForce e serviços SOAP para maior flexibilidade.
- **Notificações Automatizadas**: Envio de e-mails e notificações para manter os stakeholders informados.

---

## Endpoints dos Controllers

### `LimiteTaxaController`
| Método HTTP | Endpoint | Descrição |
|-------------|----------|-----------|
| GET | `/api/limiteTaxa/{cnpjTomador}/ultimoAprovadoManual/{classificacaoCodigo}` | Obtém o último limite de taxa aprovado manualmente. |
| GET | `/api/limiteTaxa/obterUltimoPorClassificacao` | Obtém o último limite de taxa por classificação. |
| GET | `/api/limiteTaxa/buscamotivosdeclinio` | Busca motivos de declínio para um cliente ou situação específica. |
| GET | `/api/limiteTaxa/gerahiperlink` | Gera um hiperlink para formalização de limite de taxa. |

---

## Componentes Técnicos

| Nome da Classe | Tipo         | Descrição                                                                 |
|----------------|--------------|---------------------------------------------------------------------------|
| `LimiteTaxaBusiness` | Serviço      | Contém a lógica de negócio para manipulação de limites de taxa.          |
| `BpmBusiness`        | Serviço      | Gerencia a comunicação e integração com o sistema de BPM.                |
| `EmailBusiness`      | Serviço      | Gerencia o envio de e-mails no sistema.                                  |
| `FormalizacaoLimiteTaxaBusiness` | Serviço | Gerencia a formalização de limites de taxa.                              |
| `SalesForceBusiness` | Serviço      | Integra o sistema com a API do SalesForce.                               |

---

## Exemplos Práticos

### Cenário 1: Criar um Chamado para Limite de Taxa
csharp
var bpmBusiness = new BpmBusiness();
var resultado = await bpmBusiness.GeraChamadoLimiteTaxa(
    codigoCorretora: 123,
    cpfCnpjCliente: "12345678901234",
    cpfCnpjCorretora: "98765432100012",
    idCliente: 456,
    nomeSolicitante: "João Silva",
    emailSolicitante: "joao.silva@exemplo.com",
    numSolicitacao: 789
);
if (resultado.TipoMensagem == GSIFuncoes.EnumTipoMensagem.Sucesso) {
    Console.WriteLine($"Chamado criado com sucesso! Código: {resultado.CodSalesForce}");
} else {
    Console.WriteLine($"Erro ao criar chamado: {resultado.Mensagem}");
}


### Cenário 2: Enviar E-mail com Fatura
csharp
var emailBusiness = new EmailBusiness();
var emailFaturaDto = new EmailFaturaDto {
    idFatura = 123,
    estipulante = "Empresa XYZ",
    emails = new List<EmailDTO> {
        new EmailDTO {
            remetente = "sistema@empresa.com",
            destinatario = "cliente@empresa.com",
            assunto = "Fatura Mensal",
            mensagem = "Segue em anexo a fatura mensal."
        }
    },
    boleto = "https://linkparaboleto.com/boleto.pdf",
    nomeBoleto = "Boleto123.pdf"
};
var resultado = emailBusiness.EnviarEmailFatura(emailFaturaDto);
if (resultado.TipoMensagem == EnumTipoMensagem.Sucesso) {
    Console.WriteLine("E-mail enviado com sucesso!");
} else {
    Console.WriteLine($"Erro: {resultado.Mensagem}");
}


---

## Diagramas e Visualizações

### Fluxo de Dados entre o `LimiteTaxaController` e o `LimiteTaxaBusiness`
mermaid
graph TD
A[Cliente] -->|Requisição HTTP| B[LimiteTaxaController]
B -->|Chamada de Método| C[LimiteTaxaBusiness]
C -->|Processamento| D[Base de Dados]
D -->|Resposta| C
C -->|Retorno| B
B -->|Resposta HTTP| A


---

## Futuro do Domínio

1. **Melhorias na Validação de Dados**:
   - Implementar validações mais robustas para os parâmetros recebidos nos métodos públicos.
2. **Documentação Automatizada**:
   - Integrar ferramentas como Swagger para gerar documentação interativa da API.
3. **Adoção de Padrões Modernos**:
   - Migrar para o uso de `ASP.NET Core` para maior desempenho e suporte a novas funcionalidades.
4. **Monitoramento e Logging**:
   - Adicionar monitoramento detalhado e logs estruturados para facilitar a depuração e auditoria.
5. **Segurança**:
   - Implementar autenticação e autorização baseadas em OAuth 2.0 para proteger os endpoints e operações críticas.

 