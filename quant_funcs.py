import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class QuantFuncs:

    def __init__(self):
        self.test = "Hello"

    def drawdown(self, data: pd.DataFrame) -> pd.DataFrame:

        pass

    def returns(self, ticker: str) -> float:

        returns = (yf.download(ticker, start='2015-01-01', end='2022-05-20')["Adj Close"].pct_change() + 1).prod() - 1

        return round(returns * 100, 2)

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

    def get_daily_cumulative_returns_multiple(self, data: list, weights: list) -> pd.DataFrame:

        returns = yf.download(data, start='2015-01-01', end='2022-05-20')['Adj Close']

        rets = pd.DataFrame()
        for i in returns.columns.values:
            rets[f"{i}-rets"] = returns[f"{i}"].pct_change() + 1

        port_pct = []

        for i in range(len(rets)):
            sum_port = 0

            for j, val in enumerate(rets.columns):

                sum_port += (rets[val].iloc[i] * weights[j])

                if i == 4:
                    print(f"{j}: {sum_port}")

            port_pct.append(sum_port)

        cum_port = []

        for i, val in enumerate(port_pct):

            if i == 0:
                cum_port.append(1)

            else:
                cum_port.append(cum_port[i - 1] * val)

        data_port = {"Daily Cumulative Returns": cum_port}

        cum_rets = pd.DataFrame(data_port)

        cum_rets.plot()

        return cum_rets


if __name__ == "__main__":
    q = QuantFuncs()

    aapl = q.get_cumulative_returns('aapl', 1000)

    print(aapl)
