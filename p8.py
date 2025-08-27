import streamlit as st
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from streamlit_chat import message
from MyLCH import getOpenAI

st.markdown("Page 8")
st.sidebar.markdown("Clicked Page 8")

if 'MEMORY' not in st.session_state:
    memory = ConversationSummaryMemory(
        llm = getOpenAI(),
        return_messages=True
    )
    # add to the session
    st.session_state['MEMORY'] = memory

chain =  ConversationChain( llm=getOpenAI(),  memory=st.session_state['MEMORY'] )
def conversational_chat(query):  # 질문을 LLM에 전달 하고 결과를 받는다
    result = chain.predict(input=query)
    st.session_state['chathistory'].append((query, result))

def init_chathistory():
    st.session_state['chathistory'] = [("안녕하세요!", "안녕하세요!  전 당신에 사랑스러운 귀염둥이 입니다. ")]

if 'chathistory' not in st.session_state:
    init_chathistory()

# 사용자가 입력한 문장에 대한 컨테이너
container = st.container()
# 챗봇 이력에 대한 컨테이너
response_container = st.container(border=True)

# 질문 영역
with container:
    with st.form(key='Conv_Question', clear_on_submit=True):
        user_input = st.text_input("Query:", placeholder="무엇이든 물어보세요? (:", key='input')
        submit_button = st.form_submit_button(label='Send')
    if submit_button and user_input:
        conversational_chat(user_input)
    if st.button("Clear"):
        init_chathistory()


# 답변 영역
if st.session_state['chathistory']:
    with response_container:
        for i in range(len(st.session_state['chathistory'])-1 , -1, -1):
            message(st.session_state["chathistory"][i][1], key=str(i), avatar_style = "bottts")
            message(st.session_state["chathistory"][i][0], is_user=True, key=str(i) + '_user', avatar_style = "fun-emoji")


