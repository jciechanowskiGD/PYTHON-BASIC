"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

# step 1. getting stocks info (Code, Name) from https://finance.yahoo.com/most-active .
# step 2. getting https://finance.yahoo.com/quote/{code}/profile/ and parsing ceo name and age, (emplyees and country on same page)
# step 3. getting https://finance.yahoo.com/quote/{code}/key-statistics/ and parsing 52 week change, and getting rest of info (same page)
# step 4. getting    and parsing needed info (looking how much blackrock stake is worth)
import requests
from bs4 import BeautifulSoup
from http import cookiejar
import heapq

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"


class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = (
        lambda self, *args, **kwargs: False
    )
    netscape = True
    rfc2965 = hide_cookie2 = False


def make_request(url: str):
    page = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    if page.status_code == 200:
        return BeautifulSoup(page.content, "html.parser")
    else:
        print("Request doesnt work")
        print(page.content)
        raise Exception("Request doesnt work")


# I will hardcode url because it wont work on any other site either way
def get_stock_codes_names() -> dict:
    soup = make_request("https://finance.yahoo.com/most-active")
    rows = soup.find_all("tr", class_="row yf-1570k0a")
    codes_names = {}
    for row in rows:
        symbol = row.find("span", class_="symbol yf-1jsynna")
        name = row.find(
            "div", class_="leftAlignHeader companyName yf-362rys enableMaxWidth"
        )
        codes_names[symbol.text.rstrip()] = name.text.rstrip()

    return codes_names


def get_stocks_with_youngest_ceo(stock_codes_names: dict) -> dict:
    data = {
        "Name": [],
        "Code": [],
        "Country": [],
        "Employees": [],
        "CEO Name": [],
        "CEO Age": [],
    }
    age_heap = []
    for code in stock_codes_names:
        data["Name"] = stock_codes_names[code]
        data["Code"] = code

        soup = make_request(f"https://finance.yahoo.com/quote/{code}/profile/")
        row = soup.find("tr", class_="yf-mj92za")
        row = row.find_all("td", class_="yf-mj92za")

        name = row[0].text.rstrip()
        age = int(row[-1].text.rstrip())
        data["CEO Name"].append(name)
        data["CEO Age"].append(age)

        company_stats = soup.find("dl", class_="company-stats yf-wxp4ja")
        data["Employees"].append(company_stats.find("strong").text)

        address = soup.find("div", class_="address yf-wxp4ja")
        data["Country"].append(address.find_all("div")[-1].text)

        # heap of 5 smallest ceo ages. In python its min heap and I need max heap thats why -1
        if len(age_heap) < 5:
            heapq.heappush(age_heap, -1 * age)
        elif -1 * age_heap[0] > age:
            heapq.heappushpop(age_heap, age)

    indexes = []
    heap_len = len(age_heap)
    for _ in range(heap_len):
        age = heapq.pop(age_heap)
        indexes.append(data["CEO Age"].index(age))

    final_data = {
        "Name": [],
        "Code": [],
        "Country": [],
        "Employees": [],
        "CEO Name": [],
        "CEO Age": [],
    }
    for i in reversed(indexes):
        final_data["Name"].append(data["Name"][i])
        final_data["Code"].append(data["Code"][i])
        final_data["Country"].append(data["Country"][i])
        final_data["Employees"].append(data["Employees"][i])
        final_data["CEO Name"].append(data["CEO Name"][i])
        final_data["CEO Age"].append(data["CEO Age"][i])

    return final_data


def get_stocks_with_biggest_gain(stock_codes_names: dict) -> dict:
    data = {
        "Name": [],
        "Code": [],
        "52-Week Change": [],
        "Total Cash": [],
    }
    change_heap = []
    for code in stock_codes_names:
        data["Name"] = stock_codes_names[code]
        data["Code"] = code

        soup = make_request(f"https://finance.yahoo.com/quote/{code}/key-statistics/")
        trading_info = soup.find_all("section", class_="yf-14j5zka")[1]
        row_52_week = trading_info.find_all("tr", class_="row yf-vaowmx")[1]
        change_52_week = float(
            row_52_week.find("td", class_="value yf-vaowmx").text.rstrip()[:-1]
        )
        data["52-Week Change"].append(change_52_week)

        financial_info = soup.find_all("section", class_="yf-14j5zka")[0]
        balance_sheet = financial_info.find_all(
            "section", class_="card small tw-p-0 yf-ispmdb sticky noBackGround"
        )[4]
        total_cash = balance_sheet.find("td", class_="value yf-vaowmx").text.rstrip()
        data["Total Cash"].append(total_cash)

        if len(change_heap) < 10:
            heapq.heappush(change_heap, change_52_week)
        elif change_heap[0] < change_52_week:
            heapq.heappushpop(change_heap, change_52_week)

    indexes = []
    heap_len = len(change_heap)
    for _ in range(heap_len):
        change_52_week = heapq.pop(change_heap)
        indexes.append(data["52-Week Change"].index(change_52_week))

    final_data = {
        "Name": [],
        "Code": [],
        "52-Week Change": [],
        "Total Cash": [],
    }

    for i in reversed(indexes):
        final_data["Name"].append(data["Name"][i])
        final_data["Code"].append(data["Code"][i])
        final_data["52-Week Change"].append(str(data["52-Week Change"][i]) + "%")
        final_data["Total Cash"].append(data["Total Cash"][i])

    return final_data


def get_blackrock_holds(stock_codes_names: dict) -> dict:
    data = {
        "Name": [],
        "Code": [],
        "Shares": [],
        "Date Reported": [],
        "% Out": [],
        "Value": [],
    }
    value_heap = []
    for code in stock_codes_names:
        soup = make_request(f"https://finance.yahoo.com/quote/{code}/holders/")
        top_institutional_holders = soup.find(
            "section", attrs={"data-testid": "holders-top-institutional-holders"}
        )
        rows = top_institutional_holders.find_all("tr", class_="yf-idy1mk")

        for row in rows:
            if row.find("td", class_="yf-idy1mk").text.rstrip() != "Blackrock Inc.":
                continue

            data["Name"] = stock_codes_names[code]
            data["Code"] = code
            data["Shares"] = row.find_all("td", class_="yf-idy1mk")[1].text
            data["Date Reported"] = row.find_all("td", class_="yf-idy1mk")[2].text
            data["% Out"] = row.find_all("td", class_="yf-idy1mk")[3].text
            value = int(
                row.find_all("td", class_="yf-idy1mk")[4].text.replace(",", "")
            )
            data["Value"] = value

            if len(value_heap) < 10:
                heapq.heappush(value_heap, value)
            elif value_heap[0] < value:
                heapq.heappushpop(value_heap, value)
            break

    indexes = []
    heap_len = len(value_heap)
    for _ in range(heap_len):
        value = heapq.pop(value_heap)
        indexes.append(data["52-Week Change"].index(value))

    final_data = {
        "Name": [],
        "Code": [],
        "Shares": [],
        "Date Reported": [],
        "% Out": [],
        "Value": [],
    }

    for i in reversed(indexes):
        final_data["Name"].append(data["Name"][i])
        final_data["Code"].append(data["Code"][i])
        final_data["Shares"].append(data["Shares"][i])
        final_data["Date Reported"].append(data["Date Reported"][i])
        final_data["% Out"].append(data["% Out"][i])
        final_data["Value"].append(str(data["Value"][i]))

    return final_data


def create_string_with_good_format(info_to_include: dict, title: str) -> str:
    lens = [len(k) if len(k) > len(v) else len(v) for k, v in info_to_include.items()]
    total_len = sum(lens) + 4 + (len(info_to_include) - 1) * 3

    # building string
    title_index = (total_len - len(title)) // 2
    title_string = "=" * (title_index-1) + title + "=" * (total_len - (title_index+len(title)) + 1) + "\n"
    column_names = "|"
    for length, key in zip(lens, info_to_include):
        column_names += " " + key + " " * (length - len(key)) + " |"
    column_names += "\n"
    column_separator = "-" * total_len + '\n'
    value_rows = ""
    for i in range(len(next(iter(info_to_include.values())))):
        value_rows += "| "
        for length,k in zip(lens, info_to_include):
            
            value_rows += (
                info_to_include[k][i]
                + " " * (length - len(info_to_include[k][i]))
                + " | "
            )
        value_rows += "\n"

    return (
        title_string + column_names + column_separator + value_rows + column_separator
    )


if __name__ == "__main__":
    codes_names = get_stock_codes_names()
    print(codes_names)
    data = {
        "Name": ["tet", "test"],
        "Code": ["RTW", "AGH"],
        "Shares": ["20022", "13424"],
        "Date Reported": ["21344 mr 2222", "fkoaww"],
        "% Out": ["12%", "41%"],
        "Value": ["122", "5551"],
    }
    title = 'Test Title'
    print(create_string_with_good_format(data,title))
    # youngest_ceo = get_stocks_with_youngest_ceo(codes_names)
    # biggest_gain = get_stocks_with_biggest_gain(codes_names)
    # blackrock_holding = get_blackrock_holds(codes_names)

    # print(create_string_with_good_format(youngest_ceo, "5 stocks with most youngest CEOs"))
    # print(create_string_with_good_format(biggest_gain, "10 with biggest week"))
    # print(create_string_with_good_format(blackrock_holding, "10 biggest blackrock holdings"))
