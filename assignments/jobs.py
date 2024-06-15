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
