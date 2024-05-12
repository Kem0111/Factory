from django.core.files.storage import default_storage
from django.db import models
from django.utils.safestring import mark_safe

from application.utils import validate_phone
from users.models import CustomUser


class DeletableFileModel(models.Model):
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, models.FileField) or isinstance(field, models.ImageField):
                field_value = getattr(self, field.name)
                if field_value and default_storage.exists(field_value.name):
                    default_storage.delete(field_value.name)
        super().delete(*args, **kwargs)


class Product(DeletableFileModel):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=250
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        choices=(
            ('шт', 'шт'),
            ('кв', 'кв'),
            ('пог.м', 'пог.м'),
        ),
        max_length=10
    )
    price = models.FloatField(
        verbose_name='Цена'
    )
    photo = models.ImageField(
        upload_to='photo',
        verbose_name='Фото',
    )

    def image_tag(self):
        return mark_safe(f'<img src="{self.photo.url}" width="50"/>')

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} {self.price} руб./{self.unit}"


class Provider(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=150
    )
    address = models.TextField(
        verbose_name='Адрес'
    )
    full_name = models.CharField(
        verbose_name='ФИО',
        max_length=100
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        validators=[validate_phone],
        help_text='Введите номер телефона в формате +7 977 900 00 00',
        max_length=20
    )

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщик'

    def __str__(self):
        return f'{self.name} {self.name} {self.phone_number}'


class Application(models.Model):
    status_choices = (
        ('Создан', 'Создан'),
        ('На производстве', 'На производстве'),
        ('Упаковка', 'Упаковка'),
        ('Готов к отгрузке', 'Готов к отгрузке'),
        ('Готов', 'Готов'),
    )
    products = models.ManyToManyField(
        Product,
        through='ApplicationProduct',
        related_name='applications'
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Заказчик',
        on_delete=models.SET_NULL,
        related_name='applications',
        blank=True,
        null=True
    )
    full_name = models.CharField(
        verbose_name='ФИО менеджера',
        max_length=100
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона менеджера',
        validators=[validate_phone],
        help_text='Введите номер телефона в формате +7 977 900 00 00',
        max_length=20
    )
    address = models.TextField(
        verbose_name='Адрес доставки',
    )
    status = models.CharField(
        verbose_name='Статус работы',
        max_length=50,
        default='Создан',
        choices=status_choices
    )
    notes = models.TextField(
        verbose_name='Примечание',
        blank=True,
        null=True
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        related_name='applications',
        blank=True,
        null=True,
        verbose_name='Поставщик'
    )
    total_cost = models.FloatField(
        verbose_name='Итоговая стоимость',
        blank=True,
        null=True
    )
    manager = models.ForeignKey(
        CustomUser,
        verbose_name='Менеджер',
        on_delete=models.SET_NULL,
        related_name='manage_app',
        blank=True,
        null=True
    )
    overdue = models.BooleanField(
        verbose_name='Просрочено или нет',
        default=False
    )
    production_time = models.DateField(
        verbose_name='Сроки изготовления',
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения"
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заявки'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return str(self.pk)


class ApplicationProduct(DeletableFileModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', verbose_name='Образец')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    warehouse = models.CharField(
        verbose_name='Склад',
        max_length=100
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=100
    )
    quantity = models.FloatField(
        verbose_name='Количество'
    )

    def photo_tag(self):
        return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" width="100"/></a>')

    photo_tag.short_description = 'Образец'


class ProductWarehouse(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        related_name='stock'
    )
    warehouse = models.CharField(
        verbose_name='Склад',
        max_length=100
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=100
    )
    in_stock = models.FloatField(
        verbose_name='Остаток'
    )

    class Meta:
        verbose_name = 'Остатки'
        verbose_name_plural = 'Остатки'

    def __str__(self):
        if self.in_stock == 0:
            return f"{self.product.name} {self.product.price} руб./{self.product.unit} (ПОД ЗАКАЗ)"
        return (f"{self.product.name} {self.product.price} руб./{self.product.unit} {self.city} {self.warehouse} "
                f"Остаток: {self.in_stock} {self.product.unit}")


class Objects(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        related_name='objects',
        blank=True,
        null=True
    )
    city = models.CharField(
        verbose_name='Населенный пункт местонахождения объекта (город, поселок, станица и др.)',
        max_length=100
    )
    street = models.CharField(
        verbose_name='Улица местонахождения объекта',
        max_length=100
    )
    house = models.CharField(
        verbose_name='Дом местонахождения объекта',
        max_length=100
    )
    dealer_name = models.CharField(
        verbose_name='Наименование дилера',
        max_length=100
    )
    manager = models.CharField(
        verbose_name='Менеджер от дилера (ФИО И номер телефона)',
        max_length=100
    )
    main_name = models.CharField(
        verbose_name='ФИО, должность контактного лица с которым '
                     'ведутся переговоры',
        max_length=100
    )
    main_phone = models.CharField(
        verbose_name='Телефон контактного лица (Полностью без сокращений)',
        max_length=100
    )
    full_address = models.CharField(
        verbose_name='Полный адрес',
        max_length=255
    )
    full_name_object = models.CharField(
        verbose_name='Полное наименование объекта',
        max_length=100
    )
    architect = models.CharField(
        verbose_name='Архитектор/ аритектурная организация',
        max_length=100
    )
    investor = models.CharField(
        verbose_name='Инвестор/ застройщик',
        max_length=100
    )
    materials = models.CharField(
        verbose_name='Конкурирующие материалы',
        max_length=100
    )
    stages = models.CharField(
        verbose_name='Стадии реализации проекта',
        max_length=100
    )
    date_of_delivery = models.DateField(
        verbose_name='Дата поставки'
    )
    document = models.FileField(
        upload_to='document',
        verbose_name='Титульный лист/Или визуализация проекта',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Объекты'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.full_name_object
