from model import InputForm
from compute import show
from flask import Flask, render_template, request
import ast

app = Flask(__name__)


@app.route('/Titration-Simulator/<string:page_name>/')
def help(page_name):
    return render_template('help.html', page=page_name)


@app.route('/Titration-Simulator', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    print(form)
    print((type(form)))
    if request.method == 'POST' and form.validate():
        v_Ac = form.v_Ac.data
        v_B = form.v_B.data
        v_sample = form.v_sample.data
        Kb = form.pKs_B.data
        Ka = form.pKs_Ac.data
        Kt = form.pKs_Tit.data
        erase = form.erase.data

        # collect pKs Base
        if Kb.startswith('[') is False:
            pKs_B = []
        elif Kb.count('],[') == 0 and len(ast.literal_eval(Kb)) == 1:
            pKs_B = [[i] for i in ast.literal_eval(Kb)]
        elif Kb.count('],[') == 0 and len(ast.literal_eval(Kb)) > 1:
            pKs_B = [[i for i in ast.literal_eval(Kb)]]
        else:
            pKs_B = [i for i in ast.literal_eval(Kb)]

        # collect pKs Acid
        if Ka.startswith('[') is False:
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
        # collect v(Ac)
        if len(str(form.v_Ac.data).strip()) == 0:
            v_Ac = [0]
        else:
            v_Ac = [float(i) for i in form.v_Ac.data.split(',')]

        # collect c(Ba)
        if len(str(form.c_B.data).strip()) == 0:
            c_B = [0]
        else:
            c_B = [float(i) for i in form.c_B.data.split(',')]
        # collect v(Ba)
        if len(str(form.v_B.data).strip()) == 0:
            v_B = [0]
        else:
            v_B = [float(i) for i in form.v_B.data.split(',')]

        # collect c(Tit)
        if len(str(form.c_Tit.data).strip()) == 0:
            c_Tit = [0]
        else:
            c_Tit = [float(i) for i in form.c_Tit.data.split(',')]

        # collect pKs(Tit)
        if Kt.startswith('[') is False:
            pKs_Ac = [[7]]
            Err_msg = "Error! No Titration agent was selected."
            return Err_msg
        elif Kt.count('],[') == 0 and len(ast.literal_eval(Kb)) == 1:
            pKs_Tit = [[i] for i in ast.literal_eval(Kt)]
        elif Kt.count('],[') == 0 and len(ast.literal_eval(Kb)) > 1:
            pKs_Tit = [[i for i in ast.literal_eval(Kt)]]
        else:
            pKs_Tit = [i for i in ast.literal_eval(Kt)]

        # collect v_sample
        if len(str(form.v_sample.data).strip()) == 0:
            v_sample = [0]
        else:
            v_sample = [float(i) for i in form.v_sample.data.split(',')]
        # collect v_tit
        if len(str(form.v_Tit.data).strip()) == 0:
            v_Tit = [0]
        else:
            v_Tit = [float(i) for i in form.v_Tit.data.split(',')]

        result = show(v_Ac,
                c_Ac,
                pKs_Ac,
                v_B,
                c_B,
                pKs_B,
                v_sample,
                c_Tit,
                v_Tit,
                pKs_Tit,
                erase
                )

    else:
        result = None

    return render_template('view.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
