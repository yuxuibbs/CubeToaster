import os
import requests
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import Required, Length, Regexp
from werkzeug.utils import secure_filename
import heatGenerator
import sheetGenerator


app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'random insecure key'


class RegistrationDataInputForm(FlaskForm):
    file = FileField()


class HeatInputForm(FlaskForm):
    file = FileField()

@app.route('/', methods=['GET', 'POST'])
def home():
    registrationForm = RegistrationDataInputForm()
    heatForm = HeatInputForm()
    if request.method == "POST":
        if request.form["form"] == "registration":
            entered_filename = request.files['file'].filename
            if len(entered_filename.split('.')) > 1 and (entered_filename.split('.')[1] == "json" or entered_filename.split('.')[1] == "csv"):
                text = request.files['file'].read()
                text_to_translate = text.decode()
            else:
                flash("File must be the csv file from WCA registration or the json file from CubingUSA registration")
        if request.form["form"] == "heats":
            entered_filename = request.files['file'].filename
            if len(entered_filename.split('.')) > 1 and entered_filename.split('.')[1] == "csv":
                text = request.files['file'].read()
                text_to_translate = text.decode()
            else:
                flash("File must be a csv file (safest way is to use the csv file that you got from above and changing the numbers but you can also just fill out the sample csv file)")
    return render_template("index.html", registration=registrationForm, heat=heatForm)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(os.getenv('PORT', 5000)))
