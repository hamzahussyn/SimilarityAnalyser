# SimilarityAnalyser

A web based tool for finding similarity in two peices of Python code.
Its a flask project which makes use of AST, astor, RE, and difflib libraries in Python.

## Disclaimer

I authored this project for the fun of it to learn more about ASTs and CFGs. This project does not gurantee any results derived of comparisons.

**Warning**: This project is intended for <u>educational purposes</u> only. Any unfair use, including but not limited to <u>plagiarism</u> and <u>unauthorized copying</u>, is strictly prohibited and unethical.

Reach me out at [hamzaahussyn@outlook.com](mailto:hamzaahussyn@outlook.com)

## Project Setup

### Virtual Environment (Optional)
Set up a virtual environment in the project directory after cloning it on to your machine.

`python3 -m venv env`

Once you have the virtual environment set up, activate it by changing your directory to:

`cd env/bin`

then execute activate scripte, works differently for linux, mac os, or windows.

### Installing dependencies
Make sure you're at the same directory level as `requirement.txt` file at the root. Then execute:

`pip install -r requirement.txt`

### Running the project
Now to finally run the flask server, execute:

`python3 -m flask --app app run`

