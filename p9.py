import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import base64

# ✅ .env 파일 로드
load_dotenv()

# ✅ OpenAI 연결 함수
def getOpenAI():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)

# 페이지 제목 및 설명
st.sidebar.markdown("👩‍🍳 음식 변환 페이지")
st.title("🍽️ 외국 음식 → 한국식 레시피 변환")

# ✅ 이미지 업로더
uploaded_img = st.file_uploader("외국 음식 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_img is not None:
    # 업로드된 이미지 표시
    image = Image.open(uploaded_img)
    st.image(image, caption="업로드된 음식 사진", use_container_width=True)

    # 이미지 base64 인코딩 (OpenAI Vision 모델 입력용)
    img_bytes = uploaded_img.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # 프롬프트 정의
    prompt = """
    1. 업로드된 사진 속 음식이 무엇인지 알려주세요.
    2. 그 음식이 어떤 외국 음식인지 간단히 설명해주세요.
    3. 그 음식을 한국식으로 바꾼 레시피를 제안해주세요.
       - 한국에서 쉽게 구할 수 있는 재료 사용
       - 조리법은 간단명료하게
       - 원래 음식의 특징을 유지하면서 한국적인 맛을 살리기
    """

    # OpenAI 모델 호출
    client = getOpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # 이미지 + 텍스트 지원 모델
        messages=[
            {"role": "system", "content": "당신은 외국 음식을 한국식으로 재해석하는 요리사입니다."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
            ]}
        ],
        max_tokens=700
    )

    # 결과 출력
    result = response.choices[0].message.content
    st.subheader("📖 변환 결과")
    st.write(result)
