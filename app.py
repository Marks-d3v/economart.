import streamlit as st

# --- CONFIGURAÇÃO DE DESIGN ---
st.set_page_config(page_title="EconoMart", layout="centered")

# Estilo CSS Personalizado (Cores Laranja e Vermelho nos cards)
st.markdown("""
    <style>
    .main { background-color: #121212; } /* Fundo escuro para destacar as cores */
    
    /* Estilo do Card Laranja (Informação do Produto) */
    .card-info {
        background-color: #FF8C00; /* Laranja */
        padding: 15px;
        border-radius: 12px 12px 0px 0px;
        color: white;
        font-weight: bold;
        margin-bottom: 0px;
        border: 1px solid #e67e00;
    }
    
    /* Estilo do Botão Vermelho (Adicionar) */
    div.stButton > button {
        background-color: #FF0000 !important; /* Vermelho */
        color: white !important;
        border-radius: 0px 0px 12px 12px !important;
        width: 100% !important;
        height: 45px !important;
        border: none !important;
        font-weight: bold !important;
        margin-top: -5px !important;
        text-transform: uppercase;
    }
    
    /* Ajuste para o texto não sumir */
    h1, h2, h3, p, b { color: #ffffff; }
    
    /* Estilo das abas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #333;
        border-radius: 5px;
        color: white;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título EconoMart
st.markdown("<h1 style='text-align: center;'><span style='color: #FF0000;'>Econo</span><span style='color: #FF8C00;'>Mart</span></h1>", unsafe_allow_html=True)

# --- SISTEMA DE DADOS ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'mercados' not in st.session_state:
    st.session_state.mercados = ["Mercado 1", "Mercado 2", "Mercado 3"]
if 'dados' not in st.session_state:
    st.session_state.dados = {m: {"🥩 Carnes": {}, "🧼 Limpeza": {}, "🪥 Higiene": {}} for m in st.session_state.mercados}

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("### 👋 Acesse sua conta")
    n = st.text_input("Nome")
    e = st.text_input("E-mail")
    if st.button("🚀 ENTRAR"):
        if n and e: st.session_state.logado = True; st.rerun()
else:
    aba1, aba2 = st.tabs(["🛒 COMPRAS", "⚙️ CONFIGURAÇÕES"])

    with aba2:
        st.markdown("### ⚙️ Configurações")
        with st.expander("🏢 Nome dos Mercados"):
            for i in range(3):
                novo = st.text_input(f"Mercado {i+1}", value=st.session_state.mercados[i], key=f"m{i}")
                if novo != st.session_state.mercados[i]:
                    st.session_state.dados[novo] = st.session_state.dados.pop(st.session_state.mercados[i])
                    st.session_state.mercados[i] = novo

        with st.expander("📝 Cadastrar Produtos"):
            m_s = st.selectbox("Mercado", st.session_state.mercados)
            t_s = st.selectbox("Tópico", list(st.session_state.dados[m_s].keys()) + ["➕ Novo"])
            if t_s == "➕ Novo":
                nt = st.text_input("Nome Tópico")
                if st.button("Criar"):
                    for m in st.session_state.mercados: st.session_state.dados[m][nt] = {}
                    st.rerun()
            else:
                pn = st.text_input("Produto")
                pp = st.number_input("Preço", min_value=0.0, format="%.2f")
                if st.button("💾 SALVAR"):
                    st.session_state.dados[m_s][t_s][pn] = pp
                    st.success("Salvo!")

    with aba1:
        busca = st.text_input("🔍 Buscar produto...")
        
        if busca:
            for m in st.session_state.mercados:
                for t, prods in st.session_state.dados[m].items():
                    for p, v in prods.items():
                        if busca.lower() in p.lower():
                            # CARD LARANJA (Info)
                            st.markdown(f"""<div class='card-info'>{p}<br><small>{m} - R$ {v:.2f}</small></div>""", unsafe_allow_html=True)
                            # BOTÃO VERMELHO (Adicionar)
                            if st.button(f"Adicionar ao Carrinho", key=f"busc_{m}_{p}"):
                                st.session_state.carrinho.append({"p": p, "v": v, "m": m})
                                st.toast("Adicionado!")

        st.markdown("### 🏪 Mercados")
        for m in st.session_state.mercados:
            with st.expander(f"🏢 {m}"):
                for t, prods in st.session_state.dados[m].items():
                    st.markdown(f"**{t}**")
                    for p, v in prods.items():
                        # CARD LARANJA
                        st.markdown(f"""<div class='card-info'>{p}<br><small>R$ {v:.2f}</small></div>""", unsafe_allow_html=True)
                        # BOTÃO VERMELHO
                        if st.button(f"ADICIONAR +", key=f"lis_{m}_{p}"):
                            st.session_state.carrinho.append({"p": p, "v": v, "m": m})
                            st.toast("No carrinho!")

    # RODAPÉ TOTAL
    tot = sum(item['v'] for item in st.session_state.carrinho)
    st.markdown("---")
    with st.expander(f"🛒 TOTAL: R$ {tot:.2f}"):
        for i, it in enumerate(st.session_state.carrinho):
            c1, c2 = st.columns([3, 1])
            c1.write(f"{it['p']} ({it['m']})")
            if c2.button("🗑️", key=f"d_{i}"):
                st.session_state.carrinho.pop(i)
                st.rerun()
