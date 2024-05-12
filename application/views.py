from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from config import settings
from application.forms import ApplicationForm, ObjectsForm
from application.models import (
    Application,
    ApplicationProduct,
    ProductWarehouse,
    Product
)
from application.utils import check_deals_address, create_deals

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



@login_required
def index(request):
    template = 'application/index.html'
    title = 'Это главная страница'
    paginator = Paginator(request.user.applications.all(), settings.PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj
    }

    return render(request, template, context)


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            total_cost = 0
            use_nums = []
            for key in request.POST.keys():
                num = key.split('_')[-1]
                if num.isdigit() and num not in use_nums:
                    product_id = int(request.POST.get(f'product_{num}'))
                    quantity = float(request.POST.get(f'number_{num}'))
                    image = request.FILES.get(f'image_{num}')
                    product = ProductWarehouse.objects.get(pk=product_id)
                    total_cost += product.product.price * quantity
                    ApplicationProduct.objects.create(
                        application=application,
                        product=product.product,
                        quantity=quantity,
                        image=image,
                        warehouse=product.warehouse,
                        city=product.city
                    )
                    use_nums.append(num)
            application.total_cost = total_cost
            application.save()

            return redirect('application:index')
    form = ApplicationForm()
    return render(request, 'application/create_application.html', {
        'form': form,
        'title': 'Формирование заказа',
        'products': ProductWarehouse.objects.all(),
    })


@login_required
def application_detail(request, app_id):
    template = 'application/application_detail.html'
    app = get_object_or_404(Application, pk=app_id)
    title = str(app)
    context = {
        'title': title,
        'app': app,
    }
    return render(request, template, context)


@login_required
def application_delete(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    if app.status != 'Создан':
        return redirect('application:app_detail', app_id=app_id)
    app.delete()
    return redirect('application:index')


@login_required
def bitrix_deals(request):
    if request.method == 'POST':
        form = ObjectsForm(request.POST, request.FILES)
        if form.is_valid():
            save_object = form.save(commit=False)
            status = check_deals_address(save_object.city, save_object.street)
            if status:
                messages.error(request, 'Такой адрес уже существует')
                return render(request, 'application/bitrix_deal.html', {
                    'form': form,
                    'title': 'Привязать объект'
                })
            data = create_deals(save_object.city, save_object.street, save_object.house,request.user.email)
            save_object.user = request.user
            save_object.save()
            messages.success(request, 'Заявка успешно создана')
            return redirect('application:create_deals')

    form = ObjectsForm()
    return render(request, 'application/bitrix_deal.html', {
        'form': form,
        'title': 'Привязать объект'
    })


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'application/product_list.html'
    context_object_name = 'products'
    login_url = '/login/'

    def get_queryset(self):
        city = self.request.GET.get('city', '')
        warehouse = self.request.GET.get('warehouse', '')

        queryset = Product.objects.prefetch_related('stock').all()
        if city:
            queryset = queryset.filter(stock__city=city)
        if warehouse:
            queryset = queryset.filter(stock__warehouse=warehouse)

        return sorted(
            queryset,
            key=lambda x: (any(stock.in_stock == 0 for stock in x.stock.all()), x.name)
        )
