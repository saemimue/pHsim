from wtforms import Form, FloatField, validators

class InputForm(Form):
    c_Ac = FloatField(
            label='c(Ac) [mol/L]', default=0.1,
            validators=[validators.InputRequired()])
    c_B = FloatField(
            label='c(B) [mol/L]', default=0,
            validators=[validators.InputRequired()])
    pKs_Ac = FloatField(
            label='pKs(Ac)', default=-2,
            validators=[validators.InputRequired()])
    pKs_B = FloatField(
            label='pKs(B)', default=14,
            validators=[validators.InputRequired()])
    pKs_Tit = FloatField(
            label='pKs(Tit)', default=14,
            validators=[validators.InputRequired()])
