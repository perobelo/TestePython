import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

class bancoSQL:
    def __init__(self):
        self.cn = None
        self.cnString= (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=177.85.160.119;"
            "DATABASE=gw_GUARU_DOCE;"
            "UID=sa;"
            "PWD=jsweb2011"
        )

    def AbreConexao(self):
        try:
            self.cn = pyodbc.connect(self.cnString)
            return True
        except Exception as ex:
            return False
        
    def FechaConexao(self):
        self.cn.close()
    
st.set_page_config(
    layout="wide",
    page_title="Análise Teste"
)

bd = bancoSQL()

if  bd.AbreConexao():

    wDados = "select c1.Descricao as Categoria, (vi.Quantidade * vi.ValorUnitario) as ValorTotal, p.Descricao, v.DataVenda "
    wDados = wDados + "From Vendas v "
    wDados = wDados + "     Inner Join VendasItens vi on vi.Venda_ID = v.Internal "
    wDados = wDados + "     Inner Join Produtos p on vi.Produto_ID = p.Internal "
    wDados = wDados + "     Inner Join Classe1 c1 on p.Classe1_ID = c1.Internal "
    wDados = wDados + "Where v.DataVenda >= '20250301' "
    wDados = wDados + "And   v.DataVenda <= '20250330' "

    df = pd.read_sql(wDados, bd.cn)
    #df


    wDados = "select top 5 c1.Descricao as Categoria, sum((vi.Quantidade * vi.ValorUnitario)) as ValorTotal "
    wDados = wDados + "From Vendas v "
    wDados = wDados + "     Inner Join VendasItens vi on vi.Venda_ID = v.Internal "
    wDados = wDados + "     Inner Join Produtos p on vi.Produto_ID = p.Internal "
    wDados = wDados + "     Inner Join Classe1 c1 on p.Classe1_ID = c1.Internal "
    wDados = wDados + "Where v.DataVenda >= '20250301' "
    wDados = wDados + "And   v.DataVenda <= '20250330' "
    wDados = wDados + "Group by c1.Descricao "
    wDados = wDados + "Order by sum((vi.Quantidade * vi.ValorUnitario)) "
    dfCat = pd.read_sql(wDados, bd.cn)
    #dfCat


    col1, col2 = st.columns(2, vertical_alignment="center")
    fig1, ax1 = plt.subplots()
    ax1.pie(dfCat["ValorTotal"], labels=dfCat["Categoria"], autopct='%1.1f%%',
        shadow=False, startangle=90)

    with col1:
        st.write("Top 5 Categorias")
        st.pyplot(fig1)


    wDados = "select top 5 p.Descricao as Produto, sum((vi.Quantidade * vi.ValorUnitario)) as ValorTotal "
    wDados = wDados + "From Vendas v "
    wDados = wDados + "     Inner Join VendasItens vi on vi.Venda_ID = v.Internal "
    wDados = wDados + "     Inner Join Produtos p on vi.Produto_ID = p.Internal "
    wDados = wDados + "Where v.DataVenda >= '20250301' "
    wDados = wDados + "And   v.DataVenda <= '20250330' "
    wDados = wDados + "Group by p.Descricao "
    wDados = wDados + "Order by sum((vi.Quantidade * vi.ValorUnitario)) "
    dfProd = pd.read_sql(wDados, bd.cn)

    fig1, ax1 = plt.subplots()
    ax1.pie(dfProd["ValorTotal"], labels=dfProd["Produto"], autopct='%1.1f%%',
        shadow=False, startangle=90)
    
    with col2:
        st.write("Top 5 Produtos")
        st.pyplot(fig1)


    cc={
        "Ano1Vendas": "Vendas 2024",
        "Ano2Vendas": "Vendas 2025",
        "Ano1TicketMedio": "TM 2024",
        "Ano1TicketMedio": "TM 2025"
    }

    Ano1 = '2024'
    Ano2 = '2025'
    wDados = "sp_AnaliseTicketMedio1 '20240101', '20250330' "
    dfTM = pd.read_sql(wDados, bd.cn)
    dfTM.columns = ["Mes", "NomeMes", "Vendas 2024", "Vendas 2025", "TM 2024", "TM 2025"]
    
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.write("Ticket Médio")
        st.line_chart(dfTM, x="NomeMes", y=["TM 2024", "TM 2025"])

    with col2:
        st.write("Qtde de Vendas")
        st.line_chart(dfTM, x="NomeMes", y=["Vendas 2024", "Vendas 2025"])


    bd.FechaConexao()


def Teste():
    options = st.sidebar.selectbox(
        "Filtro por Artista",
        df["Artist"].unique()
    )

    df_Filtered = df[df["Artist"] == options]
    #df_Filtered
    #st.line_chart(df_Filtered["Energy"])

    col1, col2 = st.columns([0.7, 0.3])
    col1.pyplotpie(df["Categoria"])
    col1.line_chart(df["Categoria"])


