import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

from MyLCH import process_text, getOpenAI

st.markdown("Page2 PDF 요약")
st.sidebar.markdown("Clicked Page2")

pdf = st.file_uploader('PDF파일을 업로드해주세요', type='pdf')

if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""  # 텍스트 변수에 PDF 내용을 저장
    for page in pdf_reader.pages:
        text += page.extract_text()

    documents = process_text(text)
    query = "업로드된 PDF 파일의 내용을 약 3~5문장으로 요약해주세요."  # LLM에 PDF파일 요약 요청

    if query:
        docs = documents.similarity_search(query)
        llm = getOpenAI()
        chain = load_qa_chain(llm, chain_type='stuff')

        with get_openai_callback() as cost:
            response = chain.run(input_documents=docs, question=query)
            print(cost)

        st.subheader('--요약 결과--:')
        st.write(response)