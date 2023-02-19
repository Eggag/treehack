import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        statement = request.form["statement"]
        editorial = request.form["editorial"]
        tags = request.form["tags"]
        # apparently low temp means it is more focused on prompt
        #response = openai.Completion.create(
        #    model="text-davinci-003",
        #    prompt=generate_prompt(statement),
        #    temperature=0.6,
        #)

        ans = "" # ans is the string with the problems we output
        return redirect(url_for("index", result=ans))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(x):
    return """random prompt""".format(x)
