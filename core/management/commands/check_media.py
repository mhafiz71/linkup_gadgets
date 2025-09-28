from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check media files configuration and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking media configuration...'))
        
        # Check if media directory exists
        if os.path.exists(settings.MEDIA_ROOT):
            self.stdout.write(f'✓ Media directory exists: {settings.MEDIA_ROOT}')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Media directory missing: {settings.MEDIA_ROOT}'))
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            self.stdout.write(f'✓ Created media directory: {settings.MEDIA_ROOT}')
        
        # Check permissions
        if os.access(settings.MEDIA_ROOT, os.W_OK):
            self.stdout.write('✓ Media directory is writable')
        else:
            self.stdout.write(self.style.ERROR('✗ Media directory is not writable'))
        
        # List some media files
        media_files = []
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files[:5]:  # Show first 5 files
                rel_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
                media_files.append(rel_path)
        
        if media_files:
            self.stdout.write(f'Sample media files found: {", ".join(media_files)}')
        else:
            self.stdout.write('No media files found')
        
        self.stdout.write(f'Media URL: {settings.MEDIA_URL}')
        self.stdout.write(f'Debug mode: {settings.DEBUG}')
        self.stdout.write(self.style.SUCCESS('Media check complete!'))