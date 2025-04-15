from django.core.management.base import BaseCommand
from currencies.views import start_bot


class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write("Функция start_bot запускается")
        try:
            start_bot()
        except Exception as e:
            self.stderr.write(f"Ошибка: {e}")
        finally:
            self.stdout.write("Функция start_bot завершила работу")