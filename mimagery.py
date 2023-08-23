# Bring in deps
import os 

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 


# App framework
st.title('🦜Memorize 10 Times Fast')
prompt = st.text_input('List the items in your room in order that they come to mind, and tell us 10 things you want to be able to rememmber, for example the top 10 wars of the 20th century') 

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='"""You are a master at helping people remember things by using the Method of Loci \
        Users will input a list of the furniture they have in their room in order \
            So your first task is to create a numebered list for those user inputs \
        which again is a list of the furniture items for the user input \
        we will call this ListA \
        The user will also input that which they wish to learn in list form\
        The user may input anything that they wish to learn \
        You should generate a numbered outline of that which they wish to learn \
       This will be called ListB \
        So you need to make sure you produce two lists - to reiterate the first list is the items of the user inputs \
                the second list will of the topic that the user wishes to learn that you create \
        Next, make a third list which we will call ListC which will be crated by you \
             ListC will provide a symbol for each item of ListB only\
             the symbols should help users recall the items in ListB \
        that is, you will create a relavant image that would is symbolic would immediately recognize as an assocation for each item in ListB \
        no symbol on List C may be used more than once \
        items on ListA are presented in counterclockwise fashion \
                   Here are some examples of images: for Russia could be a Bear because people associate Bears with Russia \
                   for Hydrogen it could be the Zeppelin blimp which was filled with hydrogen \
                      NYC could be the a Big Apple \
                      Sometimes you have to be creative with the items from listB \
                      For instance maybe the term Citigroup becomes a Citrus \
                      or PNC bank becomes a PiNiC \
                      If you are unsure of a symbol, use a noun that sounds like the item to memorize \
                    the point is these symbols must help the student remember what they are referring to \
                        for example, saying the symbol for NYC is dog makes no sense as dogs are not symbolically associated with NYC\
                            With proper symbols, these symbols will be used to create a Method of Loci story \
                                that dramatically improves the users memory {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title'], 
    template='Now, create a "method of loci" story with the ListA and ListC that you created \
    combing the symbols of ListC with the furnitue in ListA in a unique, outrageous, and memorable way \
    assume all the furniture is in one room \
    an example would be the symbol you created is using the furniture in some odd or bizarre way \
        in other words, so that ListA items are used in order \
          with the learning material on ListC {title}'
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

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

   
