import streamlit as st

# --- CONFIGURAÇÃO DE DESIGN E CORES ---
st.set_page_config(page_title="EconoMart", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #121212; }
    
    /* Centralizar Título */
    .titulo-centralizado {
        text-align: center;
        margin-bottom: 20px;
    }

    /* Estilo do Card Laranja (Informação do Produto) */
    .card-info {
        background-color: #FF8C00; 
        padding: 12px;
        border-radius: 15px 15px 0px 0px;
        color: white;
        font-weight: bold;
        margin-bottom: 0px;
        border: 1px solid #e67e00;
        text-align: center;
    }
    
    /* Estilo do Botão Vermelho (Adicionar) */
    div.stButton > button {
        background-color: #FF0000 !important; 
        color: white !important;
        border-radius: 0px 0px 15px 15px !important;
        width: 100% !important;
        height: 50px !important;
        border: none !important;
        font-weight: bold !important;
        margin-top: -2px !important;
        font-size: 16px !important;
    }
    
    /* Ajuste de cor de textos gerais */
    h2, h3, span, label { color: #ffffff !important; }
    
    /* Esconder o label (nome) da barra de pesquisa para ficar só o interno */
    div[data-testid="stTextInput"] label {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Nome Centralizado
st.markdown("""
    <div class='titulo-centralizado'>
        <h1><span style='color: #FF0000;'>Econo</span><span style='color: #FF8C00;'>Mart</span></h1>
    </div>
""", unsafe_allow_html=True)

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
    st.markdown("<h3 style='text-align:center;'>👋 Bem-vindo!</h3>", unsafe_allow_html=True)
    n = st.text_input("Nome", placeholder="Digite seu nome")
    e = st.text_input("E-mail", placeholder="seu@email.com")
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
                pn = st.text_input("Produto", placeholder="Ex: Arroz")
                pp = st.number_input("Preço", min_value=0.0, format="%.2f")
                if st.button("💾 SALVAR"):
                    st.session_state.dados[m_s][t_s][pn] = pp
                    st.success("Salvo!")

    with aba1:
        # 2. Barra de Pesquisa com texto interno (Placeholder)
        busca = st.text_input("busca_interna", placeholder="🔍 Buscar produto...")
        
        if busca:
            st.markdown(f"**Resultados para: {busca}**")
            for m in st.session_state.mercados:
                for t, prods in st.session_state.dados[m].items():
                    for p, v in prods.items():
                        if busca.lower() in p.lower():
                            st.markdown(f"<div class='card-info'>{p}<br><span style='font-size:12px;'>{m} - R$ {v:.2f}</span></div>", unsafe_allow_html=True)
                            if st.button(f"ADICIONAR {p}", key=f"busc_{m}_{p}"):
                                st.session_state.carrinho.append({"p": p, "v": v, "m": m})
                                st.toast("No carrinho!")

        st.markdown("### 🏪 Mercados")
        for m in st.session_state.mercados:
            with st.expander(f"🏢 {m}"):
                for t, prods in st.session_state.dados[m].items():
                    st.markdown(f"**{t}**")
                    for p, v in prods.items():
                        st.markdown(f"<div class='card-info'>{p}<br><span style='font-size:12px;'>R$ {v:.2f}</span></div>", unsafe_allow_html=True)
                        if st.button(f"ADICIONAR +", key=f"lis_{m}_{p}"):
                            st.session_state.carrinho.append({"p": p, "v": v, "m": m})
                            st.toast("No carrinho!")

    # RODAPÉ TOTAL
    tot = sum(item['v'] for item in st.session_state.carrinho)
    st.markdown("---")
    with st.expander(f"🛒 TOTAL: R$ {tot:.2f}"):
        if st.session_state.carrinho:
            for i, it in enumerate(st.session_state.carrinho):
                c1, c2 = st.columns([3, 1])
                c1.write(f"{it['p']} ({it['m']})")
                if c2.button("🗑️", key=f"d_{i}"):
                    st.session_state.carrinho.pop(i)
                    st.rerun()
        else:
            st.write("Vazio")
