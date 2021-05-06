from django import forms

class Match(forms.Form):
    winner = forms.ChoiceField(choices= [("1", "2")])
    def get_fields(self, member1, member2):
        CHOICES=[(member1.last_known_name, member2.last_known_name)]
        self.fields["winner"] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)