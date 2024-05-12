from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from application.models import Application, Product, ApplicationProduct, Provider, ProductWarehouse, Objects
from application.resources import ApplicationResource, ExportFilterForm
from users.models import CustomUser


class BotAdminSite(AdminSite):
    site_title = "Управление заявками"
    site_header = "Управление заявками"
    index_title = ""


bot_admin = BotAdminSite()


@admin.register(CustomUser, site=bot_admin)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'first_name',
        'last_name',
        'status',
    )

    list_display_links = ('pk',)
    search_fields = ('email', 'first_name', 'last_name',)
    list_editable = ('status',)
    list_filter = ('status',)

    class Meta:
        verbose_name_plural = 'Пользователи'


class ProductInline(admin.TabularInline):
    model = ApplicationProduct
    verbose_name = 'Товары'
    verbose_name_plural = 'Товары'
    fields = ('product', 'quantity', 'warehouse', 'city', 'photo_tag')
    extra = 3
    max_num = 0
    readonly_fields = [field.name for field in ApplicationProduct._meta.fields]
    readonly_fields.append('photo_tag')


@admin.register(Application, site=bot_admin)
class ApplicationAdmin(ImportExportModelAdmin):
    resource_class = ApplicationResource
    list_display = (
        'pk',
        'total_cost',
        'user',
        'full_name',
        'phone_number',
        'address',
        'status',
        'notes',
        'provider',
        'overdue',
        'manager',
        'created',
        'updated',
    )

    list_display_links = ('pk',)
    list_filter = ('user', 'status', 'provider', 'manager',)
    empty_value_display = '-пусто-'
    search_fields = ('full_name', 'phone_number', 'pk',)
    inlines = (ProductInline,)

    def get_export_form_class(self):
        return ExportFilterForm

    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)

        status = request.POST.get('status')

        if status and status != "all":
            queryset = queryset.filter(status=status)

        return queryset

    class Meta:
        verbose_name_plural = 'Заявки'


@admin.register(Product, site=bot_admin)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'unit',
        'price',
        'image_tag',
    )

    list_display_links = ('pk',)
    list_editable = ('name', 'unit', 'price',)
    list_filter = ('unit',)
    empty_value_display = '-пусто-'
    search_fields = ('name',)

    class Meta:
        verbose_name_plural = 'Заявки'


@admin.register(Provider, site=bot_admin)
class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'address',
        'phone_number',
        'full_name',
    )

    list_display_links = ('pk',)
    empty_value_display = '-пусто-'
    search_fields = ('name', 'phone_number', 'full_name')

    class Meta:
        verbose_name_plural = 'Поставщик'


@admin.register(ProductWarehouse, site=bot_admin)
class ProductWarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'warehouse',
        'city',
        'in_stock',
    )

    list_display_links = ('pk',)
    empty_value_display = '-пусто-'
    search_fields = ('product__name', 'warehouse', 'city')
    list_editable = ('product', 'warehouse', 'city', 'in_stock')

    class Meta:
        verbose_name_plural = 'Остатки'


@admin.register(Objects, site=bot_admin)
class ObjectsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'city',
        'street',
        'house',
        'dealer_name',
        'manager',
        'main_name',
        'main_phone',
        'full_address',
        'full_name_object',
        'architect',
        'investor',
        'materials',
        'stages',
        'date_of_delivery',
        'document_mod',
    )

    list_display_links = ('pk',)
    empty_value_display = '-пусто-'
    search_fields = ('city', 'street', 'house', 'dealer_name', 'manager', 'main_name', 'main_phone',
                     'full_address', 'full_name_object', 'architect', 'investor', 'materials', 'stages', 'document')

    def document_mod(self, obj):
        return mark_safe(f'<a href={obj.document.url}>Перейти к документу</a>') if obj.document else ''

    document_mod.short_description = 'Титульный лист/Или визуализация проекта'

    class Meta:
        verbose_name_plural = 'Объекты'
