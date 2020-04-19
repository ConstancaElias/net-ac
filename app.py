#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, redirect
import os
import subprocess
import os.path

app = Flask(__name__)

from actualizar_dicionario import actualizar_dicionario
from leitura_ficheiro_json import leitura_ficheiro_json


'''
def execute(cmd, files):
    subp_ret = ""
    cmd_list = [cmd]
    cmd_list.extend(files)
    try:
        subp_ret = subprocess.check_output(cmd_list)
        """ at this point you have the output of the command in subp_ret in case you need it """
    except Exception as e:
        print("Failed to run subprocess. Details: " + str(e))
    back =dict()
    for file in files:
        with open(file, 'r') as f:
            info = f.read()
            back[file] = info
    return back
'''


@app.route("/home")
@app.route("/")
def home():
	return render_template('home.html')

@app.route('/words', methods=['POST', 'GET'])
def words():
	if request.method == 'POST':
		typeP = request.form['type']
		sociolinguistic = request.form.get('sociolinguistic')
		keyword = request.form['keyword']
		if os.name == "nt":       
		    encondF = "cp1252" 
		else:
		    encondF = "utf8"
		with open("novas_palavras2.txt", "w") as f: 
			f.write("%s*%s*%s" % (typeP, sociolinguistic, keyword))
		f.close()
		print("SUBPROCESS")
		output = actualizar_dicionario('static/dicionario_Ingles.txt')
		
		return redirect(url_for("novapalavra", output = output))
	else:
		return render_template("words.html")

@app.route('/novapalavra')
def novapalavra():
	output = request.args['output']
	return render_template("novapalavra.html", output = output)

@app.route("/Analise_Ficheiros",  methods=['POST', 'GET'])
def Analise_Ficheiros():
	if request.method == 'POST':
		f = request.form['file']
		string = 'static/Ficheiros_Json/' + f
		if os.name == "nt":       
		    encondF = "cp1252" 
		else:
		    encondF = "utf8"
		f ="static/TabelaFreq_" + f+".pdf"
		#no caso de ja existir pdf de um ficheiro, para ser mais rapido vamos so carregar o pdf sem o gerar de novo
		if os.path.isfile(f):
			return redirect(url_for("resultados_analise", file = f))
		else:
			leitura_ficheiro_json('static/dicionario_Ingles.txt', string)
			return redirect(url_for("resultados_analise", file = f))
	else:
		return render_template("Analise_Ficheiros.html")

@app.route('/resultados_analise')

def resultados_analise():
	#output = request.args['output']
	f = request.args['file']
	return render_template("resultados_analise.html", file = f)


'''
@app.route('/dicionario')
def dicionario():
	path = "C:/Users/Constança Elias/Documents/Projeto_LCC/dicionario_Ingles.pdf"
	return send_file(path, as_attachment=True)
'''

if __name__ == "__main__":
	app.run()
