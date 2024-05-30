import os
import time
import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=api_key, model="gpt-4")

# Streamlit 앱 시작
st.set_page_config(page_title="오아시스 챗봇", page_icon=":memo:", layout="centered", initial_sidebar_state="collapsed")

# CSS 스타일 정의
st.markdown("""
<style>
.chat-container {
    width: 100%;
    max-width: 480px;
    margin: 0 auto;
    padding: 1rem;
    background-color: #abc1d1;
    border-radius: 1rem;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.chat-message {
    padding: 0.8rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 70%;
}
.chat-message.user {
    background-color: #FEE500;
    color: black;
    border-top-right-radius: 0.3rem;
    justify-content: flex-end;
    margin-left: auto;
}
.chat-message.assistant {
    background-color: white;
    color: black;
    border-top-left-radius: 0.3rem;
    justify-content: flex-start;
    margin-right: auto;
}
.chat-header {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 0.5rem;
}
.chat-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 0.5rem;
}
.chat-title {
    font-size: 1rem;
    font-weight: bold;
}
.chat-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem;
    background-color: white;
    text-align: center;
    font-size: 0.8rem;
    color: #999;
}
</style>
""", unsafe_allow_html=True)

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅창 컨테이너
chat_container = st.empty()

with chat_container.container():
    # 채팅 헤더
    st.markdown('<div class="chat-header"><img src="https://i.imgur.com/YMdJE5g.png" alt="오아시스 챗봇 아이콘" class="chat-icon"/><span class="chat-title">오아시스 챗봇</span></div>', unsafe_allow_html=True)
    
    # 채팅 기록 표시
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f'<div class="chat-message assistant">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)

    # 초기 대화 메시지
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": "안녕하세요! 당신의 이름이 무엇인가요?"})
        st.markdown('<div class="chat-message assistant">안녕하세요! 당신의 이름이 무엇인가요?</div>', unsafe_allow_html=True)

    # 사용자 입력 받기
    prompt = st.text_input("메시지 입력", key='input', max_chars=None)

    if prompt:
        # 사용자 메시지 표시
        st.markdown(f'<div class="chat-message user">{prompt}</div>', unsafe_allow_html=True)
        
        # 사용자 메시지를 채팅 기록에 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
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
        
        # 1초 기다렸다가 어시스턴트 응답 표시
        time.sleep(1)
        st.markdown(f'<div class="chat-message assistant">{response}</div>', unsafe_allow_html=True)
        
        # 어시스턴트 응답을 채팅 기록에 추가
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 채팅창 하단 고정
    st.markdown('<div class="chat-footer">오아시스 일기 작성 챗봇</div>', unsafe_allow_html=True)