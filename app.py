import openai
from flask import Flask, render_template, request, send_file, session
from flask_socketio import SocketIO, emit
from pprint import pprint
import utils
from md2pdf.core import md2pdf
from gevent.pywsgi import WSGIServer
import logging




app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)



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

    with open('data/input.txt', 'r') as file:
        input_txt = file.read()

    user_input = input_txt.format(
        chapters_number=chapters_number, prompt=prompt)

    # init_output = utils.get_reponse(user_input)
    init_output = "Simple reponse"
    output += init_output
    table_of_contents = utils.extract_table_of_contents(init_output)

    # pprint(table_of_contents)

    for topic_index in range(2):
        curr_topic = table_of_contents[topic_index]

        with open('data/output_continue.txt', 'r') as file:
            output_continue_txt = file.read()

        output_continue = output_continue_txt.format(
            table_of_contents=table_of_contents, curr_topic=curr_topic)
        output += "[simeple output]"
        # output += utils.get_reponse(output_continue)

        socketio.emit('output_update', {'output': output}, namespace='/test')
        socketio.sleep(0)  # Yield control to other events

    # session['output'] = output
    
    with open('data/output.txt', 'w') as file:
        file.write(output)

    return render_template('display.html', output=output)




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


@socketio.on('connect')
def connect():
    logging.info('Client connected with logging')
    print('Client connected')


if __name__ == '__main__':
    print("***** Started application *****")
    socketio.run(app, host='127.0.0.1', debug=True)
