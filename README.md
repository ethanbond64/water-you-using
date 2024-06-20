# Water You Using
Water You Using is a web app that meets the UN's challenge to Conserve Water through AI. It is aimed at helping consumers learn about and track their water consumption through everyday products, which helps them make more informed decisions. We believe that with the right information, we can positively affect consumer behavior to lead to more sustainable water consumption across multiple industries.

## Installation
To install this application you must have python 3 already installed on your computer. Enter the root directory of the project in a terminal.

### Create a virtual environment
`python3 -m venv venv`

### Activate your environment
`source venv/bin/activate`

### Install requirements
`pip install -r requirements.txt`

### Create an environment file
Create a file named `.env` in the root directory of the project and add the following variables to it:
- OPENAI_API_KEY=<your openai api key> (get a key at openai.com)


## Running the application
`python3 app.py`

You should be able to see your app running by going to http://127.0.0.1:5000/ in your browser.