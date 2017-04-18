from wtforms import Form, StringField, validators, SelectField, RadioField

class InputForm(Form):
    v_Ac = StringField(
            label='V(Ac) [L]', default="0.02",
            validators=[validators.InputRequired()])
    c_Ac = StringField(
            label='c(Ac) [mol/L]', default="0.1",
            validators=[validators.InputRequired()])
    pKs_Ac = StringField(
            label='pKs(Ac)', default="[-6]",
            validators=[validators.InputRequired()])
    v_B = StringField(
            label='V(B) [L]', default="0",
            validators=[validators.InputRequired()])
    c_B = StringField(
            label='c(B) [mol/L]', default="0",
            validators=[validators.InputRequired()])
    pKs_B = StringField(
            label='pKs(B)', default="[0]",
            validators=[validators.InputRequired()])
    v_sample = StringField(
            label='V(total) [L]', default="0.02",
            validators=[validators.InputRequired()])
    c_Tit = StringField(
            label='c(Tit) [mol/L]', default="0.1",
            validators=[validators.InputRequired()])
    v_Tit = StringField(
           label='V(Tit) [L]', default="0.04",
            validators=[validators.InputRequired()])
    pKs_Tit = StringField(
            label='pKs(Tit)', default="[14]",
            validators=[validators.InputRequired()])
    erase = RadioField('New Figure?', choices=[('True', 'Yes'),
            ('False', 'No')])
