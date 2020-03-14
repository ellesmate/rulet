from django.db import models  # TODO: SqlLite to PostgreSQL


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} the place"


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.place.name} the restaurant"


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField()  # Price dollar * 100
    time = models.TimeField()
    recipe = models.TextField()
    total_weight = models.FloatField()  # TODO: Auto calculating field

    def __str__(self):
        return f"{self.name}:{self.price/100}$/{self.total_weight}g"


class Order(models.Model):
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return ", ".join([p.name for p in self.products.all()]) + " for " + str(self.customer)


class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    weight = models.FloatField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} employee at {self.restaurant}"
