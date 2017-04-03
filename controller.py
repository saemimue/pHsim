from model import InputForm
from compute import titrate, pH
from flask import Flask, render_template, request
import ast

app = Flask(__name__)

@app.route('/Titration-Simulator', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        Kb = form.pKs_B.data
        Ka = form.pKs_Ac.data
        Kt = form.pKs_Tit.data
        erase = form.erase.data

        # collect pKs Base
        if Kb.startswith('[') == False:
            pKs_B = []
        elif Kb.count('],[') == 0 and len(ast.literal_eval(Kb)) == 1:
            pKs_B = [[i] for i in ast.literal_eval(Kb)]
        elif Kb.count('],[') == 0 and len(ast.literal_eval(Kb)) > 1:
            pKs_B = [[i for i in ast.literal_eval(Kb)]]
        else:
            pKs_B = [i for i in ast.literal_eval(Kb)]

        # collect pKs Acid
        if Ka.startswith('[') == False:
            pKs_Ac = []
        elif Ka.count('],[') == 0 and len(ast.literal_eval(Ka)) == 1:
            pKs_Ac = [[i] for i in ast.literal_eval(Ka)]
        elif Ka.count('],[') == 0 and len(ast.literal_eval(Ka)) > 1:
            pKs_Ac = [[i for i in ast.literal_eval(Ka)]]
        else:
            pKs_Ac = [i for i in ast.literal_eval(Ka)]

        # collect c(Ac)
        if len(str(form.c_Ac.data).strip()) == 0:
            c_Ac = [0]
        else:
            c_Ac = [float(i) for i in form.c_Ac.data.split(',')]

        # collect c(Ba)
        if len(str(form.c_B.data).strip()) == 0:
            c_B = [0]
        else:
            c_B = [float(i) for i in form.c_B.data.split(',')]

        # collect pKs(Tit)
        if Kt.startswith('[') == False:
            pKs_Ac = [[7]]
            Err_msg = "Error! No Titration agent was selected."
            return Err_msg
        elif Kt.count('],[') == 0 and len(ast.literal_eval(Kb)) == 1:
            pKs_Tit = [[i] for i in ast.literal_eval(Kt)]
        elif Kt.count('],[') == 0 and len(ast.literal_eval(Kb)) > 1:
            pKs_Tit = [[i for i in ast.literal_eval(Kt)]]
        else:
            pKs_Tit = [i for i in ast.literal_eval(Kt)]

        result = titrate(c_Ac,c_B,pKs_Ac,pKs_B,pKs_Tit,erase)

    else:
        result = None

    return render_template('view.html',form=form,result=result)

if __name__=='__main__':
    app.run(debug=True)
