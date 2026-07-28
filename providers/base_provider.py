from abc import ABC, abstractmethod
import pandas as pd


class BaseProvider(ABC):
    """
    모든 데이터 공급자가 따라야 하는 기본 인터페이스
    """

    @abstractmethod
    def get_etf_list(self) -> pd.DataFrame:
        """ETF 목록 조회"""
        pass

    @abstractmethod
    def get_price(self, ticker: str,
                  start_date: str,
                  end_date: str) -> pd.DataFrame:
        """가격 데이터 조회"""
        pass