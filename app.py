import os

import openai
from flask import Flask, redirect, render_template, request, url_for

import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

statement_comp = "Simplify the following problems by replacing all ideas with a purely mathematical description while being clear and concise in one paragraph. Then rate the similarity of the two given problems on a scale from 1 to 10, and output that rating enclosed in curly braces. Differences in wording, context, and details must be ignored completely – only focus on what the problems require you to find. For the problems to be similar, the specific steps and ideas for getting to the solution must be almost identical for both of them. Being in the same broad category does not mean the problems are similar, the category must be very specific."

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
                f = 0
                for t in problem["tags"]:
                    if(tags.find(t) != -1):
                        f = 1
                        break
                if(f == 0):
                    continue
                p.append(problem)

        ans = "" # ans is output
        cnt = 0
        for prob in p:
            cnt += 1
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(statement_comp, statement, prob["statement"]),
                temperature=0.8,
                max_tokens = 200,
            )
            result = response.choices[0].text
            cur = prob["code"][0] + prob["code"][1] + ", "
            ind = result.find("{")
            if(ind != -1):
                if(result[ind + 1] >= '0' and result[ind + 1] <= '9' and (int(result[ind + 1]) >= 8 or (ind + 2 < len(result) and result[ind + 1] == '1' and result[ind + 2] == '0'))):
                    print(cur)
                    ans += cur

        if(ans == ""):
            ans = "No match found"
        else:
            ans = ans[:-1]
        return redirect(url_for("index", result=ans))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(a, b, c):
    ret = a + "\n\n" + "Problem 1:\n" + b + "\n\n" + "Problem 2:\n" + c
    return ret