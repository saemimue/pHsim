from wtforms import Form, StringField, validators

class InputForm(Form):
    c_Ac = StringField(
            label='c(Ac) [mol/L]', default=0.1,
            validators=[validators.InputRequired()])
    c_B = StringField(
            label='c(B) [mol/L]', default=0,
            validators=[validators.InputRequired()])
    pKs_Ac = StringField(
            label='pKs(Ac)', default=-2,
            validators=[validators.InputRequired()])
    pKs_B = StringField(
            label='pKs(B)', default=14,
            validators=[validators.InputRequired()])
    pKs_Tit = StringField(
            label='pKs(Tit)', default=14,
            validators=[validators.InputRequired()])
