from django.core.management.base import BaseCommand

from access.models import Context, User
from assignments.models import Assignment
from frames.models import Bucket, Frame


class Command(BaseCommand):
    help = 'Get mark for a certain user & frame'

    def add_arguments(self, parser):
        parser.add_argument('context', type=str, help='Context slug')
        parser.add_argument('bucket', type=str, help='Bucket slug')
        parser.add_argument('user', type=str, help='User slug')

    def handle(self, *args, **options):
        try:
            context = Context.objects.get(slug=options['context'])
        except Context.DoesNotExist:
            print(f'Context <{options["context"]}> does not exist!')
            return
        try:
            bucket = Bucket.objects.get(slug=options['bucket'])
        except Bucket.DoesNotExist:
            print(f'Bucket <{options["bucket"]}> does not exist!')
            return
        try:
            user = User.objects.get(slug=options['user'], context=context)
        except User.DoesNotExist:
            print(f'User <{options["user"]}> does not exist!')
            return
        frame = Frame.objects.get(context=context, bucket=bucket)
        passed_assignments = Assignment.objects.filter(user=user, chunk__frame=frame, passed=True)
        mark = round(passed_assignments.count() / frame.num_exercises * 10, 2)
        print(mark)
