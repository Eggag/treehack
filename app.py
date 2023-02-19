import os

import openai
from flask import Flask, redirect, render_template, request, url_for

import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

#parse json stuff
with open('./stuff.json', 'r') as f:
    response = f.read()
    response = response.replace('\n', '')
    response = response.replace('}{', '},{')
    response = "[" + response + "]"
    data = json.loads(response) 

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # get stuff from html form
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


        for problem in p:


        #apparently low temp means it is more focused on prompt
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(),
            temperature=0.8,
            max_tokens = 500,
        )
        print(response.choices[0].text)
        print(response)
        ans = "" # ans is the string with the problems we output
        return redirect(url_for("index", result=ans))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt():

