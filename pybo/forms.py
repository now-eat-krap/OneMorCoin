from django import forms
from pybo.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

#class TradeHistoryFrom(forms.ModelForm):
#    class Meta:
#        model = TradeHistory
#        fields = [
#                  'crypto',
#                  'symbol',
#                  'open_time',
#                  'open_timestamp',
#                  'close_time',
#                  'close_timestamp',
#                  'side',
#                  'leverage',
#                  'open_amount',
#                  'close_amount',
#                  'open_price',
#                  'close_price',
#                  'open_cost',
#                  'close_cost',
#                  'tp',
#                  'sl',
#                  'open_commission_fee',
#                  'close_commission_fee',
#                  'funding_fee',
#                  'insurance_clear',
#                  'realized_pnl',
#                  'pnl',
#                  'pnl_percentage',
#                  'open_balance',
#                  'close_balance',
#                 ]
