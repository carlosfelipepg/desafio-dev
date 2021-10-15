import pandas as pd
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from dateutil import parser
from .models import TFinances
from .serializers import FinancesSerializer


class FinancesView(ModelViewSet):
    queryset = TFinances.objects
    serializer_class = FinancesSerializer

    @action(methods=['POST'], detail=False)
    def upload_file(self, request):
        if request.method == 'POST':
            files = request.FILES
            for file in files:
                data = str(files[file].read().decode('utf-8')).split('\n')
                data = self.format_file(data[:-1])
                self.queryset.bulk_create(data, 100)
        return redirect('finances:success')

    @action(methods=['GET'], detail=False)
    def list_finances(self, request):
        template = loader.get_template('finances/list.html')
        finances_list = self.queryset.all() \
            .values('store', 'type', 'desc_type')\
            .annotate(total_value=Sum('value'))\
            .order_by('store')
        context = {
            'finances_list': finances_list
        }
        return HttpResponse(template.render(context, request))

    @action(methods=['GET'], detail=False)
    def success(self, request):
        return render(request, 'finances/success.html')

    @staticmethod
    def format_file(data):
        new_data = list()
        for obj in data:
            new_data.append(TFinances(
              type=obj[0],
              desc_type=FinancesView.get_description_type(obj[0]),
              date_hour=FinancesView.format_date_hour(obj[1:9] + 'T' + obj[42:48] + '-00:00'),
              value=int(obj[9:19])/100,
              cpf=obj[19:30],
              card=obj[30:42],
              store_owner=obj[48:62].rstrip(),
              store=obj[62:].rstrip()
            ))
        return new_data

    @staticmethod
    def format_date_hour(date):
        return parser.parse(date)

    @staticmethod
    def get_description_type(value):
        desc = {
            '1': 'Débito',
            '2': 'Boleto',
            '3': 'Financiamento',
            '4': 'Crédito',
            '5': 'Recebimento Empréstimo',
            '6': 'Vendas',
            '7': 'Recebimento TED',
            '8': 'Recebimento DOC',
            '9': 'Aluguel'
        }
        return desc[value]
