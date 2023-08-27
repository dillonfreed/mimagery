import os
import streamlit as st
from langchain.llms import OpenAI

os.environ['api_key'] == st.secrets['api_key']

st.title = ('Mimagery')
prompt = st.text_input('Enter your prompt here')
llm = OpenAI(temperature=0.9)

if prompt:
 response = llm(prompt)
 st.write(response) 




