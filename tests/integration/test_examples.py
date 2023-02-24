from pathlib import Path
import runpy


def test_facility_example():
    path_to_example = Path('examples/facility_example/logger.py')
    assert path_to_example.exists()
    runpy.run_path(str(path_to_example), run_name='__main__')
