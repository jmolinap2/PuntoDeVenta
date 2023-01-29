from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.pos.models import Sale, Client
from core.reports.forms import ReportForm


class ReportSaleView(FormView):
    template_name = 'sale/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                queryset = Sale.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for s in queryset:
                    data.append([
                        s.id,
                        s.client.names,
                        s.date_joined.strftime('%Y-%m-%d'),
                        f'{s.subtotal:.2f}',
                        f'{s.total_dscto:.2f}',
                        f'{s.total_iva:.2f}',
                        f'{s.total:.2f}',
                    ])

                subtotal = queryset.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('r')
                iva = queryset.aggregate(r=Coalesce(Sum('total_iva'), 0, output_field=FloatField())).get('r')
                dscto = queryset.aggregate(r=Coalesce(Sum('total_dscto'), 0, output_field=FloatField())).get('r')
                total = queryset.aggregate(r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    f'{subtotal:.2f}',
                    f'{dscto:.2f}',
                    f'{iva:.2f}',
                    f'{total:.2f}',
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('sale_report')
        return context


class ReportClientView(FormView):
    template_name = 'client/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = {'categories': [], 'series': []}
                year = int(request.POST['year'])
                month = int(request.POST['month'])
                queryset = Sale.objects.filter(date_joined__year=year, date_joined__month=month)
                clients = list(queryset.values_list('client_id', flat=True).order_by('client_id').distinct())
                for client in Client.objects.filter(id__in=clients):
                    data['categories'].append(client.names)
                    amount = float(queryset.filter(client_id=client.id).aggregate(result=Coalesce(Sum('total'), 0, output_field=FloatField())).get('result'))
                    data['series'].append(round(amount, 2))
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Clientes'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('client_report')
        return context
