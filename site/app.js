(() => {
  "use strict";
  const cfg = window.PORTFOLIOHUB_CONFIG || {};
  // ?user=fulano permite testar com outro perfil sem editar o config (validado contra o formato de login do GitHub)
  const param = new URLSearchParams(location.search).get("user");
  const usuario = /^[a-z\d](?:[a-z\d-]{0,38})$/i.test(param || "") ? param : cfg.usuario;
  const API = "https://api.github.com";
  const CORES = { JavaScript:"#C9A100", TypeScript:"#3178C6", HTML:"#E34C26", CSS:"#663399", Python:"#4B8B3B",
    Java:"#B07219", "C#":"#178600", "C++":"#F34B7D", C:"#555555", PHP:"#4F5D95", Go:"#00ADD8", Shell:"#5FA83A",
    Vue:"#41B883", Dart:"#00B4AB", Kotlin:"#A97BFF", Ruby:"#701516", Rust:"#B7410E", Outra:"#8A96A3" };
  const $ = (id) => document.getElementById(id);
  // Todo conteúdo vindo da API entra via textContent (nunca innerHTML) para impedir XSS
  const el = (tag, props = {}, ...filhos) => {
    const n = document.createElement(tag);
    Object.entries(props).forEach(([k, v]) => {
      if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v);
    });
    filhos.forEach((f) => f && n.append(f));
    return n;
  };
  // Só aceita links https (bloqueia javascript:, data: etc. vindos do campo homepage)
  const urlSegura = (u) => { try { const x = new URL(u); return x.protocol === "https:" ? x.href : null; } catch { return null; } };
  const dataBR = (iso) => new Date(iso).toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });

  let repos = [];
  const estado = { busca: "", lang: "", ordem: "updated" };

  async function getJSON(caminho) {
    const chave = "phub:" + caminho;
    try {
      const c = JSON.parse(sessionStorage.getItem(chave) || "null");
      if (c && Date.now() - c.t < (cfg.cacheMinutos || 10) * 60000) return c.d;
    } catch { /* cache indisponível */ }
    const r = await fetch(API + caminho, { headers: { Accept: "application/vnd.github+json" } });
    if (r.status === 403 || r.status === 429) throw new Error("limite");
    if (r.status === 404) throw new Error("naoencontrado");
    if (!r.ok) throw new Error("falha");
    const d = await r.json();
    try { sessionStorage.setItem(chave, JSON.stringify({ t: Date.now(), d })); } catch { /* ok */ }
    return d;
  }

  function renderPerfil(u) {
    $("nome").textContent = u.name || u.login;
    $("bio").textContent = u.bio || `${u.public_repos} repositórios públicos no GitHub.`;
    const av = $("avatar");
    const src = urlSegura(u.avatar_url);
    if (src) { av.src = src; av.alt = `Foto de ${u.login}`; av.hidden = false; }
    const lp = $("link-perfil");
    const href = urlSegura(u.html_url);
    if (href) { lp.href = href; lp.hidden = false; }
    document.title = `${u.name || u.login} · PortfolioHUB`;
  }

  function renderBarra() {
    const cont = {};
    repos.forEach((r) => { const l = r.language || "Outra"; cont[l] = (cont[l] || 0) + 1; });
    const total = repos.length || 1;
    const barra = $("barra"); barra.replaceChildren();
    const sel = $("lang");
    Object.entries(cont).sort((a, b) => b[1] - a[1]).forEach(([l, n]) => {
      const b = el("button", { type: "button", class: "fatia", "aria-pressed": "false", "data-lang": l, title: `${l}: ${n}` },
        el("span", { class: "rotulo", text: `${l} ${Math.round((n / total) * 100)}%` }));
      b.style.flexGrow = n;
      b.style.setProperty("--cor", CORES[l] || CORES.Outra);
      b.addEventListener("click", () => { estado.lang = estado.lang === l ? "" : l; sel.value = estado.lang; render(); });
      barra.append(b);
      sel.append(el("option", { value: l, text: l }));
    });
  }

  function itemRepo(r, destaque) {
    const repoUrl = urlSegura(r.html_url);
    const demo = urlSegura(r.homepage);
    const lang = r.language || "Outra";
    const ponto = el("i", { class: "ponto", "aria-hidden": "true" });
    ponto.style.background = CORES[lang] || CORES.Outra;
    const meta = el("p", { class: "meta" },
      el("span", { class: "lang" }, ponto, document.createTextNode(lang)),
      el("span", { text: `★ ${r.stargazers_count}` }),
      el("span", { text: `Atualizado em ${dataBR(r.pushed_at)}` }));
    const acoes = el("p", { class: "acoes" },
      repoUrl ? el("a", { href: repoUrl, target: "_blank", rel: "noopener noreferrer", text: "Código" }) : null,
      demo ? el("a", { href: demo, target: "_blank", rel: "noopener noreferrer", class: "demo", text: "Abrir demo" }) : null);
    return el("li", { class: destaque ? "destaque" : "repo" },
      el("h3", { text: r.name }),
      el("p", { class: "desc", text: r.description || "Sem descrição." }),
      meta, acoes);
  }

  function render() {
    document.querySelectorAll(".fatia").forEach((b) =>
      b.setAttribute("aria-pressed", String(!!estado.lang && b.dataset.lang === estado.lang)));
    const q = estado.busca.toLowerCase();
    const lista = repos.filter((r) =>
      (!estado.lang || (r.language || "Outra") === estado.lang) &&
      (!q || r.name.toLowerCase().includes(q) || (r.description || "").toLowerCase().includes(q)));
    const ord = { updated: (a, b) => new Date(b.pushed_at) - new Date(a.pushed_at),
      stars: (a, b) => b.stargazers_count - a.stargazers_count, name: (a, b) => a.name.localeCompare(b.name) };
    lista.sort(ord[estado.ordem]);
    $("lista").replaceChildren(...lista.map((r) => itemRepo(r, false)));
    $("status").textContent = lista.length
      ? `${lista.length} de ${repos.length} projetos`
      : "Nenhum projeto com esse filtro. Limpe a busca ou escolha outra linguagem.";
  }

  function erro(e) {
    const msg = {
      limite: "O GitHub limitou as consultas deste navegador (60 por hora). Tente de novo em alguns minutos.",
      naoencontrado: `O usuário “${usuario}” não existe no GitHub. Confira o campo usuario em config.js.`,
    }[e.message] || "Não foi possível falar com a API do GitHub. Verifique a conexão e recarregue a página.";
    $("status").textContent = msg; $("bio").textContent = msg;
  }

  async function iniciar() {
    if (!usuario || usuario === "SEU_USUARIO_GITHUB") {
      $("status").textContent = "Defina seu usuário do GitHub em site/config.js."; $("bio").textContent = ""; return;
    }
    try {
      const [u, rs] = await Promise.all([
        getJSON(`/users/${encodeURIComponent(usuario)}`),
        getJSON(`/users/${encodeURIComponent(usuario)}/repos?per_page=100&sort=pushed`)]);
      renderPerfil(u);
      repos = rs.filter((r) => (cfg.incluirForks || !r.fork) && !r.private);
      const dest = repos.filter((r) => (r.topics || []).includes(cfg.topicoDestaque));
      if (dest.length) { $("sec-destaques").hidden = false; $("destaques").replaceChildren(...dest.map((r) => itemRepo(r, true))); }
      renderBarra(); render();
    } catch (e) { erro(e); }
  }

  $("busca").addEventListener("input", (e) => { estado.busca = e.target.value.slice(0, 80); render(); });
  $("lang").addEventListener("change", (e) => { estado.lang = e.target.value; render(); });
  $("ordem").addEventListener("change", (e) => { estado.ordem = e.target.value; render(); });
  iniciar();
})();
