from flask import Flask, render_template, request
from urllib.parse import quote_plus

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    birthdate = request.form['birthdate']  # формат: YYYY-MM-DD
    birthtime = request.form['birthtime']  # формат: HH:MM
    birthcity = request.form['birthcity']

    # Формируем ссылку с данными пользователя
    encoded_city = quote_plus(birthcity)
    encoded_date = quote_plus(birthdate)
    encoded_time = quote_plus(birthtime)

    external_link = f"https://freehumandesignchart.com/?date={encoded_date}&time={encoded_time}&city={encoded_city}"

    return render_template("result.html", name=name, birthdate=birthdate, birthtime=birthtime, birthcity=birthcity, link=external_link)

if __name__ == "__main__":
    app.run()
