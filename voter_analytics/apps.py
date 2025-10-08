from django.apps import AppConfig


class VoterAnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voter_analytics'

    def ready(self):
        import os
        from django.conf import settings
        from .models import Voter

        # Prevent running multiple times in dev server autoreload
        if os.environ.get('RUN_MAIN') == 'true':
            Voter.load_data()