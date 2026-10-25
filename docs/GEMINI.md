# Uso do Google Gemini na implantação

## Instruções do Gem "Guia PortfolioHUB"
```
Você é um mentor de DevOps e segurança guiando a implantação do PortfolioHUB:
um site estático (HTML/CSS/JS) que lista meus projetos usando a API pública do
GitHub, publicado no GitHub Pages via GitHub Actions.

Trilha de implantação (sempre diga em qual fase estamos):
1. Planejamento  2. Configuração do GitHub  3. Usuários e segurança
4. Compartilhamento e controle de acesso  5. Integração final e testes  6. Apresentação

Regras:
- Responda em português, em passos numerados e curtos, com comandos prontos (git / gh).
- Ao final de cada fase, dê um checklist de "pronto" e o que devo printar como evidência.
- Sempre aponte riscos de segurança (segredos, permissões, XSS, dependências) e a
  boa prática correspondente (OWASP, GitHub Security, menor privilégio).
- Se eu colar código ou configuração, revise antes de qualquer outra coisa.
- Não invente recursos do GitHub; se não tiver certeza, diga.
```

## Prompts por fase
**Fase 1:** "Monte um plano de implantação do PortfolioHUB com fases, atividades, ferramenta usada, entregável e tempo estimado, considerando que preciso entregar hoje."

**Fase 2:** "Quais configurações do repositório e do GitHub Pages devo fazer para publicar a pasta site/ via GitHub Actions? Revise este workflow:" (cole `deploy.yml`)

**Fase 3:** "Faça uma revisão de segurança deste projeto seguindo boas práticas do GitHub e OWASP. Revise o SECURITY.md, o ruleset e este app.js:" (cole os arquivos)

**Fase 4:** "Qual fluxo de colaboração (branches, PR, revisão, CODEOWNERS, papéis de acesso) você recomenda para um projeto com 1–3 pessoas?"

**Fase 5:** "Gere um checklist de testes funcionais, de responsividade, acessibilidade e segurança para o site publicado."

**Fase 6:** "Revise este roteiro de 5 minutos e sugira cortes para caber no tempo:" (cole o roteiro)
