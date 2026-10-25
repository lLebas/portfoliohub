# Roteiro — vídeo de 5 min (YouTube, não listado)

Grave a tela (OBS ou Loom) com o site, o GitHub e o Gemini já abertos em abas.

| Tempo | Tela | Fala (resumo) |
|---|---|---|
| 0:00–0:30 | Site publicado | "Oi, sou [SEU NOME]. Este é o PortfolioHUB: uma plataforma que reúne meus projetos lendo direto do GitHub e é publicada automaticamente no GitHub Pages." |
| 0:30–1:10 | Gemini (Gem "Guia PortfolioHUB") | "Comecei criando um Gem no Gemini com a trilha das 6 fases. Ele gerou o plano de implantação e me guiou em cada etapa, sempre com checklist e alerta de segurança." Mostrar 1 resposta. |
| 1:10–2:00 | Site: barra de linguagens, filtro, busca, destaques | "A integração com o GitHub funciona assim: o site consulta a API pública, mostra o perfil, as linguagens e os repos. Quem tem o tópico 'portfolio' vira destaque, e o campo Website vira o botão de demo." |
| 2:00–3:10 | GitHub: Settings → Rules, Code security, Collaborators | "Na segurança: 2FA na conta, ruleset na main sem push direto e sem force-push, PR obrigatório, CodeQL em todo PR, Dependabot, secret scanning com push protection e colaboradores com o menor privilégio. No site: CSP restritiva e nenhum dado da API entra como HTML, o que evita XSS." |
| 3:10–4:00 | PR aberto → checks → merge → Actions deploy | "A colaboração segue issue → branch → PR com template → CodeQL passa → revisão → squash merge. O deploy roda sozinho após o merge." |
| 4:00–4:40 | Tela de testes / Lighthouse / release v1.0.0 | "Testei funcionalidade, mobile, tema escuro, erro de usuário inexistente e Lighthouse, e publiquei a release v1.0.0." |
| 4:40–5:00 | Site | "O maior desafio foi [DESAFIO REAL, ex.: limite de 60 requisições/h da API — resolvi com cache de 10 min]. Obrigado!" |
