# Bring in deps


import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('🖤MEMORY PALACE CREATOR')
prompt = st.text_input('Create your memory palace, list the furntire in your room, and then add whatever you wish to learn (e.g.the first 10 elements of the periodic table). Here is an example of how the input should look: desk, table, chair, pillow, blanket, stove, picture, furnace, desk \\ I want to learn the most important 10 wars of the 20th century in chronological order') 

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='First, create a numebered list 1 which is a list the furniture items for the user input. Second, create a break and an enitrely new list called list 2 by producing whatever the user user wishes to learn. Create a relavant image that any educated would immediately recognize as an assocation for each item in list #2. {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title'], 
    template='Create a memory palace story with the two lists, lining up each number and using the relavant symbolic images.  {title} '
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    script = script_chain.run(title=title)

    st.write(title) 
    st.write(script) 

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    
