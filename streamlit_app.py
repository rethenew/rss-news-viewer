import streamlit as st
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 📌 환경 변수 로드
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 📌 타이틀과 질문 입력창을 상단에 배치
st.title("RE, THE NEW with AI")
question = st.text_input("🤖 리더뉴 AI에게 삼성전자 CSR 기사에 대해 무엇이든 질문해보세요", "")

# 📌 기사 데이터 로딩
try:
    with open("rss_output.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
except:
    articles = []

# 📌 기사 요약을 전체 문맥으로 구성
context = "\n\n".join([
    f"{a.get('title')}\n{a.get('summary')}" for a in articles
])

# 📌 Gemini 모델 설정
model = genai.GenerativeModel("gemini-1.5-pro")

# 📌 질문이 들어오면 응답 처리
if question:
    with st.spinner("리더뉴 AI가 답변 중입니다..."):
        response = model.generate_content([
            "다음 기사들을 참고해서 삼성 CSR 관련 질문에 답해줘:",
            context,
            f"질문: {question}"
        ])
        st.subheader("💬 RE, THE NEW AI의 응답:")
        st.write(response.text)
