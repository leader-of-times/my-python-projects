import json
import os
import pytest
from unittest.mock import patch, mock_open
from project import (
    admin, display_data, display_specific_data, add_new, delete_prod,
    update_prod_data, display_reports_admin, user, search_prod,
    search_prod_cat, purchase_product, main
)

# Test data
mock_data = {
    "1001": {"name": "avocado", "price": 230, "category": "grocery", "quantity": 10, "date": "10/03/2021"},
    "1002": {"name": "lotion", "price": 250, "category": "beauty & personal", "quantity": 100, "date": "15/07/2021"},
    "1003": {"name": "pain reliever", "price": 500, "category": "health", "quantity": 200, "date": "12/04/2021"},
}

# Helper function to write mock data to data.json
def write_mock_data():
    with open("data.json", 'w') as fd:
        json.dump(mock_data, fd)

# Write initial data
write_mock_data()

# Helper function to read data from data.json
def read_data():
    with open("data.json", 'r') as fd:
        return json.load(fd)

# Test display_data
def test_display_data(capsys):
    write_mock_data()
    display_data()
    captured = capsys.readouterr()
    assert "avocado" in captured.out
    assert "lotion" in captured.out

# Test display_specific_data
@patch('builtins.input', return_value="1001")
def test_display_specific_data(mock_input, capsys):
    write_mock_data()
    display_specific_data()
    captured = capsys.readouterr()
    assert "avocado" in captured.out

# Test add_new
@patch('builtins.input', side_effect=["1004", "banana", "50", "grocery", "100", "01/01/2022"])
def test_add_new(mock_input):
    write_mock_data()
    add_new()
    data = read_data()
    assert "1004" in data
    assert data["1004"]["name"] == "banana"

# Test delete_prod
@patch('builtins.input', return_value="1001")
def test_delete_prod(mock_input):
    write_mock_data()
    delete_prod()
    data = read_data()
    assert "1001" not in data

# Test update_prod_data
@patch('builtins.input', side_effect=["1002", "0", "shampoo", "300", "beauty & personal", "150", "01/01/2022"])
def test_update_prod_data(mock_input):
    write_mock_data()
    update_prod_data()
    data = read_data()
    assert data["1002"]["name"] == "shampoo"

# Test display_reports_admin
@patch('builtins.input', return_value="0")
def test_display_reports_admin(mock_input, capsys):
    user_data = {
        "user1": {
            "1234": {
                "time_date": "2021-12-01 12:00:00",
                "name": "avocado",
                "product_id": "1001",
                "quantity": 2,
                "price": 460
            }
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(user_data))):
        display_reports_admin()
        captured = capsys.readouterr()
        assert "user1" in captured.out

# Test search_prod
@patch('builtins.input', return_value="avocado")
def test_search_prod(mock_input, capsys):
    write_mock_data()
    search_prod()
    captured = capsys.readouterr()
    assert "avocado" in captured.out

# Test search_prod_cat
@patch('builtins.input', return_value="grocery")
def test_search_prod_cat(mock_input, capsys):
    write_mock_data()
    search_prod_cat()
    captured = capsys.readouterr()
    assert "avocado" in captured.out

# Test purchase_product
@patch('builtins.input', side_effect=["user1", "1001", "2", "1"])
def test_purchase_product(mock_input, capsys):
    write_mock_data()
    purchase_product()
    captured = capsys.readouterr()
    assert "Total Amount Payable" in captured.out

# Test main menu
@patch('builtins.input', side_effect=["3"])
@patch('sys.exit', side_effect=SystemExit)
def test_main_menu(mock_input, mock_exit):
    with pytest.raises(SystemExit):
        main()
