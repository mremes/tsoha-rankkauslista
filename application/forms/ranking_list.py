from flask_wtf import Form
from wtforms import StringField, validators, RadioField, IntegerField


class RankingListForm(Form):
    name = StringField('Nimi', [validators.DataRequired(), validators.Length(min=6)])
    gender_filter = RadioField('Sukupuoli', choices=[('mies', 'mies'),
                                                     ('nainen', 'nainen'),
                                                     ('mikä tahansa', 'mikä tahansa')])
    age_cap_hi = IntegerField('Iän yläikäraja')
    age_cap_lo = IntegerField('Iän alaikäraja')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.ranking_list = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        return True

    @property
    def genders(self):
        if self.gender_filter.data == 'mies':
            return ['mies']
        elif self.gender_filter.data == 'nainen':
            return ['nainen']
        elif self.gender_filter.data == 'mikä tahansa':
            return ['mies', 'nainen', 'muu']