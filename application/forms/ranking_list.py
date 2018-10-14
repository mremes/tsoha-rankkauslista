from flask_wtf import Form
from wtforms import StringField, validators, RadioField, IntegerField


class RankingListForm(Form):
    name = StringField(
        'Nimi', [validators.DataRequired(), validators.Length(min=6, max=60,
                                                              message="Nimen pitää olla vähintään 2 ja enintään 60 merkkiä pitkä.")])
    gender_filter = RadioField('Sukupuoli', choices=[('mies', 'mies'),
                                                     ('nainen', 'nainen'),
                                                     ('mikä tahansa', 'mikä tahansa')])
    age_cap_hi = IntegerField('Iän yläikäraja',
                              [validators.NumberRange(min=2, max=130, message="Iän pitää olla välillä 2 ja 130.")])
    age_cap_lo = IntegerField('Iän alaikäraja',
                              [validators.NumberRange(min=2, max=130, message="Iän pitää olla välillä 2 ja 130.")])

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
