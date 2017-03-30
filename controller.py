from model import InputForm
from compute import titrate
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/Titration-Simulator', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        titration = titrate(
                list(form.c_Ac.data),
                list(form.c_B.data),
                list(form.pKs_Ac.data),
                list(form.pKs_B.data),
                list(form.pKs_Tit.data))

    else:
        titration = None

    return render_template('view.html', form=form, titration=titration)

if __name__=='__main__':
    app.run(debug=True)
