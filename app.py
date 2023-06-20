import logging
import os

import openai
from flask import Flask, render_template, request, send_file, session
from flask_socketio import SocketIO, emit, ConnectionRefusedError
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from md2pdf.core import md2pdf
from pprint import pprint
import utils





app = Flask(__name__, template_folder='frontend/templates')
own_pid = os.getpid() 
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)



@app.route('/kill')
def kill_backend():
    global own_pid
    os.kill(own_pid, 9) 


@app.route('/')
def index():
    return render_template('index.html')



@socketio.on('connect')
def handle_connect():
    print('A client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('A client disconnected')

@app.route('/', methods=['POST'])
def data_processing():
    prompt = request.form['prompt']
    chapters_number = int(request.form['chapters_number'])
    api_key = str(request.form['api_key'])
    openai.api_key = api_key
    output = ""

    with open('data/input_prompt.txt', 'r') as input_file:
        input_text = input_file.read()

    user_input = input_text.format(chapters_number=chapters_number, prompt=prompt)

    initial_output = utils.get_response(user_input)
    output += initial_output

    table_of_contents = utils.extract_table_of_contents(initial_output)

    for topic_index in range(2):
        current_topic = table_of_contents[topic_index]
        output_continue = get_formatted_output_continue(table_of_contents, current_topic)
        output += utils.get_response(output_continue)


    save_output(output)

    return render_template('display.html', output=output)


def get_formatted_output_continue(table_of_contents, current_topic):
    with open('data/output_continue_prompt.txt', 'r') as output_continue_file:
        output_continue_text = output_continue_file.read()

    return output_continue_text.format(table_of_contents=table_of_contents, current_topic=current_topic)


def save_output(output):
    session['output'] = output

    with open('data/output.txt', 'w') as output_file:
        output_file.write(output)


@app.route('/download', methods=['GET'])
def download():

    file_path_txt = 'data/output.txt'
    file_path_pdf = 'output.pdf'
    file_path_md = 'output.md'

    try:
        with open(file_path_txt, 'r') as file:
            output = file.read()

        with open(file_path_md, 'w') as f:
            f.write(output)

        md2pdf(file_path_pdf,
               md_content=output,
               )

    except Exception as e:
        print(f"Error during conversion: {str(e)}")

    return send_file(file_path_pdf, as_attachment=True)





if __name__ == '__main__':
    print("***** Started application *****")
    host = '127.0.0.1'
    port = 5000
    print(f"Server running at http://{host}:{port}")
    socketio.run(app, host=host, port=port)
