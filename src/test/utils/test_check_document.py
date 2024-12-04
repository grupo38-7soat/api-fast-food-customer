from src.utils.check_document import validate_document

def test_validate_document_valid():
    document = "12345678909"
    result = validate_document(document)
    assert result['status'] == True

def test_validate_document_invalid_length():
    document = "12345678"
    result = validate_document(document)
    assert result['status'] == False

def test_validate_document_repeated_digits():
    document = "11111111111"
    result = validate_document(document)
    assert result['status'] == False

def test_validate_document_invalid_checksum():
    document = "12345678900"
    result = validate_document(document)
    assert result['status'] == False