from django.core.management.base import BaseCommand

from chunks.models import Chunk


class Command(BaseCommand):
    help = 'Make chunks puttable or not'

    def add_arguments(self, parser):
        (
            parser.add_argument(
                'frame',
                type=str,
                help='Frame where the chunks are located (format: context_slug/bucket_slug).',
            ),
        )
        (
            parser.add_argument(
                '-n',
                '--non-puttable',
                action='store_true',
                default=False,
                help='Make chunks non-puttable.',
            ),
        )
        (
            parser.add_argument(
                '-e',
                '--exercise',
                type=str,
                help='Exercise slug to filter chunks.',
            ),
        )
        parser.add_argument(
            '-t',
            '--topic',
            type=str,
            help='Topic slug to filter chunks (format: primary_topic/secondary_topic).',
        )
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            default=False,
            help='Force the update without confirmation.',
        )

    def handle(self, *args, **options):
        make_puttable = not options['non_puttable']
        chunks = Chunk.filter_by_frame_slug(options['frame'])
        if options['exercise']:
            chunks = chunks.filter(exercise__slug=options['exercise'])
        if options['topic']:
            primary_topic, secondary_topic = options['topic'].split('/', 1)
            chunks = chunks.filter(exercise__topic__primary=primary_topic)
            if secondary_topic:
                chunks = chunks.filter(exercise__topic__secondary=secondary_topic)
        if not chunks.exists():
            print(self.style.WARNING('No chunks found with the specified criteria.'))
            return
        print(
            f'Following chunks ({chunks.count()}) will be updated with [puttable={make_puttable}]'
        )
        print('=' * 80)
        for chunk in chunks:
            print(f'* {chunk}')
        print('=' * 80)
        if not options['force']:
            confirm = input('Are you sure you want to proceed? (y/n): ')
            if confirm.lower() != 'y':
                print(self.style.WARNING('Operation cancelled.'))
                return
        chunks.update(puttable=make_puttable)
        print(self.style.SUCCESS('Chunks updated successfully.'))
