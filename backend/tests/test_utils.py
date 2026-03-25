import pytest
from CITation.data.process_references import extract_reference_numbers


# TODO: add more tests
@pytest.mark.parametrize("ref,output", [("[1]", [1]), ("[1,2-4]", [1, 2, 3, 4])])
def test_extract_reference_numbers(ref, output):
    assert extract_reference_numbers(ref) == output
