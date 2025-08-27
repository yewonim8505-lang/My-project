import streamlit as st
from langchain_core.prompts import PromptTemplate

from MyLCH import getOpenAI

st.markdown("Page5 이메일 작성기")
st.sidebar.markdown("Clicked Page5")

input_text = st.text_area(label="메일 입력", label_visibility='collapsed',
                          placeholder="당신의 메일은...", key="input_text")

query_template = """
    메일을 작성해주세요.    
    아래는 이메일입니다:
    이메일: {email}
"""

prompt = PromptTemplate(
    input_variables=["email"],
    template=query_template,
)

st.button("*예제를 보여주세요*", type='secondary', help="봇이 작성한 메일을 확인해보세요.")
st.markdown("### 봇이 작성한 메일은:")

if input_text:
    llm = getOpenAI()
    # PromptTemplate 및 언어 모델을 사용하여 이메일 형식을 지정
    prompt_with_email = prompt.format(email=input_text)
    formatted_email = llm.predict(prompt_with_email)
    # 서식이 지정된 이메일 표시
    st.write(formatted_email)
