from flask_wtf import Form
from . import TournamentPrize
from . import db
from wtforms import IntegerField


class TournamentPrizesForm(Form):
    dyn_attrs = []

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        return True

    @staticmethod
    def update_form_fields(num_players):
        for attr in TournamentPrizesForm.dyn_attrs:
            setattr(TournamentPrizesForm, attr, None)
        TournamentPrizesForm.dyn_attrs = []

        for i in range(num_players):
            attr = 'p{}'.format(i)
            setattr(TournamentPrizesForm,
                    attr,
                    IntegerField('%d. sijoituksen palkinto' % (i+1)))
            TournamentPrizesForm.dyn_attrs.append(attr)

    def create_prizes(self, tournament):
        prizes = []
        # Create tournament player pairs
        for i in range(len(self.dyn_attrs)):
            prize_money = getattr(self, self.dyn_attrs[i]).data
            prize = TournamentPrize(tournament, i+1, prize_money)
            db.session().add(prize)
            prizes.append(prize)
        db.session().commit()
        return prizes
