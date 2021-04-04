import os
from datetime import datetime
from pathlib import Path
from pydantic import EmailStr


def send_dummy_mail(subject: str, message: str, to: EmailStr):
    current_path = os.getcwd()
    filename = f'{datetime.now().timestamp()} - {subject}.txt'
    email_text = f'''Subject: {subject}
From: no-reply@email.com
To: {to}

{message}
'''
    email_path = Path(os.path.join(current_path, 'emails'))
    emails_file = os.path.join(current_path, 'emails', filename)
    try:
        with open(emails_file, 'w') as file_obj:
            file_obj.write(email_text)
    except FileNotFoundError:
        email_path.mkdir()
        with open(emails_file, 'w') as file_obj:
            file_obj.write(email_text)

    return 'email sent!'