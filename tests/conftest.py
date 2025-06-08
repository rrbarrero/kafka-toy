import pytest

from consumer.infra.filesystem_repo import FileSystemRepo


@pytest.fixture
def filesystem_repo(tmp_path):
    return FileSystemRepo(output_path=tmp_path)
