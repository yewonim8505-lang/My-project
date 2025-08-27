import tempfile
import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from streamlit_chat import message
from MyLCH import getOpenAI

st.markdown("Page4")
st.sidebar.markdown("Clicked Page4")

uploaded_file = st.sidebar.file_uploader("upload", type="pdf")

if uploaded_file :
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    loader = PyPDFLoader(tmp_file_path)
    data = loader.load()
    embeddings = OpenAIEmbeddings()
    vectors = FAISS.from_documents(data, embeddings)

    chain = ConversationalRetrievalChain.from_llm(llm = getOpenAI(), retriever=vectors.as_retriever())

    def conversational_chat(query):  # 문맥 유지를 위해 과거 대화 저장 이력에 대한 처리
        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))

    if 'history' not in st.session_state:
        st.session_state['history'] = [("안녕하세요!","안녕하세요! " + uploaded_file.name + "에 관해 질문주세요." )]

    # 챗봇 이력에 대한 컨테이너
    response_container = st.container()
    # 사용자가 입력한 문장에 대한 컨테이너
    container = st.container()

    with container:  # 대화 내용 저장(기억)
        with st.form(key='Conv_Question', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="PDF파일에 대해 얘기해볼까요? (:", key='input')
            submit_button = st.form_submit_button(label='Send')
        if submit_button and user_input:
            conversational_chat(user_input)

    if st.session_state['history']:
        with response_container:
            for i in range(len(st.session_state['history'])):
                message(st.session_state["history"][i][0], is_user=True, key=str(i) + '_user', avatar_style = "fun-emoji", seed = "Nala")
                message(st.session_state["history"][i][1], key=str(i), avatar_style = "bottts", seed = "Fluffy")