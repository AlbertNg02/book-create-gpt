import aspose.words as aw
import openai
from flask import Flask, render_template, request, send_file, session
from flask_socketio import SocketIO, emit
from pprint import pprint
import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

openai.api_key = ''


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
    intput = f"As a world-renowned writer with seven years of experience and numerous published books, you have been tasked with writing an outline of a book consisting of {chapters_number} chapters, each chapter containing 2-3 sub-chapters. Give me only the table of content first, do not give a description of the outline. The output will be in PYTHON list FORMAT with NO nested list. The book prompt is: {prompt}. Also, have a conclusion at the end of the table of contents; no need for starting greetings, acknowledgments, or references. The chapter and sub-chapter names should be explicit."

    # Make the first request to retrieve the table of contents and introduction
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a book writer"},
            {"role": "user", "content": intput}
        ]
    )
    init_output = completion["choices"][0]["message"]["content"]
    output += init_output
    table_of_contents = utils.extract_table_of_contents(init_output)
    print("-----------Table of contents start-------")
    pprint(table_of_contents)

    # Loop over to get the specific table of contents pages
    # for topic_index in range(len(table_of_contents)):
    for topic_index in range(3):
        curr_topic = table_of_contents[topic_index]
        output_continue = f"We have a table of content which is {table_of_contents}, now we have to expand upon each subtopic. The current subtopic that needs to be extended is {curr_topic}. Start the response with the {curr_topic} as the headline by itself on a new line. The whole output must be RAW MARKDOWN and have the {curr_topic} as an appropriate heading. Avoid using headings for anything else apart from the main topic "
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a book writer"},
                {"role": "user", "content": output_continue}
            ]
        )
        output += completion["choices"][0]["message"]["content"]

        # Emit the updated output via web socket
        socketio.emit('output_update', {'output': output}, namespace='/test')
        socketio.sleep(0)  # Yield control to other events

    session['output'] = output

    return render_template('display.html', output=output)


@app.route('/download', methods=['GET'])
def download():
    # Retrieve the 'output' variable from session
    output = session.get('output')
    if output is None:
        return 'No output available for download.'

    file_path_md = 'output.md'
    file_path_pdf = 'output.pdf'

    with open(file_path_md, 'w') as file:
        file.write(output)

    # Convert Markdown to PDF using Aspose.Words
    doc = aw.Document(file_path_md)
    doc.save(file_path_pdf)

    return send_file(file_path_pdf, as_attachment=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
