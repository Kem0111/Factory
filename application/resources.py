from django import forms
from import_export import resources, fields
from import_export.forms import ExportForm
from import_export.widgets import DateWidget

from application.models import Application


class ExportFilterForm(ExportForm):
    status = forms.ChoiceField(
        choices=[("all", "Все")] + list(Application.status_choices), required=False,
        label='Статус'
    )


class ApplicationResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    full_name = fields.Field(
        column_name='ФИО Заказчика',
        attribute='full_name'
    )
    phone_number = fields.Field(attribute='phone_number', column_name='Номер телефона')
    address = fields.Field(attribute='address', column_name='Адрес')
    status = fields.Field(attribute='status', column_name='Статус')
    total_cost = fields.Field(attribute='total_cost', column_name='Итоговая стоимость')
    provider = fields.Field(attribute='provider', column_name='Поставщик')
    manager = fields.Field(attribute='manager', column_name='Менеджер')
    created = fields.Field(attribute='created', column_name='Дата создания',
                           widget=DateWidget(format='%d.%m.%Y %H:%M'))

    def dehydrate_products(self, app: Application):
        return '\n'.join(f'{p.product.name} - {p.quantity}' for p in app.applicationproduct_set.all())

    class Meta:
        model = Application
        fields = (
            'id', 'full_name', 'products', 'phone_number', 'address', 'status', 'total_cost', 'provider', 'created')
        export_order = (
            'id', 'full_name', 'products', 'phone_number', 'address', 'status', 'total_cost', 'provider', 'created')
