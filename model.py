from wtforms import Form, StringField, validators

class InputForm(Form):
    c_Ac = StringField(
            label='c(Ac) [mol/L]', default="2e-5, 3e-5, 1e-5",
            validators=[validators.InputRequired()])
    c_B = StringField(
            label='c(B) [mol/L]', default="1e-5",
            validators=[validators.InputRequired()])
    pKs_Ac = StringField(
            label='pKs(Ac)', default="[-1.32],[-3, 1.92],[-6]",
            validators=[validators.InputRequired()])
    pKs_B = StringField(
            label='pKs(B)', default="[9.25]",
            validators=[validators.InputRequired()])
    pKs_Tit = StringField(
            label='pKs(Tit)', default="[14]",
            validators=[validators.InputRequired()])
