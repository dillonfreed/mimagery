# Bring in deps
import os 
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

# App framework

st.title('🖤MEMORY PALACE CREATOR')
prompt = st.text_input('Create your memory palace, list the furntire in your room, and then add whatever you wish to learn (e.g.the first 10 elements of the periodic table). Here is an example of how the input should look: desk, table, chair, pillow, blanket, stove, picture, furnace, desk \\ I want to learn the most important 10 wars of the 20th century in chronological order') 


# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],  
    template='"""You are a master at hleping people remember things by using the Method of Loci  {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title'], 
    template='Now, create a "method of loci"story with the ListA and ListC that you created {title} '
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    script = script_chain.run(title=title)

    st.write(title) 
    st.write(script) 

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    
