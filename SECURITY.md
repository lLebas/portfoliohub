# Política de Segurança

## Versões suportadas
Apenas a versão publicada na branch `main` (GitHub Pages) recebe correções.

## Como reportar uma vulnerabilidade
Não abra issue pública. Use **Security → Report a vulnerability** (Private Vulnerability Reporting) neste repositório.
Resposta em até 72 h; correção priorizada conforme a gravidade.

## Controles aplicados
| Camada | Controle |
|---|---|
| Conta | 2FA obrigatório; tokens com escopo mínimo e validade curta |
| Repositório | Ruleset na `main`: sem push direto, sem force-push, sem deleção, PR obrigatório, conversas resolvidas |
| Código | CodeQL em todo PR e semanalmente; Dependabot para Actions; secret scanning + push protection |
| Acesso | Princípio do menor privilégio (Read/Triage/Write/Maintain/Admin); CODEOWNERS revisa `.github/` |
| Aplicação | Site estático, sem backend e sem segredos; Content-Security-Policy restritiva; dados da API inseridos via `textContent`; links só `https`, com `rel="noopener noreferrer"` |
| CI/CD | Workflows com `permissions` mínimas; deploy via OIDC (`id-token`) sem token salvo |
