import openai
import json
import os

openai.api_key = "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"

#parse json stuff
with open('./stuff.json', 'r') as f:
    response = f.read()
    response = response.replace('\n', '')
    response = response.replace('}{', '},{')
    response = "[" + response + "]"
    data = json.loads(response) 


def prompt_simplify(rules, text):
    return """{}:

{}
""".format(rules, text)

def prompt_simplify_statement(statement):
    rules = "Simplify the following problem by replacing all ideas with a purely mathematical description while being clear and concise in one paragraph"
    return prompt_simplify(rules, statement)

def prompt_simplify_editorial(editorial):
    rules = "Simplify the following editorial by replacing all ideas with a purely mathematical description while being clear and concise in one paragraph"
    return prompt_simplify(rules, editorial)

def prompt_deconstruct_statement(statement):
    rules = "Give a very concise bullet list of the distinct givens, properties, operations, and objectives of the following problem while replacing all descriptions with purely mathematical terminology"
    return prompt_simplify(rules, statement)

def prompt_brute(statement):
    rules = "Give a one sentence description of a brute force algorithm to solve to the following problem"
    return prompt_simplify(rules, statement)

def prompt_analyze_simplified(rules, statement, editorial):
    return """{}:

PROBLEM
{}

IDEAS
{}
""".format(rules, statement, editorial)

def prompt_approaches(statement, editorial):
    rules = "Give a bullet list of distinct approach ideas explained in one sentence one might use to solve the following problem using the ideas provided"
    return prompt_analyze_simplified(rules, statement, editorial)

def prompt_insights(statement, editorial):
    rules = "Give a bullet list of possible mathematical insights explained very concisely needed to solve the following problem using the ideas provided"
    return prompt_analyze_simplified(rules, statement, editorial)

def prompt_api(prompttext):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt=prompttext,
        temperature=0.8,
        max_tokens = 500
    )

    responsetext = response.choices[0].text
    return responsetext

def print_simplified(problem, param):
    text = problem["simplified"][param]
    print("""{}
{}
""".format(param.upper(), text))


def main():
    for problem in data:
        if not problem["editorial"]:
            continue

        problem["simplified"] = {}
        problem["simplified"]["statement"] = prompt_api(prompt_simplify_statement(problem["statement"]))
        problem["simplified"]["editorial"] = prompt_api(prompt_simplify_editorial(problem["editorial"]))
        
        problem["simplified"]["deconstruct"] = prompt_api(prompt_deconstruct_statement(problem["simplified"]["statement"]))
        problem["simplified"]["brute"] = prompt_api(prompt_brute(problem["simplified"]["statement"]))

        problem["simplified"]["approaches"] = prompt_api(prompt_approaches(problem["simplified"]["statement"], problem["simplified"]["editorial"]))
        problem["simplified"]["insights"] = prompt_api(prompt_insights(problem["simplified"]["statement"], problem["simplified"]["editorial"]))


        print_simplified(problem, "statement")
        print_simplified(problem, "editorial")
        print_simplified(problem, "deconstruct")
        print_simplified(problem, "brute")
        print_simplified(problem, "approaches")
        print_simplified(problem, "insights")
     
main()
