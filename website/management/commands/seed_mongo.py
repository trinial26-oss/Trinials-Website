from django.core.management.base import BaseCommand
from website.mongo import (
    seed_email_config_to_mongo,
    seed_admin_credentials_to_mongo,
    get_mongo_db,
    list_recent_enquiries
)


class Command(BaseCommand):
    help = "Seed or update email configuration and admin credentials in MongoDB Atlas."

    def handle(self, *args, **options):
        self.stdout.write("Connecting to MongoDB Atlas...")
        db = get_mongo_db()
        if db is None:
            self.stderr.write(self.style.ERROR("Could not connect to MongoDB Atlas! Check MONGO_URI."))
            return

        self.stdout.write(self.style.SUCCESS(f"Connected to MongoDB Atlas: {db.name}"))

        success_mail = seed_email_config_to_mongo()
        if success_mail:
            self.stdout.write(self.style.SUCCESS("Successfully synced email_config into collection 'app_config'."))
        else:
            self.stderr.write(self.style.ERROR("Failed to sync email_config to MongoDB Atlas."))

        success_admin = seed_admin_credentials_to_mongo()
        if success_admin:
            self.stdout.write(self.style.SUCCESS("Successfully synced admin_auth (password: Trinialjo@2026) into collection 'app_config'."))
        else:
            self.stderr.write(self.style.ERROR("Failed to sync admin_auth to MongoDB Atlas."))

        enquiries = list_recent_enquiries(limit=5)
        self.stdout.write(f"Total recent enquiries retrieved: {len(enquiries)}")
        for e in enquiries:
            dispatch = e.get('email_dispatch', {})
            self.stdout.write(f" - [{e.get('created_at')}] {e.get('name')} <{e.get('email')}> | Team Dispatched: {dispatch.get('team_dispatched')}")

