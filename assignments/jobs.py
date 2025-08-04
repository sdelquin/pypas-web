import shlex
import subprocess

import pytest
from django.conf import settings


def test_assignment(assignment):
    cmd = settings.PYTEST_CMD.format(
        assignment_path=assignment.folder, uid=settings.PYTEST_UID, gid=settings.PYTEST_GID
    )
    ret = subprocess.run(shlex.split(cmd))
    assignment.passed = ret.returncode == pytest.ExitCode.OK
    assignment.save()
    assignment.dump_test()
    if not assignment.passed and assignment.chunk.pass_to_put:
        assignment.remove_folder()
        assignment.delete()
