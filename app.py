import requests
# from functools import cache
import pandas as pd
import streamlit as st
from PIL import Image

def hX2():
    pass

def header():
    img = Image.open("images/kegg128.png")
    st.set_page_config(page_title="KEGG TERMS & METABOLITES", page_icon=img, layout="wide")
    st.sidebar.image("images/kegg128.png", use_column_width='never', caption='Kegg')
    st.title("KEGG TERMS & METABOLITES")
    st.sidebar.subheader("This app connects kegg terms with kegg compound database")
    st.sidebar.markdown("I have parsed all the available kegg modules from this [link](https://www.genome.jp/kegg/docs/module_statistics.html).\n\nFor each module_id I have collected all the associated kegg terms and its associated compound information.")
    st.sidebar.markdown("- Select the KEGG term to view the data frame")
    st.sidebar.markdown("- Once a perticular KEGG term is selected you can find more about the compound id or kegg terms or module ids using the dropdown")
    st.sidebar.markdown("- Flat files or Images can be pulled down using the kegg rest API")
    st.markdown("---")

    
def footer():
    st.markdown('---')
    st.markdown(" P @ 2021")
    
def _make_url(term):
    """
    Retrun a url
    """
    return f"http://rest.kegg.jp/get/{term}"

def get_df():
    return pd.read_csv("data/module_kegg_and_compound_df.tsv", sep="\t")

@st.cache(suppress_st_warning=True)
def get_rest_data(term):
    url = _make_url(term)
    r = requests.get(url)
    if r.status_code == 200:
        _ = r.content.decode()
        if len(_) >2 :
            st.text(_)
        else:
            return("Didn't retreive anything")
        # print(_)
    else :
        return(f"Status Code : {r.status_code}")    

@st.cache(suppress_st_warning=True)
def get_image(term):
    url = f"http://rest.kegg.jp/get/{term}/image"
    r = requests.get(url)
    if r.status_code == 200:
        st.image(r.content)

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# --------------------------
hX2()

header()

df = get_df()
# all_module_names = sorted(df.module.unique())
all_kegg_names = sorted(df.kegg_term.unique())

st.info('## Search kegg terms in the data frame')
kt = st.selectbox('', all_kegg_names)
df_selected = df[df.kegg_term == kt].reset_index(drop=True)
st.dataframe(df_selected)
csv = convert_df(df_selected)
csv2 = convert_df(df)
st.sidebar.markdown("---")
st.sidebar.download_button(label="Download Selected Data", data=csv, file_name='selected_data.csv',mime='text/csv')
st.sidebar.download_button(label="Download All Data", data=csv, file_name='data.csv',mime='text/csv')
# st.table(df_selected)
st.markdown("---")
# --------------------------
st.info('## Get the flat file for compound ids from kegg rest API')

ids = sorted(df_selected.compound_id.unique().tolist()) 
A1, A2 = st.columns([1,3])
with A1:
    selection = st.selectbox('Select Compound Terms', ids )
    resA = st.button("submit")
    if st.button("Clear"):
        resA = False
with A2:      
    if resA:
        get_image(selection)
        get_rest_data(selection)
st.markdown("---")
# --------------------------
st.info('## Get the flat file for module ids or kegg ids from kegg rest API')

ids2 = sorted(df_selected.module.unique().tolist() + df_selected.kegg_term.unique().tolist())
B1, B2 = st.columns([1,3])
with B1:
    selection2 = st.selectbox('Select Kegg Terms or Module IDs', ids2)
    resB = st.button("submit!")
    if st.button("Clear!"):
        resB = False
with B2:
    if resB:
        get_rest_data(selection2)
st.markdown("---")
# --------------------------

st.info("## Get the flat file for any ID which is not in the curated data frame")
C1, C2 = st.columns([1,3])
with C1:
    orphan_kid = st.text_input(label="", value='K06595')
    resC = st.button("submit!!")
    if st.button("Clear!!"):
        resC = False
with C2:
    if resC:
        get_rest_data(orphan_kid)
st.markdown("---")  
  
# -------------
st.header("Get the Image for pathway, compound, reaction or map")
D1, D2 = st.columns([1,3])
with D1:
    orphan_kid2 = st.text_input(label="", value='map01110')
    resD = st.button("submit!!!")
    if st.button("Clear!!!"):
        resD = False
with D2:
    if resD:
        get_image(orphan_kid2)
# st.markdown("---")
# ---------------
footer()




