from flask import Flask, render_template,request, redirect, url_for
import requests
import smtplib

app = Flask(__name__)

response = requests.get("https://api.npoint.io/35ae1eacb379fff684fd")
response_data = response.json()


@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=response_data)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in response_data:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data['username']
        email = data['Email']
        phone = data['Phone']
        subject = data['Subject']
        message = data['Message']
        send_email(name, email, phone,subject,message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, subject, message):
    email_message = f"Subject:{subject}\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=OWN_EMAIL, password=OWN_PASSWORD)
        connection.sendmail(from_addr=FROM_EMAIL, to_addrs=TO_EMAIL, msg=email_message)


if __name__ == "__main__":
    app.run(debug=True)
