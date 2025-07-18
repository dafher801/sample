import streamlit as st
import smtplib

# Gmail 로그인 정보 (보안을 위해 환경 변수를 사용하는 것이 좋습니다)
EMAIL_ADDRESS = "dafher801@gmail.com"
EMAIL_PASSWORD = "rzpp eono svtr qukt"  # 여기서 your_app_password는 생성된 앱 비밀번호로 바꿔야 합니다

st.title("이메일 전송 예제")

# 수신자 이메일 입력
receiver_email = st.text_input("수신자 이메일 주소를 입력하세요")

# 이메일 전송 함수
def send_email(to_address, subject, body):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(EMAIL_ADDRESS, to_address, message)
        st.success("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        st.error(f"이메일 전송 중 오류가 발생했습니다: {e}")

if receiver_email:
    if st.button('이메일 전송'):
        send_email(receiver_email, "Test Email", "Hello World!")