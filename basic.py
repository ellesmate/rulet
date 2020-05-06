from api.models import Entity, Category, MenuItem

def create():
    dodo = Entity.objects.create(name='ДОДО ПИЦЦА', image='додо.jpeg', address='г. Минск, ул. Петра Глебки, 5', phone=7576, rate=4.86)
    vesl = Entity.objects.create(name='Суши весла', image='сушивесла.jpg', address='г. Минск, проспект Независимости, 76', phone=375445706662, rate=4.7)

    c1 = Category.objects.create(name='Пиццы', image='пицца.jpeg', entity=dodo)
    c2 = Category.objects.create(name='Десерты', image='десерты.jpeg', entity=dodo)
    c3 = Category.objects.create(name='Сеты', image='сеты.jpeg', entity=vesl)
    c4 = Category.objects.create(name='Супы', image='супы.jpeg', entity=vesl)


    m1 = MenuItem.objects.create(item_type='Рулетики с брусниой', price=630, available=True, 
                                item_description='Сладкие рулетики с натуральной брусникой политые сгущенным молоком, 16 шт.',
                                image='рулетики_с_брусники.jpeg', size=16, category=c2, entity=dodo)
    m2 = MenuItem.objects.create(item_type='Рулетики с корицей', price=490, available=True, 
                                item_description='Горячие сладкие рулетики с пряной корицей и сахаром, 16 шт.',
                                image='рулетики_с_корицей.jpeg', size=16, category=c2, entity=dodo)
    m3 = MenuItem.objects.create(item_type='Сырный цыпленок', price=1390, available=True, 
                                item_description='Сырный соус, цыпленок, томаты, моцарелла',
                                image='Сырный_цыпленок.jpg', size=460, category=c1, entity=dodo)
    m4 = MenuItem.objects.create(item_type='Сырная', price=740, available=True, 
                                item_description='Томатный соус, моцарелла',
                                image='Сырная.jpg', size=360, category=c1, entity=dodo)
    m5 = MenuItem.objects.create(item_type='Ветчена и грибы', price=790, available=True, 
                                item_description='Томатный соус, моцарелла, ветчина, шампиньоны',
                                image='ветчена_и_грибы.jpg', size=435, category=c1, entity=dodo)
    m6 = MenuItem.objects.create(item_type='Суп Рамен со свининой', price=590, available=True, 
                                item_description='355г или 620г, свинина, капуста пекинская, морковь, брокколи, шпинат, помидор, грибы Шиитаке отварные, лапша яичная, яйцо, сельдерей стебель, лук зеленый',
                                image='супы_FsRofv9.jpeg', size=355, category=c4, entity=vesl)
    m7 = MenuItem.objects.create(item_type='Суп с тигровыми креветками', price=890, available=True, 
                                item_description='355г или 620г, окорочок куриный, брокколи, капуста пекинская, шпинат, морковь, помидор, грибы Шиитаке отварные, лапша яичная, яйцо, стебель сельдерея, лук зеленый',
                                image='тайский.jpeg', size=300, category=c4, entity=vesl)
    m8 = MenuItem.objects.create(item_type='Сет 1 на 3 человека', price=3750, available=True, 
                                item_description='732г, Кияри маки (1/2), Кайсо маки (1/2), Умаи маки (1/2), Филадельфия маки (1/2), Асахи маки (1/2), New Филадельфия маки (1/2)',
                                image='сеты_Yr371pl.jpeg', size=732, category=c3, entity=vesl)
    m9 = MenuItem.objects.create(item_type='Сет 2 на 3 человека', price=2340, available=True, 
                                item_description='677г, Сакура маки (1/2), Карай маки (1/2), Филадельфия маки (1/2), Бунсай маки (1/2), Хоккайдо маки (1/2), Мияги маки (1/2)',
                                image='сет2.jpeg', size=677, category=c3, entity=vesl)

