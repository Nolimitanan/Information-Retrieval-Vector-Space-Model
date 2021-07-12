from flask import Flask, render_template, request
import os
from random import *
from math import *

app = Flask(__name__)
ch = "ABCDEF"


@app.route('/')
def documents():
    return '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Home</title>
            <link rel="stylesheet" media="screen" href="static/bootstrap.min.css">
            <style>
                     h2{
                         text-align: center;
                     }
                    a{
                        max-width: max-content;
                        margin: auto;
                    }
                    form{
                        max-width: max-content;
                        margin: auto;
                    }
                    h1{
                         text-align: center;
                     }
                    
                </style>
        </head>
        <body  style="background: linear-gradient(to bottom, #4da6ff 11%, #ffff 100%);object-fit: cover;background-repeat: no-repeat;">
            <h1>Click to generate 10 Document file</h1>
            <form action = "http://127.0.0.1:5000/Created">
                <br>
                <input type="submit" value="generate">
                <br>
            </form>
            <br>
            <h2><a href="http://127.0.0.1:5000/Vector_Space_Model">Vector Space Model</a></h2>
        </body>
    </html>
    '''


@app.route('/Created')
def creat():
    creat_files()
    return '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>generated</title>
                <link rel="stylesheet" media="screen" href="static/bootstrap.min.css">
                <style>
                     h2{
                         text-align: center;
                     }
                    p{
                        max-width: max-content;
                        margin: auto;
                    }
                    h1{
                        max-width: max-content;
                        margin: auto;
                    }
                </style>
            </head>
            <body  style="background: linear-gradient(to bottom, #4da6ff 11%, #ffff 100%);object-fit: cover;background-repeat: no-repeat;">
                <h1>The generation was successful</h1>
                <br>
                <h2><a href="http://127.0.0.1:5000/Vector_Space_Model">Vector Space Model</a></h2>
                <h2><a href="http://127.0.0.1:5000">Home</a></h2>
            </body>
        </html>
        '''


@app.route('/Vector_Space_Model')
def vector_space():
    return render_template('Vector Space Model.html')


@app.route('/Vector Space Model Result', methods=["POST"])
def vector_result():
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    string = request.form['query']
    matrix = count()
    query = Query(string)
    idf_array = idf()
    maximum = max(query.values())
    for char in ch:
        query[char] = (query[char]/maximum)*idf_array[char]
    weight(matrix, idf_array)
    sim(matrix, query)
    matrix = sorted(matrix, reverse=True, key=lambda doc: matrix[doc]["score"])
    return render_template('Result.html', matrix=matrix, num=len(text_files))


def creat_files():
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for file in text_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    for i in range(10):
        f = open(f"D{i + 1}.txt", "w")
        txt = ""
        for j in range(randint(5, 15)):
            txt += choice(ch) + " "
        f.write(txt[:len(txt) - 1])


def files(directory):
    files_in_directory = os.listdir(directory)
    text_files = [file for file in files_in_directory if file.endswith(".txt")]
    return text_files


def count():
    matrix = {}
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for i in range(len(text_files)):
        file_name = f"D{i + 1}"
        counter = {}
        file = open(f"{file_name}.txt", "r")
        text = file.read()
        for char in ch:
            counter[char] = text.count(char)
        matrix[file_name] = counter
        file.close()
    return matrix


def Query(string):
    query = {}
    for char in ch:
        if char in string:
            query[char] = string.count(char)
        else:
            query[char] = 0
    return query


def idf():
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    idf_array = {}
    for char in ch:
        counter = 0
        for i in range(len(text_files)):
            file = open(f"D{i+1}.txt", "r")
            text = file.read()
            file.close()
            if char in text:
                counter += 1
        idf_array[char] = log(len(text_files)/counter, 2)
    return idf_array


def weight(matrix, idf_array):
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for i in range(len(text_files)):
        maximum = max(matrix[f"D{i+1}"].values())
        for char in ch:
            matrix[f"D{i+1}"][char] = (matrix[f"D{i+1}"][char]/maximum)*idf_array[char]


def sim(matrix, query):
    directory = os.path.dirname(os.path.abspath("app.py"))
    text_files = files(directory)
    for i in range(len(text_files)):
        inner = 0
        matrix_sum = 0
        query_sum = 0
        for char in ch:
            inner += matrix[f"D{i + 1}"][char] * query[char]
            matrix_sum += pow(matrix[f"D{i + 1}"][char], 2)
            query_sum += pow(query[char], 2)

        matrix[f"D{i + 1}"]["score"] = inner/sqrt(matrix_sum*query_sum)


if __name__ == '__main__':
    app.run()
