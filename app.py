import streamlit as st

# --- DESIGN E CORES ATUALIZADOS ---
st.set_page_config(page_title="EconoMart", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #121212; }
    .titulo-centralizado { text-align: center; margin-bottom: 20px; }

    /* Card Laranja Padrão */
    .card-info {
        background-color: #FF8C00; 
        padding: 12px;
        border-radius: 15px 15px 0px 0px;
        color: white;
        font-weight: bold;
        text-align: center;
        border: 1px solid #e67e00;
    }

    /* Card Destaque (Mais Barato) */
    .card-melhor-preco {
        background-color: #FF8C00; 
        padding: 12px;
        border-radius: 15px 15px 0px 0px;
        color: white;
        font-weight: bold;
        text-align: center;
        border: 4px solid #00FF7F; /* Borda Verde Brilhante */
    }
    
    .selo-economia {
        background-color: #00FF7F;
        color: #000;
        font-size: 10px;
        padding: 2px 8px;
        border-radius: 10px;
        margin-bottom: 5px;
        display: inline-block;
    }

    /* Botão Vermelho Largo */
    div.stButton > button {
        background-color: #FF0000 !important; 
        color: white !important;
        border-radius: 0px 0px 15px 15px !important;
        width: 100% !important;
        height: 50px !important;
        border: none !important;
        font-weight: bold !important;
        margin-top: -2px !important;
    }
    
    h2, h3, span, label { color: #ffffff !important; }
    div[data-testid="stTextInput"] label { display: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-centralizado'><h1><span style='color: #FF0000;'>Econo</span><span style='color: #FF8C00;'>Mart</span></h1></div>", unsafe_allow_html=True)

# --- DADOS ---
if 'logado' not in st.session_state: st.session_state.logado = False
if 'carrinho' not in st.session_state: st.session_state.carrinho = []
if 'mercados' not in st.session_state: st.session_state.mercados = ["Mercado 1", "Mercado 2", "Mercado 3"]
if 'dados' not in st.session_state:
    st.session_state.dados = {m: {"🥩 Carnes": {}, "🧼 Limpeza": {}, "🪥 Higiene": {}} for m in st.session_state.mercados}

if not st.session_state.logado:
    st.markdown("<h3 style='text-align:center;'>👋 Bem-vindo!</h3>", unsafe_allow_html=True)
    n = st.text_input("Nome", placeholder="Nome")
    e = st.text_input("E-mail", placeholder="E-mail")
    if st.button("🚀 ENTRAR"):
        if n and e: st.session_state.logado = True; st.rerun()
else:
    aba1, aba2 = st.tabs(["🛒 COMPRAS", "⚙️ CONFIGURAÇÕES"])

    with aba2:
        st.subheader("⚙️ Configurações")
        with st.expander("🏢 Nomes dos Mercados"):
            for i in range(3):
                novo = st.text_input(f"Mercado {i+1}", value=st.session_state.mercados[i], key=f"m{i}")
                if novo != st.session_state.mercados[i]:
                    st.session_state.dados[novo] = st.session_state.dados.pop(st.session_state.mercados[i])
                    st.session_state.mercados[i] = novo
        with st.expander("📝 Cadastrar Produtos"):
            ms = st.selectbox("Mercado", st.session_state.mercados)
            ts = st.selectbox("Tópico", list(st.session_state.dados[ms].keys()) + ["➕ Novo"])
            if ts == "➕ Novo":
                nt = st.text_input("Nome do Tópico")
                if st.button("Criar"):
                    for m in st.session_state.mercados: st.session_state.dados[m][nt] = {}
                    st.rerun()
            else:
                pn = st.text_input("Produto", placeholder="Ex: Cerveja")
                pp = st.number_input("Preço", min_value=0.0, format="%.2f")
                if st.button("💾 SALVAR"):
                    st.session_state.dados[ms][ts][pn] = pp
                    st.success("Salvo!")

    with aba1:
        busca = st.text_input("busca_interna", placeholder="🔍 Buscar produto...")
        
        if busca:
            resultados = []
            for m in st.session_state.mercados:
                for t, prods in st.session_state.dados[m].items():
                    for p, v in prods.items():
                        if busca.lower() in p.lower():
                            resultados.append({'p': p, 'v': v, 'm': m})
            
            if resultados:
                # Encontrar o menor preço da lista
                menor_preco = min(r['v'] for r in resultados)
                
                for res in resultados:
                    is_mais_barato = (res['v'] == menor_preco)
                    estilo_card = "card-melhor-preco" if is_mais_barato else "card-info"
                    selo = "<div class='selo-economia'>🥇 MELHOR PREÇO 💸</div><br>" if is_mais_barato else ""
                    
                    st.markdown(f"""
                        <div class='{estilo_card}'>
                            {selo}{res['p']}<br>
                            <span style='font-size:12px;'>{res['m']} - R$ {res['v']:.2f}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"ADICIONAR {res['p']} ({res['m']})", key=f"b_{res['m']}_{res['p']}"):
                        st.session_state.carrinho.append(res)
                        st.toast("Adicionado!")
            else:
                st.warning("Nenhum produto encontrado.")

        st.markdown("### 🏪 Mercados")
        for m in st.session_state.mercados:
            with st.expander(f"🏢 {m}"):
                for t, prods in st.session_state.dados[m].items():
                    if prods:
                        st.markdown(f"**{t}**")
                        for p, v in prods.items():
                            st.markdown(f"<div class='card-info'>{p}<br><span style='font-size:12px;'>R$ {v:.2f}</span></div>", unsafe_allow_html=True)
                            if st.button(f"ADICIONAR {p}", key=f"l_{m}_{p}"):
                                st.session_state.carrinho.append({'p': p, 'v': v, 'm': m})
                                st.toast("No carrinho!")

    # TOTAL
    total_val = sum(i['v'] for i in st.session_state.carrinho)
    st.markdown("---")
    with st.expander(f"🛒 TOTAL NO CARRINHO: R$ {total_val:.2f}"):
        for idx, item in enumerate(st.session_state.carrinho):
            c1, c2 = st.columns([3, 1])
            c1.write(f"{item['p']} - {item['m']}")
            if c2.button("🗑️", key=f"del_{idx}"):
                st.session_state.carrinho.pop(idx)
                st.rerun()
