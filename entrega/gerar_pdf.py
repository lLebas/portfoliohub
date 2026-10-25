# Uso: preencha DADOS, salve os prints em entrega/prints/ com os nomes da lista PRINTS e rode:
#   pip install reportlab pillow && python3 entrega/gerar_pdf.py
import os
BASE=os.path.dirname(os.path.abspath(__file__))
DADOS={
  "nome": "",          # Seu nome completo
  "ra": "",            # Seu RA
  "usuario": "",       # login do GitHub
  "video": "",         # link do YouTube
  "colaborador": "",   # usuário do colaborador
  "lighthouse": "",    # ex.: "A11y 98 / BP 100"
  "desafio": "", "solucao": "",
  "reflexao": "",
  "gemini": [          # (recomendação do Gemini, ação tomada)
    ("", ""), ("", ""), ("", "")
  ],
}
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Image as RLImage
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W=os.path.join(os.environ.get('WINDIR','C:\\Windows'),'Fonts')
if os.path.exists(os.path.join(W,'segoeui.ttf')):  # Windows: Segoe UI + Consolas
    FONTES={'S':'segoeui.ttf','SB':'segoeuib.ttf','M':'consola.ttf'}; F=W
else:                                               # Linux: DejaVu
    FONTES={'S':'DejaVuSans.ttf','SB':'DejaVuSans-Bold.ttf','M':'DejaVuSansMono.ttf'}; F='/usr/share/fonts/truetype/dejavu'
for k,v in FONTES.items(): pdfmetrics.registerFont(TTFont(k,os.path.join(F,v)))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('S',normal='S',bold='SB',italic='S',boldItalic='SB')

TINTA=colors.HexColor('#1B2A41'); MAG=colors.HexColor('#9B1F7A'); SUAVE=colors.HexColor('#56657A')
LINHA=colors.HexColor('#D3DAE2'); AMAR=colors.HexColor('#FFF3C4'); AMARB=colors.HexColor('#E0B53A'); CINZA=colors.HexColor('#F2F4F7')

st=lambda **k: ParagraphStyle('x',**{'fontName':'S','fontSize':10.5,'leading':15,'textColor':TINTA,**k})
H1=st(fontName='SB',fontSize=17,leading=22,textColor=MAG,spaceBefore=6,spaceAfter=8)
H2=st(fontName='SB',fontSize=12.5,leading=17,spaceBefore=10,spaceAfter=4)
P=st(spaceAfter=6,alignment=4)
B=st(leftIndent=12,bulletIndent=2,spaceAfter=3,bulletFontName='S')
CEL=st(fontSize=9,leading=12); CELB=st(fontName='SB',fontSize=9,leading=12,textColor=colors.white)
MONO=ParagraphStyle('m',fontName='M',fontSize=8,leading=11,textColor=TINTA)
PH=st(fontSize=9.5,leading=13,textColor=colors.HexColor('#6B4E00'))

story=[]
def h1(t): story.append(Paragraph(t,H1))
def h2(t): story.append(Paragraph(t,H2))
def p(t): story.append(Paragraph(t,P))
def bl(items): [story.append(Paragraph(i,B,bulletText='•')) for i in items]
def code(t):
    tb=Table([[Preformatted(t,MONO)]],colWidths=[16.4*cm])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CINZA),('BOX',(0,0),(-1,-1),.5,LINHA),('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(tb); story.append(Spacer(1,6))
PRINTS=[]
def ph(t, alto=3.2):
    nome=f"{len(PRINTS)+1:02d}.png"; PRINTS.append((nome,t))
    cam=os.path.join(BASE,'prints',nome)
    if os.path.exists(cam):
        w,h=PILImage.open(cam).size; W=16.4*cm; H=W*h/w
        if H>11*cm: H=11*cm; W=H*w/h
        story.append(KeepTogether([RLImage(cam,width=W,height=H),Paragraph(t,st(fontSize=8.5,textColor=SUAVE,alignment=1)),Spacer(1,8)])); return
    t=f'<b>{nome}</b> – '+t
    tb=Table([[Paragraph('<b>[INSERIR PRINT]</b> '+t,PH)]],colWidths=[16.4*cm],rowHeights=[alto*cm])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),AMAR),('BOX',(0,0),(-1,-1),1,AMARB),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10)]))
    story.append(KeepTogether([tb,Spacer(1,8)]))
def fill(t, valor=''): return valor if valor else f'<font backColor="#FFF3C4">[{t}]</font>'
U=DADOS['usuario'] or 'SEU_USUARIO'
def tabela(cab, linhas, larg):
    d=[[Paragraph(c,CELB) for c in cab]]+[[Paragraph(c,CEL) for c in l] for l in linhas]
    tb=Table(d,colWidths=[w*cm for w in larg],repeatRows=1)
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TINTA),('GRID',(0,0),(-1,-1),.4,LINHA),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,CINZA]),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(tb); story.append(Spacer(1,8))

# ---------- CAPA ----------
story.append(Spacer(1,4.5*cm))
story.append(Paragraph('Desafio – Entrega Final',st(fontName='SB',fontSize=13,textColor=SUAVE)))
story.append(Paragraph('Implantação do PortfolioHUB<br/>com apoio do Google Gemini',st(fontName='SB',fontSize=28,leading=36,textColor=MAG,spaceBefore=6,spaceAfter=24)))
capa=[['Curso','Bootcamp I – Turma B – 0726 – Campus Virtual – 2026/2'],
      ['Aluno(a)',fill('SEU NOME COMPLETO',DADOS['nome'])+' – RA '+fill('SEU RA',DADOS['ra'])],
      ['Repositório',fill('https://github.com/SEU_USUARIO/portfoliohub',DADOS['usuario'] and f'https://github.com/{U}/portfoliohub')],
      ['Site em produção',fill('https://SEU_USUARIO.github.io/portfoliohub/',DADOS['usuario'] and f'https://{U}.github.io/portfoliohub/')],
      ['Vídeo (YouTube)',fill('LINK DO VÍDEO',DADOS['video'])],
      ['Data','25/10/2026']]
tb=Table([[Paragraph('<b>'+a+'</b>',CEL),Paragraph(b,CEL)] for a,b in capa],colWidths=[4*cm,12.4*cm])
tb.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.4,LINHA),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(tb)
story.append(Spacer(1,1.5*cm))
story.append(Paragraph('Os trechos destacados em amarelo devem ser substituídos pelos dados e prints reais da implantação.',st(fontSize=8.5,textColor=SUAVE)))
story.append(PageBreak())

# ---------- SUMÁRIO ----------
h1('Sumário')
for s in ['1. Planejamento da Implantação','2. Configuração Inicial e Integração com GitHub','3. Gestão de Usuários e Segurança',
          '4. Compartilhamento e Controle de Acesso com GitHub','5. Finalização da Integração e Testes','6. Revisão Final e Apresentação','Conclusão']:
    story.append(Paragraph(s,st(fontSize=11.5,leading=22)))
story.append(Spacer(1,10))
h2('Visão geral')
p('O PortfolioHUB é uma plataforma web centralizada para exibir e gerenciar meus projetos e portfólios digitais. '
  'Ele é um site estático (HTML, CSS e JavaScript puros) que consulta em tempo real a API pública do GitHub: o GitHub funciona como '
  'o armazenamento dos projetos e o site como a vitrine. A publicação é feita no GitHub Pages por um pipeline do GitHub Actions, '
  'e todo o processo foi guiado por um Gem personalizado do Google Gemini.')
code('Navegador do visitante ──> PortfolioHUB (GitHub Pages)\n'
     '                               │  fetch HTTPS\n'
     '                               ▼\n'
     '                       API pública do GitHub  (/users/:user e /users/:user/repos)\n\n'
     'Desenvolvedor ──> branch ──> Pull Request ──> CodeQL + revisão ──> merge na main\n'
     '                                                                     │\n'
     '                                              GitHub Actions (deploy.yml) ──> GitHub Pages')
story.append(PageBreak())

# ---------- 1 ----------
h1('1. Planejamento da Implantação')
h2('1.1 Escopo e objetivos')
bl(['Publicar uma vitrine única dos meus projetos, alimentada automaticamente pelos repositórios do GitHub.',
    'Garantir segurança na conta, no repositório, no pipeline e na aplicação.',
    'Estabelecer um fluxo de colaboração com controle de versão, revisão e controle de acesso.',
    'Usar o Google Gemini como guia em todas as fases e registrar as evidências.'])
h2('1.2 Plano de implantação')
tabela(['Fase','Atividades','Ferramentas','Entregável'],[
 ['1. Planejamento','Definir escopo, arquitetura e riscos; criar o Gem "Guia PortfolioHUB"; gerar o plano com o Gemini','Gemini (Gems)','Plano e Gem configurado'],
 ['2. GitHub','Criar repositório, estrutura do projeto, GitHub Pages via Actions, tópicos, Projects (board) e issues por fase','Git, GitHub CLI, Actions, Pages, Projects','Repositório e site no ar'],
 ['3. Segurança','2FA, ruleset da main, CodeQL, Dependabot, secret scanning, push protection, SECURITY.md, colaboradores com menor privilégio','GitHub Security, Gemini','Políticas aplicadas e revisadas'],
 ['4. Acesso','CODEOWNERS, templates de PR/issue, CONTRIBUTING.md, fluxo branch → PR → revisão → merge','GitHub','Fluxo documentado e testado'],
 ['5. Testes','Checklist funcional, responsivo, acessibilidade, segurança (CSP/XSS) e Lighthouse; release v1.0.0','DevTools, Lighthouse','Release em produção'],
 ['6. Apresentação','Roteiro, gravação de 5 min e publicação no YouTube','OBS/Loom, YouTube','Vídeo e este documento'],
],[2.6,6.6,3.8,3.4])
h2('1.3 Riscos e mitigação')
tabela(['Risco','Mitigação'],[
 ['Vazamento de token ou senha no repositório','Site sem segredos; secret scanning com push protection; .gitignore para .env'],
 ['Alteração indevida na branch principal','Ruleset: PR obrigatório, sem push direto, sem force-push e sem deleção'],
 ['Injeção de conteúdo (XSS) vindo da API','Dados inseridos com textContent; links aceitos só em https; Content-Security-Policy'],
 ['Limite de 60 requisições/hora da API sem token','Cache de 10 minutos no sessionStorage e mensagem de erro clara'],
 ['Dependência de Actions desatualizada','Dependabot semanal para github-actions'],
],[6,10.4])
h2('1.4 Configuração do Google Gemini como guia da trilha')
p('Criei um Gem (assistente personalizado) no Gemini chamado <b>Guia PortfolioHUB</b>, com instruções que definem a trilha das seis fases, '
  'o formato das respostas (passos numerados, comandos prontos, checklist de conclusão e evidências) e a obrigação de apontar riscos de segurança. '
  'Para cada fase usei um prompt específico (documentados em docs/GEMINI.md no repositório).')
code('Você é um mentor de DevOps e segurança guiando a implantação do PortfolioHUB:\n'
     'um site estático que lista meus projetos usando a API pública do GitHub,\n'
     'publicado no GitHub Pages via GitHub Actions.\n'
     'Trilha: 1 Planejamento · 2 GitHub · 3 Usuários e segurança · 4 Acesso\n'
     '        5 Integração e testes · 6 Apresentação\n'
     'Regras: responda em português, em passos curtos com comandos git/gh;\n'
     'ao fim de cada fase dê um checklist e as evidências a registrar;\n'
     'aponte riscos de segurança e a boa prática (OWASP, GitHub, menor privilégio);\n'
     'revise qualquer código colado; não invente recursos do GitHub.')
ph('Tela de criação do Gem "Guia PortfolioHUB" com as instruções.')
ph('Resposta do Gemini com o plano de implantação da Fase 1.')
story.append(PageBreak())

# ---------- 2 ----------
h1('2. Configuração Inicial e Integração com GitHub')
h2('2.1 Ambiente GitHub dedicado')
p('Criei o repositório público <b>portfoliohub</b> com descrição, tópicos (portfolio, github-pages), site configurado, wiki desativada e '
  'exclusão automática de branches após o merge. A estrutura do projeto:')
code('site/               aplicação: index.html, styles.css, app.js, config.js\n'
     '.github/workflows/  deploy.yml (Pages) e codeql.yml (segurança)\n'
     '.github/            dependabot.yml, CODEOWNERS, templates de PR e issue, ruleset-main.json\n'
     'docs/               SETUP.md (passo a passo) e GEMINI.md (Gem e prompts)\n'
     'SECURITY.md  CONTRIBUTING.md  README.md  LICENSE  .gitignore')
code('git init -b main && git add . && git commit -m "feat: estrutura inicial do PortfolioHUB"\n'
     'gh repo create portfoliohub --public --source=. --push \\\n'
     '   --description "Plataforma centralizada dos meus projetos"\n'
     'gh repo edit --add-topic portfolio --add-topic github-pages \\\n'
     '   --homepage "https://'+U+'.github.io/portfoliohub/" --delete-branch-on-merge')
h2('2.2 Publicação contínua (GitHub Pages + Actions)')
p('Em Settings → Pages selecionei a origem <b>GitHub Actions</b>. O workflow deploy.yml publica a pasta site/ a cada merge na main, '
  'com permissões mínimas (contents: read, pages: write, id-token: write) e autenticação por OIDC, sem nenhum token armazenado.')
h2('2.3 Integração das funcionalidades do GitHub no PortfolioHUB')
tabela(['Funcionalidade do GitHub','Como o PortfolioHUB usa'],[
 ['Repositórios (armazenamento dos projetos)','Lista todos os repositórios públicos via /users/:user/repos, com busca, filtro e ordenação'],
 ['Perfil do usuário','Nome, foto, bio e link do perfil via /users/:user'],
 ['Linguagem do repositório','Barra de proporção de linguagens clicável que filtra a lista'],
 ['Tópicos (topics)','Repositórios com o tópico portfolio aparecem em "Em destaque"'],
 ['Campo Website (homepage)','Vira o botão "Abrir demo" (somente URLs https)'],
 ['Estrelas e último push','Exibidos em cada projeto e usados na ordenação'],
 ['GitHub Pages e Actions','Hospedagem e deploy automático do próprio PortfolioHUB'],
],[5.5,10.9])
p('Assim, publicar um novo projeto no portfólio é só criar o repositório e adicionar o tópico portfolio: nenhuma alteração no código do site é necessária.')
ph('Repositório criado (página inicial com arquivos e tópicos).',2.8)
ph('Actions: workflow "Deploy no GitHub Pages" concluído com sucesso.',2.8)
ph('PortfolioHUB publicado mostrando meus projetos.',4)
story.append(PageBreak())

# ---------- 3 ----------
h1('3. Gestão de Usuários e Segurança')
h2('3.1 Gestão de usuários')
p('A gestão de usuários segue o princípio do menor privilégio: cada pessoa recebe apenas o papel necessário para sua função.')
tabela(['Papel no GitHub','Permissões','Quem recebe'],[
 ['Admin','Configurações, segurança, regras e exclusão','Somente o dono do projeto'],
 ['Maintain','Gerenciar issues, PRs e releases, sem configurações sensíveis','Mantenedor de confiança (se houver)'],
 ['Write','Criar branches e abrir PRs (merge só via ruleset)',fill('NOME/USUÁRIO DO COLABORADOR',DADOS['colaborador'])],
 ['Triage','Organizar issues e PRs, sem escrever código','Revisores/colegas'],
 ['Read','Ver e clonar o código','Professor/avaliador, se o repositório for privado'],
],[3,8,5.4])
bl(['Autenticação de dois fatores (2FA) ativada na conta.',
    'Colaborador adicionado em Settings → Collaborators com o papel Write.',
    'O arquivo CODEOWNERS define o responsável pela revisão de todo o código e, em especial, da pasta .github/ (workflows e regras).',
    'O PortfolioHUB exibe apenas repositórios públicos e não-fork; repositórios privados nunca são listados.'])
ph('2FA ativado na conta (Settings → Password and authentication).',2.6)
ph('Colaborador adicionado com o papel Write.',2.6)
h2('3.2 Políticas de segurança')
tabela(['Camada','Política implementada'],[
 ['Conta','2FA obrigatório; tokens pessoais apenas com escopo mínimo e validade curta'],
 ['Repositório','Ruleset "proteger-main": sem push direto, sem force-push, sem exclusão da main, PR obrigatório, conversas resolvidas e check do CodeQL obrigatório'],
 ['Código','CodeQL em todo PR, em todo push na main e semanalmente; Dependabot alerts e security updates'],
 ['Segredos','Secret scanning e push protection ativos; nenhum segredo no projeto (site 100% estático); .gitignore para .env'],
 ['Pipeline','Permissões mínimas declaradas em cada workflow; deploy via OIDC'],
 ['Aplicação','Content-Security-Policy restritiva (scripts só do próprio domínio, conexão só com api.github.com); conteúdo da API inserido com textContent; links só https com rel="noopener noreferrer"; parâmetro ?user validado'],
 ['Divulgação','SECURITY.md e Private Vulnerability Reporting para relatos de falhas sem exposição pública'],
],[3,13.4])
code('gh api -X POST repos/'+U+'/portfoliohub/rulesets --input .github/ruleset-main.json')
h2('3.3 Conformidade com boas práticas usando o Gemini')
p('Enviei ao Gem o SECURITY.md, o ruleset e o app.js pedindo uma revisão com base nas boas práticas do GitHub e do OWASP. '
  'Principais recomendações e o que foi aplicado:')
tabela(['Recomendação do Gemini','Ação tomada'],[
 *[[fill(ex[0],g[0]),fill(ex[1],g[1])] for g,ex in zip(DADOS['gemini'],[
   ('Ex.: evitar innerHTML com dados externos','Ex.: renderização com textContent'),
   ('Ex.: bloquear push direto na main','Ex.: ruleset proteger-main'),
   ('Ex.: restringir origens com CSP','Ex.: meta CSP no index.html')])],
],[8.2,8.2])
ph('Revisão de segurança feita pelo Gemini.')
ph('Settings → Code security com Dependabot, secret scanning e push protection ativos.',2.8)
ph('Settings → Rules: ruleset "proteger-main" ativo.',2.8)
story.append(PageBreak())

# ---------- 4 ----------
h1('4. Compartilhamento e Controle de Acesso com GitHub')
h2('4.1 Repositório integrado ao PortfolioHUB')
p('O repositório do PortfolioHUB aparece no próprio site (é público e tem o tópico portfolio), com link para o código e para a demo. '
  'Qualquer pessoa pode ver e clonar o código; somente colaboradores autorizados contribuem, e sempre por Pull Request.')
h2('4.2 Controle de versão e fluxo de colaboração')
code('issue (template "Tarefa")  →  branch feat/ fix/ docs/  →  commits (Conventional Commits)\n'
     '   →  Pull Request (template + "Closes #N")  →  CodeQL + revisão (CODEOWNERS)\n'
     '   →  Squash and merge  →  branch apagada  →  deploy automático no Pages')
bl(['<b>Issues e Projects:</b> uma issue por fase, organizadas no board "Implantação PortfolioHUB" (A fazer, Em andamento, Concluído).',
    '<b>Branches:</b> nomeadas por tipo (feat/, fix/, docs/), criadas a partir da main.',
    '<b>Commits:</b> padrão Conventional Commits (feat:, fix:, docs:), facilitando o histórico e as release notes.',
    '<b>Pull Requests:</b> template com checklist de testes e de segurança; merge só após o CodeQL passar.',
    '<b>Releases:</b> versões marcadas com tags (v1.0.0) e notas geradas automaticamente.'])
h2('4.3 Documentação do processo')
tabela(['Documento','Conteúdo'],[
 ['README.md','O que é o projeto, como funciona, estrutura e como rodar localmente'],
 ['docs/SETUP.md','Passo a passo completo da implantação, com comandos'],
 ['docs/GEMINI.md','Instruções do Gem e prompts usados em cada fase'],
 ['CONTRIBUTING.md','Fluxo de colaboração, padrões de branch, commit e PR'],
 ['SECURITY.md','Política de segurança e como reportar vulnerabilidades'],
],[4,12.4])
ph('Board do GitHub Projects com as issues por fase.',2.8)
ph('Pull Request com checks do CodeQL e merge realizado.',3)
story.append(PageBreak())

# ---------- 5 ----------
h1('5. Finalização da Integração e Testes')
p('Concluí as etapas restantes seguindo o checklist de testes gerado pelo Gemini e executei os testes no site publicado.')
tabela(['Teste','Resultado esperado','Status'],[
 ['Carregamento do perfil e dos projetos','Nome, foto, bio e lista exibidos',fill('OK')],
 ['Busca, filtro por linguagem e ordenação','Lista atualiza conforme o filtro',fill('OK')],
 ['Destaques','Repositórios com o tópico portfolio em "Em destaque"',fill('OK')],
 ['Responsividade (390 px)','Layout em coluna, sem rolagem horizontal',fill('OK')],
 ['Tema escuro','Cores adaptadas automaticamente',fill('OK')],
 ['Usuário inexistente (?user=...)','Mensagem de erro clara',fill('OK')],
 ['Content-Security-Policy','Console sem violações de CSP',fill('OK')],
 ['Link malicioso no campo Website','Link javascript: não é exibido',fill('OK')],
 ['Lighthouse','Acessibilidade e Boas práticas ≥ 90',fill('NOTAS',DADOS['lighthouse'])],
 ['Aba Security','Sem alertas abertos',fill('OK')],
],[5.5,8.4,2.5])
h2('Preparação para produção')
bl(['Site publicado em '+fill('URL DO SITE',DADOS['usuario'] and f'https://{U}.github.io/portfoliohub/')+' com deploy automático a cada merge.',
    'Release <b>v1.0.0</b> criada com notas automáticas: gh release create v1.0.0 --generate-notes.',
    'Monitoramento contínuo: CodeQL semanal e Dependabot.'])
ph('Relatório do Lighthouse.',3)
ph('Release v1.0.0 publicada.',2.6)
story.append(PageBreak())

# ---------- 6 ----------
h1('6. Revisão Final e Apresentação')
p('<b>Vídeo (5 min):</b> '+fill('LINK DO YOUTUBE',DADOS['video']))
h2('Roteiro da apresentação')
tabela(['Tempo','Conteúdo'],[
 ['0:00–0:30','Apresentação e o que é o PortfolioHUB'],
 ['0:30–1:10','Gem do Gemini e o plano de implantação'],
 ['1:10–2:00','Integração com o GitHub: perfil, linguagens, destaques e projetos'],
 ['2:00–3:10','Gestão de usuários e políticas de segurança'],
 ['3:10–4:00','Fluxo de colaboração: issue, PR, CodeQL, merge e deploy'],
 ['4:00–4:40','Testes e release v1.0.0'],
 ['4:40–5:00','Desafios superados e encerramento'],
],[3,13.4])
h2('Soluções implementadas e desafios superados')
tabela(['Desafio','Solução'],[
 ['Limite de 60 requisições/hora da API do GitHub sem autenticação','Cache de 10 minutos no navegador e mensagem orientando o visitante'],
 ['Exibir dados externos sem abrir brecha para XSS','Construção do DOM com textContent e validação de URLs (somente https)'],
 ['CSP restritiva bloqueando estilos inline','Estilos dinâmicos aplicados via CSSOM (element.style), permitido pela política'],
 ['Proteger a main sendo o único desenvolvedor','Ruleset com PR obrigatório e check do CodeQL, sem exigir aprovação de terceiros'],
 [fill('OUTRO DESAFIO REAL',DADOS['desafio']),fill('COMO RESOLVEU',DADOS['solucao'])],
],[7,9.4])

h1('Conclusão')
p('A implantação do PortfolioHUB resultou em uma plataforma em produção que centraliza meus projetos usando o GitHub como fonte única, '
  'com publicação automática, políticas de segurança em todas as camadas e um fluxo de colaboração documentado. O Google Gemini, configurado '
  'como um guia da trilha, acelerou o planejamento, a revisão de segurança e a definição dos testes. '+fill('Sua reflexão pessoal em 1–2 frases.',DADOS['reflexao']))

def rodape(c,d):
    c.saveState(); c.setFont('S',8); c.setFillColor(SUAVE)
    if d.page>1:
        c.drawString(2.2*cm,1.2*cm,'Implantação PortfolioHUB + IA Gemini'); c.drawRightString(A4[0]-2.2*cm,1.2*cm,str(d.page))
    c.setStrokeColor(colors.HexColor('#D6257E')); c.setLineWidth(3); c.line(0,0.6*cm,A4[0]*0.75,0.6*cm)
    c.restoreState()
doc=SimpleDocTemplate(os.path.join(BASE,'Entrega_Final_PortfolioHUB.pdf'),pagesize=A4,leftMargin=2.2*cm,rightMargin=2.2*cm,topMargin=2*cm,bottomMargin=2*cm,
    title='Implantação PortfolioHUB + IA Gemini',author=DADOS['nome'] or 'PortfolioHUB')
doc.build(story,onFirstPage=rodape,onLaterPages=rodape)

print("PDF gerado:", os.path.join(BASE,'Entrega_Final_PortfolioHUB.pdf'))
faltando=[n for n,_ in PRINTS if not os.path.exists(os.path.join(BASE,'prints',n))]
if faltando:
    print("Prints faltando em entrega/prints/:")
    for n,t in PRINTS:
        if n in faltando: print(f"  {n}  {t}")
