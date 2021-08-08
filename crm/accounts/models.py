from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=200, null=True,verbose_name='Имя')
    phone = models.CharField(max_length=200, null=True,verbose_name='Телефон')
    email = models.CharField(max_length=200, null=True,verbose_name='Е-майл')
    profile_pic = models.ImageField(default='default_profile_pic.png',null=True, blank=True, verbose_name='Аватар')
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Product(models.Model):
    CATEGORY = (
        ('На складе', 'На складе'),
        ('Вне склада','Вне склада'),
    )
    name = models.CharField(max_length=200, null=True,verbose_name='Продукт')
    category = models.CharField(max_length=200, null=True,choices=CATEGORY,verbose_name='Категория')
    price = models.FloatField(null=True,verbose_name='Цена')
    description = models.CharField(max_length=200, null=True,verbose_name='Описание')
    tag = models.ManyToManyField('Tag', verbose_name='Тэг')
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Order(models.Model):
    STATUS = (
        ('В ожидании', 'В ожидании'),
        ('В доставке', 'В доставке'),
        ('Доставлен', 'Доставлен'),
    )
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,verbose_name='Пользователь')
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL, verbose_name='Продукт')
    note = models.CharField(max_length=1000,  null=True,verbose_name='Note')
    status = models.CharField(max_length=200, choices=STATUS, null=True,verbose_name='Статус')
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f'Заказ #{self.id} {self.customer}'
    class Meta:
        ordering = ('-data_created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name='Тэг')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'