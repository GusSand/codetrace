from typing import TypeAlias
__typ0 : TypeAlias = "QChartView"
__typ1 : TypeAlias = "PieChartData"
from PyQt5.QtChart import QChartView, QBarSeries, QBarSet, \
    QBarCategoryAxis, QChart, QLegend
from PyQt5.QtGui import QPainter
from analyze.stats import PieChartData
from config import Config


class Chart:
    def __tmp3(__tmp2, config: <FILL>, chart_view: __typ0) -> None:
        __tmp2.chart_view = chart_view
        __tmp2.config = config
        __tmp2.initialized = False

        chart_view.setRenderHint(QPainter.Antialiasing)
        __tmp2.chart: QChart = chart_view.chart()
        legend: QLegend = __tmp2.chart.legend()
        legend.hide()

        __tmp2.chart_view.repaint()

    def __tmp0(__tmp2, __tmp1: __typ1) -> None:
        # series = QPieSeries()
        # for project, duration in chart_data.data.items():
        #   series.append("{} ({} s)".format(project, int(duration)), duration)
        # self.chart_view.setRenderHint(QPainter.Antialiasing)
        # self.chart_view.chart().removeAllSeries()
        # self.chart_view.chart().addSeries(series)

        # TODO redo with stacked bar chart
        series = QBarSeries()
        bar_set = QBarSet('Default')
        categories = []
        for project, duration in __tmp1.data.items():
            if project == __tmp2.config.projects.none_project:
                project = 'None'
            categories.append(project)
            bar_set.append(duration)
        series.append(bar_set)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)

        __tmp2.chart.removeAllSeries()
        __tmp2.chart.addSeries(series)
        __tmp2.chart.setAxisX(axis_x)
        series.attachAxis(axis_x)

        __tmp2.initialized = True

    def reload_config(__tmp2, config: Config) -> None:
        __tmp2.config = config
