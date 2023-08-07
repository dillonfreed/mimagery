# Bring in deps
import os 
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

st.secrets[apikey] 

# App framework

st.title('🖤MEMORY PALACE CREATOR')
prompt = st.text_input('Create your memory palace, list the furntire in your room, and then add whatever you wish to learn (e.g.the first 10 elements of the periodic table). Here is an example of how the input should look: desk, table, chair, pillow, blanket, stove, picture, furnace, desk \\ I want to learn the most important 10 wars of the 20th century in chronological order') 


# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],  
    template='"""You are a master at hleping people remember things by using the Method of Loci \
        Users will input a list of the furntire they have in their room in order \
            So your first task is to create a numebered list for those user inputs \
        which again is a list of the furniture items for the user input \
        we will cal this ListA \
        The user will also input thta which they wish to learn \
        The user may input anything that they wish to learn \
        You should generate a numbered outline of that which they wish to learn \
       This will be called ListB \
        so you need to make sure you produce two lists - to reiterate the first list is the items of the user inputs \
                the second list will of the topic that the user wishes to learn that you create \
        Next, make a third list which we will call ListC will be crated by you \
             ListC will provide a symbol for each item of ListB only\
        that is, you will create a relavant image that would is symbolic would immediately recognize as an assocation for each item in ListB \
        no symbol on List C may be used more than once \
        items on ListA are presented in counterclockwise fashion \
                   Here are some examples of images: for Russia: Bear; Hydrogen: Zeppelin blimp; NYC: A Big Apple; etc. \
                    these symbols will be used to create a Method of Loci story {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title'], 
    template='Now, create a "method of loci"story with the ListA and ListC that you created \
    combing the symbols with the furnitue in a unique and memorable way \
    assume all the furniture is in one room \
    an example would be the symbol you created is using the furniture in some odd way \
        in other words, so that ListA items are used in order \
          with the learning material on ListC {title} '
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

    
