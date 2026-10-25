# Implantação passo a passo

Pré-requisitos: Git, [GitHub CLI](https://cli.github.com) (`gh auth login`), conta Google com Gemini.
Troque `SEU_USUARIO_GITHUB` pelo seu login em: `site/config.js`, `.github/CODEOWNERS`, `README.md`.

> 📸 = tirar print para o PDF.

## Fase 1 — Planejamento + Gemini
1. Em gemini.google.com → **Gems → Novo Gem**, nome "Guia PortfolioHUB", cole as instruções de `docs/GEMINI.md`. 📸
2. Pergunte ao Gem o prompt da Fase 1 (está em `docs/GEMINI.md`) e salve a resposta. 📸

## Fase 2 — Ambiente GitHub
```bash
cd portfoliohub
git init -b main
git add . && git commit -m "feat: estrutura inicial do PortfolioHUB"
gh repo create portfoliohub --public --source=. --push \
  --description "Plataforma centralizada dos meus projetos"
gh repo edit --add-topic portfolio --add-topic github-pages \
  --homepage "https://SEU_USUARIO_GITHUB.github.io/portfoliohub/" \
  --enable-wiki=false --delete-branch-on-merge
```
3. **Settings → Pages → Source: GitHub Actions.** Rode o workflow (Actions → Deploy → Run workflow) se não rodou. 📸 (site no ar)
4. Nos repos que você quer destacar: `gh repo edit SEU_USUARIO_GITHUB/<repo> --add-topic portfolio` e preencha o *Website* se tiver demo.
5. **Projects → New project (Board)** "Implantação PortfolioHUB"; crie 1 issue por fase com o template *Tarefa* e jogue no board. 📸

## Fase 3 — Usuários e segurança
6. Conta: **Settings → Password and authentication → 2FA** ativado. 📸
7. Repo → **Settings → Code security**: ativar *Dependabot alerts*, *Dependabot security updates*, *Secret scanning* + *Push protection*, *Private vulnerability reporting*. 📸
8. Ruleset da main:
```bash
gh api -X POST repos/SEU_USUARIO_GITHUB/portfoliohub/rulesets --input .github/ruleset-main.json
```
   Depois, em **Settings → Rules → proteger-main**, adicione *Require status checks → analyze* (aparece após o 1º CodeQL). 📸
9. Colaborador (colega ou 2ª conta): **Settings → Collaborators → Add people** com papel *Write* (ou *Read* para só visualizar). 📸
   - Opcional (nota extra): crie uma Organization gratuita, times `mantenedores` (Maintain) e `revisores` (Triage), e transfira o repo.
10. Peça ao Gem a revisão de segurança (prompt da Fase 3) e aplique o que fizer sentido. 📸

## Fase 4 — Controle de versão e colaboração
11. Faça uma mudança via PR para provar o fluxo:
```bash
git switch -c docs/ajuste-readme
# edite algo no README
git commit -am "docs: ajusta descrição do README"
git push -u origin docs/ajuste-readme
gh pr create --fill
```
   Mostre: PR bloqueado até CodeQL passar → merge (squash) → branch apagada → deploy automático. 📸

## Fase 5 — Testes e produção
12. Checklist no site publicado (📸 de cada):
   - [ ] Perfil, avatar e lista carregam
   - [ ] Busca, filtro por linguagem (barra e select) e ordenação funcionam
   - [ ] Destaques aparecem (repos com tópico `portfolio`)
   - [ ] Mobile (DevTools → modo responsivo) e tema escuro
   - [ ] `?user=usuario-que-nao-existe` mostra mensagem de erro clara
   - [ ] DevTools → Console sem erros de CSP
   - [ ] Lighthouse (Acessibilidade e Boas práticas ≥ 90)
   - [ ] Aba Security sem alertas abertos
13. Crie a release: `gh release create v1.0.0 --generate-notes --title "PortfolioHUB v1.0"` 📸

## Fase 6 — Apresentação
14. Grave o vídeo de 5 min (roteiro no arquivo `docs/ROTEIRO-VIDEO.md`), suba no YouTube como **Não listado** e cole o link no PDF.

## Gerar o PDF da entrega
1. Salve os prints em `entrega/prints/` como `01.png`, `02.png`… (a lista com o que cada um mostra aparece ao rodar o script).
2. Preencha o dicionário `DADOS` no topo de `entrega/gerar_pdf.py`.
3. `pip install reportlab pillow && python3 entrega/gerar_pdf.py`
4. Confira se nada ficou em amarelo e envie `entrega/Entrega_Final_PortfolioHUB.pdf`.
