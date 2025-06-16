from stock_info import get_stock_codes_names, create_string_with_good_format
def test_format_writer():
    data = {
        "Name": ["tet", "test"],
        "Code": ["RTW", "AGH"],
        "Shares": ["20022", "13424"],
        "Date Reported": ["21344 mr 2222", "fkoaww"],
        "% Out": ["12%", "41%"],
        "Value": ["122", "5551"],
    }
    title = 'Test Title'

    predicted_output = """======================Test Title========================
        | Name | Code | Shares | Date Reported | % Out | Value |
        --------------------------------------------------------
        | tet  | RTW  | 20022  | 21344 mr 2222 | 12%   | 122   | 
        | test | AGH  | 13424  | fkoaww        | 41%   | 5551  | 
        --------------------------------------------------------
        """

    assert create_string_with_good_format(data, title) == predicted_output

def test_codes_names_getter():
    assert 'NVDA' in get_stock_codes_names()