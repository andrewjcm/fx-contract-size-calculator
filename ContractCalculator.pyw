#!/usr/bin/env python3

from bs4 import BeautifulSoup
from breezypythongui import EasyFrame
import requests


class ContractSize(EasyFrame):
    """Determines contract size based on max desired risk."""

    def __init__(self):
        """Sets up window and data"""
        EasyFrame.__init__(self, title="Contract Size Calculator")
        self.pairLabel = self.addLabel(text="Pair (6-letter pair code):", row=0, column=0)
        self.pairField = self.addTextField(text="AUDCAD", row=0, column=1)
        self.accountLabel = self.addLabel(text="Account Size $:", row=1, column=0)
        self.accountField = self.addFloatField(value=3500, row=1, column=1)
        self.riskLabel = self.addLabel(text="Risk (% of account):", row=2, column=0)
        self.riskField = self.addIntegerField(value=1, row=2, column=1)
        self.pipsLabel = self.addLabel(text="Pips (Stop Loss):", row=3, column=0)
        self.pipsField = self.addIntegerField(value=25, row=3, column=1)
        self.contractLabel = self.addLabel(text="Contract Size:", row=4, column=0)
        self.contractField = self.addIntegerField(value=0, row=4, column=1, state="disabled")
        self.calcButton = self.addButton(text="Calculate", row=5, column=0, command=self.getContractSize)
        self.perPipLabel = self.addTextField(text="", row=5, column=1, state="disabled")
        self.donateLabel = self.addLabel(text="Donate via PayPal: andy@cmventures.me", row=6, column=1)

    def getContractSize(self):
        """Pulls latest pair data from www.mataf.net and calculates the contact size based on determined inputs"""
        url = "https://www.mataf.net/en/forex/tools/pip-value"
        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, "lxml")
        table = soup.table
        table_rows = table.tbody.find_all("tr")

        pairs_list = []
        for i in range(len(table_rows)):
            for th in table_rows[i].find_all("th"):
                pairs_list.append(th.text)
        pip_val = []
        for i in range(len(table_rows)):
            for td in table_rows[i].find_all("td"):
                pip_val.append(td.text)
        usd_val = []
        for i in range(0, len(pip_val), 3):
            usd_val.append(float(pip_val[i]))

        price_list = dict(zip(pairs_list, usd_val))
        account_size = self.accountField.getNumber()
        pair = self.pairField.getText()
        pip_value = price_list[pair.upper()]
        pips = self.pipsField.getNumber()
        risk = self.riskField.getNumber()/100

        contract_size = ((account_size*risk)/pips)/pip_value
        self.contractField.setNumber(round(contract_size, 2))
        self.perPipLabel.setText("Per Pip Value: ${:,.2f}".format(pip_value*contract_size))
        

def main():
    """Instantiate and pop up the window."""
    ContractSize().mainloop()


if __name__ == "__main__":
    main()
