"""Look up song data from Billboard.

    Ex: Billboard Top 100, 2009
"""
from billboard import ChartData


class BillboardRunner:

    def __init__(self):
        pass

    def get(self, year: int, chart: str = "hot-100-songs") -> ChartData:
        return ChartData(chart, year=year)
