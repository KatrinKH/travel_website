from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ


@app.route('/')
def index():
    return render_template('index.html', title='TravelVista')


@app.route('/countries')
def countries():
    return render_template('countries.html')


@app.route('/spain')
def spain():
    return render_template('spain.html')


@app.route('/japan')
def japan():
    return render_template('japan.html')


@app.route('/uk')
def uk():
    return render_template('uk.html')


@app.route('/southkorea')
def southkorea():
    return render_template('southkorea.html')


@app.route('/turkey')
def turkey():
    return render_template('turkey.html')


@app.route('/china')
def china():
    return render_template('china.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        country = request.form['country']

        pdf_path = f'static/pdf/{country}.pdf'
        if not os.path.exists(pdf_path):
            flash(f'PDF for {country} not found.', 'danger')
            return redirect(url_for('feedback'))

        # Sending email
        send_email(email, country, pdf_path)

        flash(f'The PDF for {country} has been sent to {email}.', 'success')
        return redirect(url_for('index'))
    return render_template('feedback.html')


def send_email(to_email, country, pdf_path):
    from_email = 'vistatrav@yandex.ru'  # Замените на ваш email Яндекса
    from_password = 'kyiaqgsxkcenzyom'  # Замените на ваш пароль Яндекса
    smtp_server = 'smtp.yandex.ru'
    smtp_port = 465  # или 587 для TLS

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f'{country} Travel Guide'

    body = f'Здравствуйте {to_email},\n\nНаправляем Вам информацию по стране {country}.\n\nС наилучшими пожеланиями,\nTravelVista Team'
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_path, 'rb') as pdf_file:
        part = MIMEApplication(pdf_file.read(), Name=f'{country}.pdf')
        part['Content-Disposition'] = f'attachment; filename="{country}.pdf"'
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f'Failed to send email: {e}')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
