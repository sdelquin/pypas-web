from pathlib import Path

import toml
from django.core.management.base import BaseCommand

from .helpers.manage_pypas_toml import manipulate


def bump_version(version: str, bump_type: str) -> str:
    major, minor, patch = map(int, version.split('.'))
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    return f'{major}.{minor}.{patch}'


class Command(BaseCommand):
    help = 'Fix .pypas.toml configuration file for exercises'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--release_notes', type=str, help='Release notes')
        parser.add_argument('-b', '--bump', type=str, help='Bump version: major, minor, patch')
        parser.add_argument(
            '-n', '--dry-run', action='store_true', help='Dry run without writing changes'
        )

    def handle(self, *args, **options):
        for config_file in Path('repository').glob('**/.pypas.toml'):
            config = toml.load(config_file)
            config = manipulate(config)
            if options['bump']:
                if not options['release_notes']:
                    self.stderr.write('Release notes must be provided when bumping version.')
                    return
                current_version = config.get('version', '0.0.0')
                new_version = bump_version(current_version, options['bump'])
                config['version'] = new_version
                config['release_notes'][new_version] = options['release_notes']
            if options['dry_run']:
                print(self.style.WARNING(f'\nDry run - changes to {config_file}:'))
                self.stdout.write(toml.dumps(config))
            else:
                with open(config_file, 'w') as f:
                    toml.dump(config, f)
                print(self.style.SUCCESS(f'Updated {config_file}'))
