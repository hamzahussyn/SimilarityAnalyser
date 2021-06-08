from flask import Flask, render_template, request
from SimilarityAnalyzer import analyseSimilarity
import json

app = Flask(__name__)

codeOne = ''
codeTwo = ''

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fileOne", methods=['POST'])
def submitFileOne():
   global codeOne
   codeOne = request.get_data().decode("utf-8") 
   return "Success"

@app.route("/api/fileTwo", methods=['POST'])
def submitFileTwo():
   global codeTwo
   codeTwo = request.get_data().decode("utf-8") 
   return "Success"

@app.route("/api/astOne")
def resultsOfASTOne():
   global codeOne
   global codeTwo
   jsonObject = analyseSimilarity(codeOne, codeTwo) 
   return json.loads(jsonObject)

@app.route("/api/astTwo")
def resultsOfASTTwo():
   global codeOne
   global codeTwo
   jsonObject = analyseSimilarity(codeTwo, codeOne) 
   return json.loads(jsonObject)