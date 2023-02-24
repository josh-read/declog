from pathlib import Path
import runpy
import pytest


def discover_examples():
    """Get a generator of every python file in the examples directory."""
    example_directory = Path('examples')
    return example_directory.glob('**/*.py')


@pytest.mark.parametrize('path_to_example', discover_examples())
def test_facility_example(path_to_example):
    """Run example as __main__ and check there are no errors."""
    assert path_to_example.exists()
    runpy.run_path(str(path_to_example), run_name='__main__')
