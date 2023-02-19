import os

import openai
from flask import Flask, redirect, render_template, request, url_for

import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
with open('./stuff.json', 'r') as f:
    response = f.read()
    response = response.replace('\n', '')
    response = response.replace('}{', '},{')
    response = "[" + response + "]"
    data = json.loads(response) 
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        statement = request.form["statement"]
        editorial = request.form["editorial"]
        tags = request.form["tags"]
        difficulty = int(request.form["difficulty"])
        p = []
        for problem in data:
            if(problem["difficulty"] == ""):
                continue
            if(problem["difficulty"] >= difficulty - 300 and problem["difficulty"] <= difficulty + 300):
                f = 1
                for t in problem["tags"]:
                    if(tags.find(t) == -1):
                        f = 0
                        break
                if(f != 1):
                    continue
                p.append(problem)

        
        #apparently low temp means it is more focused on prompt
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
