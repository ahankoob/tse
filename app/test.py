import platform

class Hour:
    ok = "Im feel OK"
    tired = "Im feel Tired"
    def morning(self):
        print(self.ok)

    def evening(self):
        print(self.tired)
def main():
    
    # import pytse_client as tse
    # tickers = tse.download(symbols="all", write_to_csv=True)
    # tickers = tse.all_symbols()
    url = "http://www.tsetmc.com/Loader.aspx?ParTree=111C1417"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")

    table=soup.find_all('table')[0]
    rows=table.find_all('tr')[1:]

    data = {
        'Company' : [],
        'Symbol' : [],
        'id' : []
    }

    for row in rows:
        cols = row.find_all('td')
        data['Company'].append(cols[0].get_text())
        data['Symbol'].append(cols[1].get_text())
        data['id'].append(cols[2].get_text())
    print(data)
if __name__ == "__main__":
    main()