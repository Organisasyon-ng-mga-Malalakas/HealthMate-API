import requests

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


from app.core.config import settings


def send_forgot_password_email(email: str, username: str, identifier: str):
    auth = ("api", settings.MAIL_SERVICE_API_KEY)

    data = {
        "from": "Hello from Healthmate! <hello@healthmate.com>",
        "to": email,
        "subject": "Lost Keys? Lets Unlock Your Account 🗝️",
        "html": "<!doctypehtml><html lang=en><meta charset=UTF-8><title>Forgot Password Email</title><style>body{font-family:Arial,sans-serif;line-height:1.6;margin:0;padding:0;background-color:#f5f5f5}.container{max-width:600px;margin:20px auto;padding:20px;background-color:#fff;border-radius:8px;box-shadow:0 0 10px rgba(0,0,0,.1)}.message{margin-bottom:20px}.btn{display:inline-block;padding:10px 20px;background-color:#007bff;color:#fff;text-decoration:none;border-radius:5px}.btn:hover{background-color:#0056b3}.signature{margin-top:20px;text-align:center;font-style:italic;color:#888}</style><div class=container><div class=message><p>Dear "
        + username
        + ",<p>We hope this message finds you well.<p>It seems like you've run into a little hiccup accessing your Health App account. No worries! We're here to help you get back on track swiftly and securely.<p>To reset your password and regain access to your account, simply click on the button below:</p><a class=btn href='"
        + settings.API_URL
        + "/user/forgot-password/"
        + identifier
        + "'>Reset Password</a><p>If you didn't request this password reset, please ignore this email, and your account will remain secure.<p>Wishing you good health and wellness,<p>Healthmate</div></div>",
    }
    response = requests.post(settings.MAIL_SERVICE_URL, auth=auth, data=data)

    return response.status_code == 200


def send_new_password_email(email: str, username: str, new_pass: str):
    auth = ("api", settings.MAIL_SERVICE_API_KEY)

    # fmt: off
    data = {
        "from": "Hello from Healthmate! <hello@healthmate.com>",
        "to": email,
        "subject": "Your Fresh Password for a Healthier Journey 🌟",
        "html": "<!doctypehtml><html lang=en><meta charset=UTF-8><title>Forgot Password Email</title><style>body{font-family:Arial,sans-serif;line-height:1.6;margin:0;padding:0;background-color:#f5f5f5}.container{max-width:600px;margin:20px auto;padding:20px;background-color:#fff;border-radius:8px;box-shadow:0 0 10px rgba(0,0,0,.1)}.message{margin-bottom:20px}</style><div class=container><div class=message><p>Dear "
        + username + ",<p>Revitalize your Health App experience with a brand-new password! 🚀 We're thrilled to assist you in updating your account and ensuring a seamless journey toward wellness.<p>Your new password is: " + new_pass + "<p>We understand that remembering passwords can be a workout in itself, so feel free to update it to something more memorable through your account settings.<p>Remember, your security is our top priority! If you have any concerns or didn't request this password change, please reach out to our team immediately.<p>Wishing you vibrant health and boundless energy as you continue your health journey with us!<p>Warm regards,<p>Healthmate Squad 🍏</div></div>",
    }
    # fmt: on
    response = requests.post(settings.MAIL_SERVICE_URL, auth=auth, data=data)

    return response.status_code == 200
