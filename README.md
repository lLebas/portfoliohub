# PortfolioHUB

Plataforma centralizada que exibe meus projetos direto do GitHub: perfil, linguagens, destaques e lista filtrável de repositórios. O GitHub é o armazenamento dos projetos; o site é publicado automaticamente no GitHub Pages.

**Site:** https://llebas.github.io/portfoliohub/

## Como funciona
- `site/` — HTML, CSS e JS puros, sem dependências. Lê a API pública do GitHub (`/users/:user` e `/users/:user/repos`).
- Repositórios com o tópico `portfolio` aparecem em **Em destaque**; o campo *Website* do repo vira o botão **Abrir demo**.
- `?user=outro-login` na URL mostra o portfólio de outro usuário (útil para testes).

## Estrutura
```
site/              aplicação (index.html, styles.css, app.js, config.js)
.github/workflows  deploy.yml (Pages) e codeql.yml (segurança)
.github/           dependabot, CODEOWNERS, templates de PR/issue, ruleset da main
docs/              setup passo a passo, colaboração e uso do Gemini
SECURITY.md        política de segurança
CONTRIBUTING.md    fluxo de colaboração
```

## Rodar localmente
```bash
cd site && python3 -m http.server 8080   # no Windows: python -m http.server 8080
```

Implantação completa: [docs/SETUP.md](docs/SETUP.md)
