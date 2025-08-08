from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed common UOMs and Tax Rates'

    def handle(self, *args, **options):
        from catalog.models import UOM, TaxRate
        uoms = [
            {"code": "EA", "name": "Each", "decimals": 0},
            {"code": "BOX", "name": "Box", "decimals": 0},
            {"code": "PAIR", "name": "Pair", "decimals": 0},
        ]
        for u in uoms:
            UOM.objects.update_or_create(code=u['code'], defaults=u)
        taxes = [
            {"title": "GST 18%", "description": "Standard goods and services tax", "rate": 18},
            {"title": "VAT 5%", "description": "Reduced VAT for essentials", "rate": 5},
        ]
        for t in taxes:
            TaxRate.objects.update_or_create(title=t['title'], defaults=t)
        self.stdout.write(self.style.SUCCESS('Seeded UOMs and Tax Rates'))
