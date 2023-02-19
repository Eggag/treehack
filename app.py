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
    return """Rate the similarity of the two given problems on a scale from 1 to 10, where 1 means they are not similar at all, and 10 means they are very similar. Explain why. For that number to be high, the problems must have very similar solutions and require you to find almost identical things, ignoring specific details like names. Being in the same broad category does not mean the problems are similar.\n

Problem 1:\n
Artsem is on vacation and wants to buy souvenirs for his two teammates. There are n souvenir shops along the street. In i-th shop Artsem can buy one souvenir for ai dollars, and he cannot buy more than one souvenir in one shop. He doesn't want to introduce envy in his team, so he wants to buy two souvenirs with least possible difference in price.\n

Artsem has visited the shopping street m times. For some strange reason on the i-th day only shops with numbers from li to ri were operating (weird? yes it is, but have you ever tried to come up with a reasonable legend for a range query problem?). For each visit, Artsem wants to know the minimum possible difference in prices of two different souvenirs he can buy in the opened shops.\n

In other words, for each Artsem's visit you should find the minimum possible value of |as-at| where li≤s,t≤ri, s≠t.\n

Problem 2:\n
Kostya and Zhenya — the creators of the band "Paper" — after the release of the legendary album decided to create a new band "Day movers", for this they need to find two new people.\n

They invited 𝑛\n
 people to the casting. The casting will last 𝑞\n
 days. On the 𝑖\n
th of the days, Kostya and Zhenya want to find two people on the segment from 𝑙𝑖\n
 to 𝑟𝑖\n
 who are most suitable for their band. Since "Day movers" are doing a modern art, musical skills are not important to them and they look only at other signs: they want the height difference between two people to be as small as possible.\n

Help them, and for each day, find the minimum difference in the growth of people from the casting on this segment!"""