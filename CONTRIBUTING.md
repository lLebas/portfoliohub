# Como contribuir

1. Abra (ou pegue) uma **issue** usando o template "Tarefa".
2. Crie uma branch a partir da `main`: `feat/<assunto>`, `fix/<assunto>` ou `docs/<assunto>`.
3. Commits no padrão Conventional Commits: `feat: filtro por linguagem`, `fix: link de demo`, `docs: guia de setup`.
4. Abra um **Pull Request** com o template, vinculando a issue (`Closes #N`).
5. Aguarde o CodeQL passar e a revisão (CODEOWNERS). Merge via **Squash and merge**.
6. O deploy no GitHub Pages acontece sozinho após o merge.

Rodar localmente: `cd site && python3 -m http.server 8080` e abra http://localhost:8080
