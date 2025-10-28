from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label='向AI提问（价格/物流/库存等）', max_length=300)
