# POC IA Pottencial

## Modernização de Código Legado

### Contrato de Contragarantia

Um contrato de contragarantia é um instrumento jurídico utilizado no contexto de seguros. Ele estabelece uma relação entre três partes principais:

1. **Seguradora**: A empresa que assume os riscos e emite a apólice do seguro.
2. **Tomador (ou devedor)**: A parte que tem uma obrigação a cumprir e contrata a apólice de seguro.
3. **Segurado (ou credor)**: A parte que espera receber a obrigação e será beneficiada pelo seguro caso o tomador não cumpra suas obrigações.

No contrato de contragarantia, a seguradora obtém uma garantia adicional do tomador para se proteger contra possíveis perdas. Isso significa que, se o tomador não cumprir suas obrigações, a seguradora pode recorrer ao tomador para recuperar os valores pagos ao segurado.

Esse tipo de contrato é comum em situações onde há um risco significativo de inadimplência, proporcionando uma camada extra de segurança para a seguradora e garantindo que ela não sofra prejuízos ao conceder a garantia ao tomador.

### Application Solution Pottencial.GG 

#### Stack Técnica
- .Net Framework 4.7.2 - API REST
- Azure SQLServer

#### Principal Domínio: 
- `ContratoRotativoTomadorBusiness.cs`

#### Domínios Secundários: 
- `LimiteTaxaController.cs` -> `LimiteTaxaBusiness.cs` -> `GerarDocCCG`

A POC consiste em extrair ou realizar um recorte da parte de CCG desta aplicação (Pottencial.GG) a fim de seguir uma estratégia de modernização no ecossistema chamada estrangulamento.

#### Output
- Microservices
- Container: .Net Core 8 API REST 
- Partners: Clean Architecture | SOLID
- AZURE SQLServer
- FluentValidation
- Xunit