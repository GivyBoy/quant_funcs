
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class QuantFuncs:

    def __init__(self):
        self.test = "Hello"

    def drawdown(self, data):

        pass

    def get_cumulative_returns(self, ticker: str, investment: int) -> pd.DataFrame:

        returns = yf.download(ticker, start='2015-01-01', end='2022-05-20')
        print("done")
        returns["Rets"] = returns["Adj Close"].pct_change() + 1

        cum_ret = []
        for i in range(len(returns)):

            if i == 0:
                cum_ret.append(investment)
            else:
                cum_ret.append(cum_ret[i - 1] * returns["Rets"][i])

        holder = {"Cumulative Rets": cum_ret}

        df = pd.DataFrame(data=holder)

        return df


if __name__ == "__main__":

    q = QuantFuncs()

    aapl = q.get_cumulative_returns('aapl', 1000)

    print(aapl)

