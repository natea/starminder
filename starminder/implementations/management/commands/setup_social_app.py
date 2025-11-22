import parsenvy
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sets up the GitHub SocialApp for allauth."

    def handle(self, *args, **options):
        client_id = parsenvy.str("GITHUB_CLIENT_ID") or "dummy_client_id"
        secret = parsenvy.str("GITHUB_SECRET") or "dummy_secret"

        if client_id == "dummy_client_id":
            self.stdout.write(
                self.style.WARNING(
                    "GITHUB_CLIENT_ID or GITHUB_SECRET not found in environment. "
                    "Using dummy values. GitHub login will NOT work, but the page will load."
                )
            )

        site = Site.objects.get_current()
        site.domain = parsenvy.str("DJANGO_SITE_DOMAIN_NAME") or "127.0.0.1:8000"
        site.name = parsenvy.str("DJANGO_SITE_DISPLAY_NAME") or "Starminder Local"
        site.save()
        self.stdout.write(self.style.SUCCESS(f"Updated Site to {site.domain}"))
        
        social_app, created = SocialApp.objects.update_or_create(
            provider="github",
            defaults={
                "name": "GitHub",
                "client_id": client_id,
                "secret": secret,
            },
        )
        
        social_app.sites.add(site)
        
        if created:
            self.stdout.write(self.style.SUCCESS("Created GitHub SocialApp"))
        else:
            self.stdout.write(self.style.SUCCESS("Updated GitHub SocialApp"))
