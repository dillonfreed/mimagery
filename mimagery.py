import os
import streamlit as st
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = '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'

st.title = ('Mimagery')
prompt = st.text_input('Enter your prompt here')
llm = OpenAI(temperature=0.9)

if prompt:
 response = llm(prompt)
 st.write(response) 




