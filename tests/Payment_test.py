from unittest.mock import Mock
from services.library_service import pay_late_fees
from services.payment_service import PaymentGateway
from tests.tools import invalidBookStub, invalidLateStub, lateStub, notLateStub, validBookStub

# Test successful payment
def test_successful(mocker):
    validBookStub(mocker)
    lateStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")

    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == True
    assert txn == "txn_123"
    assert "success" in msg.lower()

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(patron_id="123456", amount=9.5, description="Late fees for 'To Kill A Mockingbird'")
    
# payment declined by gateway
def test_gateway_declined(mocker):
    lateStub(mocker)
    validBookStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")

    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert txn == None
    assert "failed" in msg.lower()

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(patron_id="123456", amount=9.5, description="Late fees for 'To Kill A Mockingbird'")
    
# invalid late calculation
def test_invalid_late(mocker):
    invalidLateStub(mocker)
    validBookStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")

    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert txn == None
    assert "unable" in msg.lower()

    mock_gateway.process_payment.assert_not_called()

# invalid book
def test_invalid_book(mocker):
    lateStub(mocker)
    invalidBookStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")

    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert txn == None
    assert "not found" in msg.lower()

    mock_gateway.process_payment.assert_not_called()
    
# invalid patron ID (verify mock NOT called)
def test_bad_patron(mocker):
    lateStub(mocker)
    validBookStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")

    success, msg, txn = pay_late_fees("1234567", 1, mock_gateway)

    assert success == False
    assert txn == None
    assert "patron id" in msg.lower()

    mock_gateway.process_payment.assert_not_called()

# zero late fees (verify mock NOT called)
def test_not_late(mocker):
    notLateStub(mocker)
    validBookStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")

    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success == False
    assert txn == None
    assert "no late fees" in msg.lower()

    mock_gateway.process_payment.assert_not_called()

# network error handling
def test_network_error(mocker):
    lateStub(mocker)
    validBookStub(mocker)
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.sideEffect = ConnectionError("Something went wrong")

    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    
    assert success == False
    assert txn == None
    assert "payment processing error" in msg.lower()

    mock_gateway.process_payment.assert_called_once()
    mock_gateway.process_payment.assert_called_with(patron_id="123456", amount=9.5, description="Late fees for 'To Kill A Mockingbird'")
    