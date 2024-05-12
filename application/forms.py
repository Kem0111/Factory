from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import inlineformset_factory, DateTimeInput, DateInput

from application.models import Application, ApplicationProduct, Objects


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'phone_number', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'lnr lnr-user form-control', 'icon_class': 'lnr lnr-user', 'placeholder': 'ФИО'}),
            'phone_number': forms.TextInput(attrs={'class': 'lnr lnr-smartphone form-control', 'icon_class': 'lnr lnr-smartphone top-40', 'placeholder': 'Номер'}),
            'address': forms.Textarea(attrs={'class': 'lnr lnr-home form-control', 'icon_class': 'lnr lnr-home', 'placeholder': 'Адрес'}),
        }


class ApplicationProductForm(forms.ModelForm):
    class Meta:
        model = ApplicationProduct
        fields = ('product', 'quantity', 'image')


ApplicationProductFormSet = inlineformset_factory(Application, ApplicationProduct, form=ApplicationProductForm, extra=1)


# class BitrixForm(forms.Form):
#     product_name = forms.CharField(label='Наименование (товар)', max_length=100, required=True)
#     city = forms.CharField(label='Город', max_length=100, required=True)
#     street = forms.CharField(label='Улица', max_length=100, required=True)
#     house = forms.CharField(label='Дом', max_length=100, required=True)


class ObjectsForm(forms.ModelForm):
    date_of_delivery = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата поставки'
    )
    full_address = forms.CharField(
        widget=forms.Textarea(attrs={'icon_class': 'lnr lnr-home', 'placeholder': 'Полный адрес'}),
        label='Полный адрес'
    )

    class Meta:
        model = Objects
        fields = ('city', 'street', 'house', 'dealer_name',
                  'manager', 'main_name', 'main_phone', 'full_address',
                  'full_name_object', 'architect', 'investor', 'materials',
                  'stages', 'date_of_delivery', 'document')
        widgets = {
            'city': forms.TextInput(attrs={'class': 'lnr lnr-map-marker form-control', 'icon_class': 'lnr lnr-map-marker', 'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'class': 'lnr lnr-map-marker form-control', 'icon_class': 'lnr lnr-map-marker', 'placeholder': 'Улица'}),
            'house': forms.TextInput(attrs={'class': 'lnr lnr-home form-control', 'icon_class': 'lnr lnr-home', 'placeholder': 'Дом'}),
            'dealer_name': forms.TextInput(attrs={'class': 'lnr lnr-user form-control', 'icon_class': 'lnr lnr-user', 'placeholder': 'Имя дилера'}),
            'manager': forms.TextInput(attrs={'class': 'lnr lnr-user form-control', 'icon_class': 'lnr lnr-user', 'placeholder': 'Менеджер'}),
            'main_name': forms.TextInput(attrs={'class': 'lnr lnr-user form-control', 'icon_class': 'lnr lnr-user', 'placeholder': 'Основное имя'}),
            'main_phone': forms.TextInput(attrs={'class': 'lnr lnr-phone-handset form-control', 'icon_class': 'lnr lnr-phone-handset', 'placeholder': 'Основной телефон'}),
            'full_name_object': forms.TextInput(attrs={'class': 'lnr lnr-construction form-control', 'icon_class': 'lnr lnr-construction', 'placeholder': 'Название объекта'}),
            'architect': forms.TextInput(attrs={'class': 'lnr lnr-user form-control', 'icon_class': 'lnr lnr-user', 'placeholder': 'Архитектор'}),
            'investor': forms.TextInput(attrs={'class': 'lnr lnr-user form-control', 'icon_class': 'lnr lnr-user', 'placeholder': 'Инвестор'}),
            'materials': forms.Textarea(attrs={'class': 'lnr lnr-cart form-control', 'icon_class': 'lnr lnr-cart', 'placeholder': 'Материалы'}),
            'stages': forms.Textarea(attrs={'class': 'lnr lnr-layers form-control', 'icon_class': 'lnr lnr-layers', 'placeholder': 'Этапы'}),
            'date_of_delivery': forms.DateInput(attrs={'type': 'date', 'class': 'lnr lnr-calendar-full form-control', 'icon_class': 'lnr lnr-calendar-full', 'placeholder': 'Дата поставки'}),
            'document': forms.FileInput(attrs={'class': 'lnr lnr-file-add form-control', 'icon_class': 'lnr lnr-file-add', 'placeholder': 'Документ'})
        }
