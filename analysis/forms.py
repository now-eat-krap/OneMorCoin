from django import forms
from .models import TradeHistory

class TradeHistoryFrom(forms.ModelForm):
    class Meta:
        model = TradeHistory
        fields = [
                  'crypto',
                  'symbol',
                  'open_time',
                  'open_timestamp',
                  'close_time',
                  'close_timestamp',
                  'side',
                  'leverage',
                  'open_amount',
                  'close_amount',
                  'open_price',
                  'close_price',
                  'open_cost',
                  'close_cost',
                  'tp',
                  'sl',
                  'open_commission_fee',
                  'close_commission_fee',
                  'funding_fee',
                  'insurance_clear',
                  'realized_pnl',
                  'pnl',
                  'pnl_percentage',
                  'open_balance',
                  'close_balance',
                 ]
