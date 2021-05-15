from flask import Flask

#1) Create a New FLask App Instance
app = Flask(__name__) 

#2) Create Flask Routes
@app.route('/')
def hello_world():
    return "Hello world"

#if __main__ == "__name__":
    #app.run()

