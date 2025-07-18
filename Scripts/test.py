import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from email import policy
from io import BytesIO
import fitz
import re
import os

EMAIL_ADDRESS = "dafher801@gmail.com"
EMAIL_PASSWORD = "rzpp eono svtr qukt"

st.title("PDF 파일 업로드 및 이메일 전송 예제")

receiver_email = "dafher801@gmail.com"
email_body = st.text_area("이메일 본문을 입력하세요")

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

uploaded_files = st.file_uploader("여러 PDF 파일을 업로드하세요", type="pdf", accept_multiple_files=True)

def send_email(to_address, subject, body, attachments):
    try:
        msg = MIMEMultipart(policy=policy.default)
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        for attachment in attachments:
            part = MIMEApplication(attachment['data'].getvalue(), Name=os.path.basename(attachment['filename']))
            part.add_header(
                'Content-Disposition', 
                f'attachment; filename="{os.path.basename(attachment["filename"])}"'
            )
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        st.success("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        st.error(f"이메일 전송 중 오류가 발생했습니다: {e}")

if receiver_email and uploaded_files:
    if not is_valid_email(receiver_email):
        st.error("유효한 이메일 주소를 입력하세요.")
    else:
        if st.button('이메일 전송'):
            attachments = []
            for uploaded_file in uploaded_files:
                # PDF 파일을 메모리에 읽어 들입니다.
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_document:
                    uploaded_file.seek(0)
                    attachments.append({'filename': uploaded_file.name, 'data': BytesIO(uploaded_file.read())})

            send_email(receiver_email, "PDF 파일 전송", email_body, attachments)
