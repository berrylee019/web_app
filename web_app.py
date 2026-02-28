import streamlit as st
import os
import io
from google import genai
from google.genai import types
from PIL import Image
import subprocess

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="AI 에러 해결사", layout="wide")
st.title("🚀 1인 기업을 위한 AI 시스템 엔지니어")
st.subheader("에러 스크린샷 한 장으로 해결책부터 도구 설치까지 한 번에!")

# 2. 사이드바: API 키 입력
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("AI Studio에서 발급받은 키를 입력하면 작동합니다.")
    st.markdown("---")
    st.write("v2.5 Flash 엔진 가동 중")

# 3. 메인 화면: 파일 업로드
uploaded_file = st.file_uploader("에러 스크린샷(PNG, JPG)을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 에러 화면', use_container_width=True)
    
    # 분석 실행 버튼
    if st.button("🔍 AI 분석 및 해결책 생성"):
        if not api_key:
            st.error("⚠️ 왼쪽 사이드바에 API Key를 먼저 입력해주세요!")
        else:
            try:
                # 제미나이 클라이언트 생성
                client = genai.Client(api_key=api_key)
                
                # 이미지를 바이너리 데이터로 변환
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()

                image_part = types.Part.from_bytes(
                    data=img_bytes,
                    mime_type="image/png"
                )

                with st.spinner('제미나이 2.5가 에러를 정밀 분석 중입니다...'):
                    # AI 요청
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", # 또는 "gemini-2.5-flash" (사용 가능 목록 확인)
                        contents=[
                            "너는 세계 최고의 풀스택 개발자야. 첨부된 에러 스크린샷을 보고 "
                            "1. 원인을 한 줄로 요약하고, 2. 해결 방법을 단계별로 설명하고, "
                            "3. 필요한 수정 코드나 터미널 명령어를 마크다운 형식으로 작성해줘.",
                            image_part
                        ]
                    )
                
                # --- [결과 출력 섹션] ---
                st.success("✅ 분석이 완료되었습니다!")
                st.markdown("---")
                st.markdown(response.text) # 제미나이의 상세 분석 내용 출력
                
                # --- [에이전트 기능 섹션: 리포트 다운로드 & 자동 설치] ---
                st.divider()
                st.subheader("🛠️ AI 에이전트 실행 메뉴")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # 필살기 1: 분석 리포트 다운로드 버튼
                    st.download_button(
                        label="📄 분석 리포트 저장 (MD 파일)",
                        data=response.text,
                        file_name="gemini_error_report.md",
                        mime="text/markdown"
                    )
                    st.caption("제미나이의 분석 내용을 문서로 저장합니다.")

                with col2:
                    # 필살기 2: 도구 자동 설치 버튼 (예시로 google-genai 설치)
                    if st.button("🔧 제안된 도구 자동 설치 (Test)"):
                        with st.spinner("터미널 명령어를 실행 중입니다..."):
                            # 윈도우 환경 대응을 위해 shell=True 사용
                            result = subprocess.run(["pip", "install", "google-genai"], capture_output=True, text=True, shell=True)
                            if result.returncode == 0:
                                st.code(result.stdout)
                                st.success("✅ 도구 설치가 성공적으로 완료되었습니다!")
                            else:
                                st.error("❌ 설치 중 에러가 발생했습니다.")
                                st.code(result.stderr)
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
                st.write("모델 이름이나 API 키를 다시 확인해 보세요.")

else:

    st.info("☝️ 위 상자에 에러 스크린샷 파일을 끌어다 놓으세요.")
