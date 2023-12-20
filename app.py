from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
# Function to get the next option from a file
def get_next_option(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    story = lines[0].strip()
    options = []
    for line in lines[1:]:
        if line.strip():
            option_text, option_file = line.split('|')
            options.append({'text': option_text.strip(), 'file': option_file.strip()})
    return story, options

# Specify the paths to your text files
background_image = "static/background.png"  # Update with your image file path

current_option = {
    'file': "static/extra/start.txt",
}

@app.route('/')
def index():
    story, options = get_next_option(current_option['file'])
    return render_template('index.html', story=story, options=options, background_image=background_image)

@app.route('/button_clicked', methods=['POST'])
def button_clicked():
    selected_button = request.form['button']
    print(selected_button)

    story, options = get_next_option(current_option['file'])
    
    if selected_button == 'button_1':
        current_option['file'] = 'static/extra/'+options[0]['file']
        file_text = read_text_from_file(current_option['file'])
        # print(f"current_option['file']: {current_option['file']}")
        story, options = get_next_option(current_option['file'])
    else:
        current_option['file'] = 'static/extra/'+options[1]['file']
        # print(f"current_option['file']: {current_option['file']}")
        file_text = read_text_from_file(current_option['file'])
        story, options = get_next_option(current_option['file'])

    if options !=[]:
        # In this alternative, there are options
        # print(f'1. story {story}')
        return render_template('index.html', story=story, options=options, background_image=background_image, current_option = current_option)
    else:
        # in this alternative, there are no options
        # print(f'2. story {story}')
        return render_template('index.html', story=story, background_image=background_image, current_option = current_option)

@app.route('/quit_story')
def quit_story():
    return render_template('goodbye.html')  # Create a 'goodbye.html' template for the goodbye page

# Reset the story route
@app.route('/reset_story')
def reset_story():
    current_option['file'] = "static/extra/start.txt"  # Reset to the initial story file
    story, options = get_next_option(current_option['file'])
    return render_template('index.html', story=story, options=options, background_image=background_image, current_option=current_option)

if __name__ == '__main__':
    app.run(debug=True)

