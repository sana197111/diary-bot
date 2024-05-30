import os
import time
import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=api_key, model="gpt-4o")

# Streamlit 앱 시작
st.set_page_config(page_title="오아시스 챗봇", page_icon=":memo:", layout="centered", initial_sidebar_state="collapsed")

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 초기 대화 메시지
if not st.session_state.messages:
    initial_message = {"role": "assistant", "content": "안녕하세요! 당신의 이름이 무엇인가요?"}
    st.session_state.messages.append(initial_message)
    with st.chat_message(initial_message["role"]):
        st.markdown(initial_message["content"])

# 사용자 입력 받기
prompt = st.chat_input("메시지를 입력하세요.")

if prompt:
    # 사용자 메시지를 채팅 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 필요한 정보 수집
    if 'name' not in st.session_state:
        st.session_state['name'] = prompt
        response = f"{st.session_state['name']}님, 반가워요! 오늘 하루는 어떠셨나요?"
    elif 'emotion' not in st.session_state:
        st.session_state['emotion'] = prompt
        response = "오늘의 기분이 그러셨군요. 오늘은 어떤 음식을 드셨어요?"
    elif 'food' not in st.session_state:
        st.session_state['food'] = prompt
        response = "정말 맛있었겠어요! 오늘 누구를 만나셨는지, 무엇을 하셨는지 궁금해요."
    elif 'activity' not in st.session_state:
        st.session_state['activity'] = prompt
        response = "오늘 하루가 참 알찼네요. 이제 오늘의 일기를 작성해볼게요!"
        
        # 일기 작성
        diary_prompt = f"이름: {st.session_state['name']}, 감정: {st.session_state['emotion']}, 식사: {st.session_state['food']}, 활동: {st.session_state['activity']}. 이 정보를 바탕으로 일기를 작성해주세요."
        messages = [
            {"role": "system", "content": "Please write a diary entry based on the following details:"},
            {"role": "user", "content": diary_prompt}
        ]
        diary_response = model.invoke(messages)
        diary_entry = diary_response.content
        response += f"\n\n## {st.session_state['name']}님의 오늘 일기:\n{diary_entry}\n\n오늘도 멋진 하루였어요. 내일도 좋은 일 가득하시길 바랍니다!"
    else:
        response = f"{st.session_state['name']}님의 오늘 일기가 완성되었어요. 또 다른 이야기를 들려주실 땐 언제든 찾아주세요!"
    
    # 어시스턴트 응답을 채팅 기록에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 1초 뒤에 어시스턴트 응답 표시
    time.sleep(1)
    with st.chat_message("assistant"):
        st.markdown(response)