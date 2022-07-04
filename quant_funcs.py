import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from PyEMD import EMD, EEMD, CEEMDAN


class Metrics:

    def __init__(self):
        pass

    def drawdown(self, data: pd.DataFrame) -> pd.DataFrame:

        pass

    def returns(self, ticker: str, start: str, end: str) -> float:

        returns = (yf.download(ticker, start=start, end=end)["Adj Close"].pct_change() + 1).prod() - 1

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

        df = pd.DataFrame(data=holder) - 1

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

        cum_rets = pd.DataFrame(data_port) - 1

        cum_rets.plot()

        return cum_rets


class TimeSeriesDecomposition:

    def __init__(self, data: pd.DataFrame):
        """
        :param data: the closing price of a stock (or any time series - the plots will not work without dates)
        """
        self.data = data

    def get_EMD(self) -> tuple[np.ndarray, np.ndarray]:
        """
        This functions uses the Empirical Mode Decomposition (EMD) Algorithm
        It decomposes the stock price into a set of oscillator components called Intrinsic Mode Functions

        :returns:
        IMFs : numpy array
            All the Intrinsic Mode Functions that make up the original stock price
        residue : numpy array
            The residue from the recently analyzed stock price
        """
        data_np = self.data.to_numpy()

        emd = EMD()
        emd.extrema_detection = "parabol"
        emd.emd(data_np)
        IMFs, residue = emd.get_imfs_and_residue()

        nIMFs = IMFs.shape[0]

        plt.figure(figsize=(15, 10))
        plt.subplot(nIMFs + 2, 1, 1)

        plt.plot(self.data, 'r')

        plt.subplot(nIMFs + 2, 1, nIMFs + 2)
        plt.plot(self.data.index, residue)
        plt.ylabel("Residue")

        for n in range(nIMFs):
            plt.subplot(nIMFs + 2, 1, n + 2)
            plt.plot(self.data.index, IMFs[n], 'g')
            plt.ylabel(f"eIMF %{(n + 1)}")
            plt.locator_params(axis='y', nbins=4)

        plt.tight_layout()
        plt.show()

        return IMFs, residue

    def get_EEMD_residue(self) -> tuple[np.ndarray, np.ndarray]:
        """
        This functions uses the Ensemble Empirical Mode Decomposition (EMD) Algorithm
        It decomposes the stock price into a set of oscillator components called Intrinsic Mode Functions
        More robust than the EMD Algorithm

        :returns:
        IMFs : numpy array
            All the Intrinsic Mode Functions that make up the original stock price
        residue : numpy array
            The residue from the recently analyzed stock price
        """

        data_np = self.data.to_numpy()

        eemd = EEMD()
        eemd.extrema_detection = "parabol"
        eemd.eemd(data_np)
        IMFs, residue = eemd.get_imfs_and_residue()

        nIMFs = IMFs.shape[0]

        plt.figure(figsize=(18, 12))
        plt.subplot(nIMFs + 2, 1, 1)

        plt.plot(self.data, 'r')

        plt.subplot(nIMFs + 2, 1, nIMFs + 2)
        plt.plot(self.data.index, residue)
        plt.ylabel("Residue")

        for n in range(nIMFs):
            plt.subplot(nIMFs + 2, 1, n + 2)
            plt.plot(self.data.index, IMFs[n], 'g')
            plt.ylabel(f"eIMF %{(n + 1)}")
            plt.locator_params(axis='y', nbins=4)

        plt.tight_layout()
        plt.show()

        return IMFs, residue

    def get_CEEMD_residue(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Complete Ensemble EMD with Adaptive Noise (CEEMDAN) performs an EEMD
        The difference is that the information about the noise is shared among all workers

        :return:
        IMFs : numpy array
            All the Intrinsic Mode Functions that make up the original stock price
        residue : numpy array
            The residue from the recently analyzed stock price
        """

        data_np = self.data.to_numpy()

        ceemd = CEEMDAN()
        ceemd.extrema_detection = "parabol"
        ceemd.ceemdan(data_np)
        IMFs, residue = ceemd.get_imfs_and_residue()

        nIMFs = IMFs.shape[0]

        plt.figure(figsize=(18, 12))
        plt.subplot(nIMFs + 2, 1, 1)

        plt.plot(self.data, 'r')

        plt.subplot(nIMFs + 2, 1, nIMFs + 2)
        plt.plot(self.data.index, residue)
        plt.ylabel("Residue")

        for n in range(nIMFs):
            plt.subplot(nIMFs + 2, 1, n + 2)
            plt.plot(self.data.index, IMFs[n], 'g')
            plt.ylabel(f"eIMF %{(n + 1)}")
            plt.locator_params(axis='y', nbins=4)

        plt.tight_layout()
        plt.show()

        return IMFs, residue

    def plot_IMFs(self, IMFs: np.ndarray, residue: np.ndarray, num_IMFs: int):
        """
        This function aims to reconstruct the Time Series using the IMFs

        :param IMFs: The IMFs returned from using any of the decomposition functions above
        :param residue: The residue returned from using any of the decomposition functions above
        :param num_IMFs: The number of IMFs you want to reconstruct your data. A value of 2 means the last two IMFs
        :return: None
        """

        sum_IMFs = sum(IMFs[-num_IMFs:])
        sum_IMFs += residue

        plt.figure(figsize=(12, 10))
        plt.plot(self.data.index, self.data, label="Stock Price")
        plt.plot(self.data.index, sum_IMFs, label=f"Last {num_IMFs} IMFs")
        plt.legend(loc="upper left")
        plt.show()


if __name__ == "__main__":
    q = Metrics()

    rets = q.returns('xom', "2015-01-01", "2022-06-10")
    cum_ret = q.get_cumulative_returns("xom", 1000)

    print(f"{rets}-{cum_ret}")



