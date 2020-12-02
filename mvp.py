import streamlit as st
import pandas as pd
import numpy as np
import udregninger

st.title("Bob Callservice")

phonerID = st.selectbox(
     'Vælg Caller ID:',
    ('1', '2', '3','4', '5', '6','7', '8', '9','10', '11', '12','13', '14', '15', '16'))

tid = st.selectbox(
     'Vælg tidsrum',
    ('Morgen','Middag','Aften'))

st.write("")

if phonerID:
    _, ppostnr, pkøn = udregninger.dfphonere.loc[int(phonerID)-1,:]
    st.write(f'God{tid.lower()}, Phoner', phonerID)
    st.write(f'Som {"kvinde" if pkøn=="F" else "mand"} fra {ppostnr} matcher du i tidsrummet {tid} med følgende kunder:')


from datetime import datetime

now = datetime.now().time().hour

st.write(udregninger.poc(int(phonerID),tid))