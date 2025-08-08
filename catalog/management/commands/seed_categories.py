from django.core.management.base import BaseCommand
from catalog.models import Category

class Command(BaseCommand):
    help = 'Seed demo categories up to Level-2 only'

    def handle(self, *args, **kwargs):
        roots = ['Electronics', 'Clothing']
        children = {
            'Electronics': ['Smartphones', 'Laptops'],
            'Clothing': ["Men's Shirts", "Women's Wear"]
        }
        root_objs = {}
        for r in roots:
            obj, _ = Category.objects.get_or_create(name=r, parent=None)
            root_objs[r] = obj
        for r, kids in children.items():
            for k in kids:
                Category.objects.get_or_create(name=k, parent=root_objs[r])
        self.stdout.write(self.style.SUCCESS('Seeded categories (max Level-2)'))
