from flask_wtf import Form
from wtforms import HiddenField as hf


class MyTranslations(object):
    translations = {'Not a valid date value': 'Syötä päivämäärä muodossa pp.kk.vvvv'}

    def gettext(self, string):
        return self.translations.get(string, string)


class TranslatedForm(Form):

    def _get_translations(self):
        return MyTranslations()


class HiddenField(hf):
    hidden = True
