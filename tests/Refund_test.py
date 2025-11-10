from unittest.mock import Mock
from services.library_service import refund_late_fee_payment
from services.payment_service import PaymentGateway

# successful refund 
def test_successful(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $9.5 processed successfully. Refund ID: refund_123")

    success, msg = refund_late_fee_payment("txn_123", 9.5, mock_gateway)

    assert success == True
    assert "success" in msg.lower()

    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with("txn_123", 9.5)

# invalid transaction ID rejection
def test_txn_reject(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $9.5 processed successfully. Refund ID: refund_123")

    success, msg = refund_late_fee_payment("rxn_123", 9.5, mock_gateway)

    assert success == False
    assert "invalid" in msg.lower()

    mock_gateway.refund_payment.assert_not_called()

# invalid refund amounts (negative, zero, exceeds $15 maximum).
def test_negative_refund(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")

    success, msg = refund_late_fee_payment("txn_123", -9.5, mock_gateway)

    assert success == False
    assert "refund amount" in msg.lower()

    mock_gateway.refund_payment.assert_not_called()

def test_refund_too_much(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $9.5 processed successfully. Refund ID: refund_123")

    success, msg = refund_late_fee_payment("txn_123", 99.5, mock_gateway)

    assert success == False
    assert "refund amount" in msg.lower()

    mock_gateway.refund_payment.assert_not_called()

def test_refund_zero(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")

    success, msg = refund_late_fee_payment("txn_123", 0, mock_gateway)

    assert success == False
    assert "refund amount" in msg.lower()

    mock_gateway.refund_payment.assert_not_called()

# refund declined by gateway
def test_gateway_declined(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")

    success, msg = refund_late_fee_payment("txn_123", 9.5, mock_gateway)

    assert success == False
    assert "refund failed" in msg.lower()

    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with("txn_123", 9.5)

# network error handling
def test_network_error(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.side_effect = ConnectionError("Something went wrong")

    success, msg = refund_late_fee_payment("txn_123", 9.5, mock_gateway)

    assert success == False
    assert "processing error" in msg.lower()

    mock_gateway.refund_payment.assert_called_once()
    mock_gateway.refund_payment.assert_called_with("txn_123", 9.5)