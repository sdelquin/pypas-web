import datetime
import os
import shlex
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Backup all project'

    def add_arguments(self, parser):
        parser.add_argument('-b', '--backup-dir', type=Path, default=settings.BACKUP_DIR)
        parser.add_argument('-k', '--backup-keep', type=int, default=settings.NUM_BACKUPS_TO_KEEP)

    def handle(self, *args, **options):
        folder = datetime.date.today().strftime('%Y-%m-%d')
        output_folder = options['backup_dir'] / folder
        output_folder.mkdir(parents=True, exist_ok=True)
        db_config = settings.DATABASES['default']
        # database backup
        output_db_path = output_folder / 'db.sql'
        cmd = f"pg_dump -c -h localhost -U {db_config['USER']} {db_config['NAME']} -f {output_db_path}"
        subprocess.run(shlex.split(cmd), env=dict(os.environ, PGPASSWORD=db_config['PASSWORD']))
        # remove old backups
        current_backup_dirs = sorted(options['backup_dir'].glob(r'[0-9]*'))
        if (num_dirs_to_remove := len(current_backup_dirs) - options['backup_keep']) > 0:
            for dir in current_backup_dirs[:num_dirs_to_remove]:
                dir.rmdir()
