import requests
from pprint import pprint
from flask import Flask, render_template, request, redirect
import openai
import utils

app = Flask(__name__)


@app.route('/', methods=['GET'])
def data_request():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def data_processing():
    prompt = request.form['prompt']
    chapters_number = int(request.form['chapters_number'])
    api_key = str(request.form['api_key'])
    openai.api_key = api_key
    output = ""
    intput = f"As a world-renowned writer with seven years of experience and numerous published books, you have been tasked with writing an outline of book consisting of {chapters_number} chapters, each chapter containing 2-3 sub-chapters. Give me only table of content first, do not give a description of the table of outline. The output will be in a PYTHON list FORMAT with NO nested list. The book prompt is {prompt}. Also have a conclusion at the end of the table of contents, no need for starting greetings, no need for acknowledgemnts or references. The chapter and sub-chapter names should be explicit"

    # Make first request to retrieve table of contents and introduction
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a book writer"},
            {"role": "user", "content": intput}
        ]
    )
    init_output = completion["choices"][0]["message"]["content"]
    pprint(init_output)
    print(type(init_output))
    print("_____________init_output end _________________")
    output += init_output
    table_of_contents = utils.extract_table_of_contents(init_output)
    print("-----------Table of contents start-------")
    pprint(table_of_contents)

    # Loop over to get the specific table of contents pages
    for topic_index in range(len(table_of_contents)):
        # for topic_index in range(2):

        curr_topic = table_of_contents[topic_index]
        output_continue = f"We have a table of content which is{table_of_contents}, now we have to expand upon each subtopic, the current subtopic that needs to be extended is{curr_topic}. Start the reponse with the {curr_topic} as the headline by itself in a new line . The whole output must be RAW MARKDOWN"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a book writer"},
                {"role": "user", "content": output_continue}
            ]
        )
        # return render_template('display.html', output=output)
        output += completion["choices"][0]["message"]["content"]

    return render_template('display.html', output=output)


if __name__ == '__main__':
    app.run()
