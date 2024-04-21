from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    sales_ranking = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def short_description(self):
        return self.description[:100]

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['-updated','-created']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return str(self.product)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    order_history = models.ManyToManyField(Order)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

class Advertisement(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='advertisement_images/')
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()

class ForumTopic(models.Model):
    name =models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ForumPost(models.Model):
    host = models.ForeignKey(User, related_name='host', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    participants = models.ManyToManyField(User, null=True)
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated','-created']
    
class MessaageForum(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(ForumPost, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        ordering = ['-updated','-created']

class ForumComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.content[50])
    
    class Meta:
        ordering = ['-updated','-date_created']