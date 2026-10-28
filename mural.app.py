import streamlit as st
import sqlite3
from datetime import datetime

# ------------------- CONFIGURAÇÕES INICIAIS -------------------
st.set_page_config(
    page_title="Mural Sustentável",
    page_icon="🌱",
    layout="wide"
)

# ------------------- BANCO DE DADOS -------------------
def criar_banco():
    conn = sqlite3.connect("dicas.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            dica TEXT NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def cadastrar_dica(nome, categoria, dica):
    conn = sqlite3.connect("dicas.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dicas (nome, categoria, dica) VALUES (?, ?, ?)', (nome, categoria, dica))
    conn.commit()
    conn.close()
    st.success("✅ Dica cadastrada com sucesso!")

def buscar_dicas(filtro_categoria=None):
    conn = sqlite3.connect("dicas.db")
    cursor = conn.cursor()
    if filtro_categoria and filtro_categoria != "Todas":
        cursor.execute('SELECT * FROM dicas WHERE categoria = ? ORDER BY data DESC', (filtro_categoria,))
    else:
        cursor.execute('SELECT * FROM dicas ORDER BY data DESC')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def editar_dica(id_dica, nova_categoria, nova_dica):
    conn = sqlite3.connect("dicas.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE dicas SET categoria = ?, dica = ? WHERE id = ?', (nova_categoria, nova_dica, id_dica))
    conn.commit()
    conn.close()
    st.info("✏️ Dica atualizada!")

def excluir_dica(id_dica):
    conn = sqlite3.connect("dicas.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dicas WHERE id = ?', (id_dica,))
    conn.commit()
    conn.close()
    st.warning("🗑️ Dica removida!")

# Cria o banco automaticamente na primeira vez
criar_banco()

# ------------------- MENU DE NAVEGAÇÃO -------------------
menu = st.sidebar.selectbox(
    "📋 Navegação",
    ["🏠 Início", "✍️ Enviar Dica", "📖 Ver Todas as Dicas", "🛠️ Editar ou Excluir"]
)

# Estilo visual
st.markdown("""
<style>
div.stButton > button { background-color: #2e8b57; color: white; border-radius: 8px; }
div.stButton > button:hover { background-color: #228b22; }
</style>
""", unsafe_allow_html=True)

# ------------------- PÁGINAS -------------------
if menu == "🏠 Início":
    st.title("🌱 Mural Comunitário de Dicas e Ações Sustentáveis")
    st.subheader("Um espaço para compartilhar boas ideias!")
    st.image("https://images.unsplash.com/photo-1542601906990-2d37e1e2a295?w=800", caption="Cuidar do mundo é uma tarefa de todos")
    st.write("""
    Este projeto foi criado para que possamos trocar dicas simples sobre:
    ♻️ Reciclagem  
    💧 Economia de água  
    💡 Economia de energia  
    🥗 Alimentação saudável  
    🌳 Preservação do meio ambiente  
    """)
    st.info("Escolha uma opção no menu ao lado para navegar!")

elif menu == "✍️ Enviar Dica":
    st.header("✍️ Compartilhe sua dica")
    with st.form("form_dica"):
        nome = st.text_input("Seu nome ou apelido")
        categoria = st.selectbox("Categoria", ["Reciclagem", "Água", "Energia", "Alimentação", "Outros"])
        dica = st.text_area("Sua dica ou ação sustentável")
        enviar = st.form_submit_button("Cadastrar Dica")
        
        if enviar:
            if nome and dica:
                cadastrar_dica(nome, categoria, dica)
            else:
                st.error("Preencha o nome e a dica antes de enviar!")

elif menu == "📖 Ver Todas as Dicas":
    st.header("📖 Dicas da Comunidade")
    filtro = st.selectbox("Filtrar por categoria", ["Todas", "Reciclagem", "Água", "Energia", "Alimentação", "Outros"])
    todas_dicas = buscar_dicas(filtro)
    
    if not todas_dicas:
        st.info("Ainda não há dicas cadastradas. Seja o primeiro a compartilhar!")
    else:
        for d in todas_dicas:
            with st.expander(f"📌 {d[2]} - por {d[1]}"):
                st.write(f"**Dica:** {d[3]}")
                st.caption(f"Enviado em: {d[4]}")

elif menu == "🛠️ Editar ou Excluir":
    st.header("🛠️ Gerenciar suas dicas")
    st.warning("⚠️ Anote o número (ID) da dica que quer alterar ou remover")
    lista = buscar_dicas()
    
    if lista:
        for d in lista:
            st.write(f"ID: {d[0]} | {d[2]} | {d[1]}: {d[3]}")
        
        st.divider()
        opcao = st.radio("O que você quer fazer?", ["Editar", "Excluir"])
        id_escolhido = st.number_input("Digite o ID da dica", min_value=1, step=1)
        
        if opcao == "Editar":
            nova_cat = st.selectbox("Nova categoria", ["Reciclagem", "Água", "Energia", "Alimentação", "Outros"])
            nova_dica = st.text_area("Nova dica")
            if st.button("Salvar Alteração"):
                if nova_dica:
                    editar_dica(id_escolhido, nova_cat, nova_dica)
                else:
                    st.error("Escreva a nova dica!")
        
        if opcao == "Excluir":
            confirma = st.button("Confirmar Exclusão")
            if confirma:
                excluir_dica(id_escolhido)
