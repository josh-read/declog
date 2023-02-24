from pathlib import Path
import runpy


def discover_examples():
    """Get a generator of every python file in the examples directory."""
    example_directory = Path('examples')
    return example_directory.glob('**/*.py')


def test_facility_example():
    path_to_example = Path('examples/facility_example/logger.py')
    assert path_to_example.exists()
    runpy.run_path(str(path_to_example), run_name='__main__')


if __name__ == '__main__':
    print(list(discover_examples()))
