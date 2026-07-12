"""Create neutral chart models from already grouped QueryResult rows."""

from presentation.models.views import ChartSeries, ChartView


class ChartFactory:
    def from_query_result(self, result, chart_id: str, title: str, chart_type: str = "line") -> ChartView:
        if not result.rows or all(row.group is None for row in result.rows):
            return ChartView(chart_id, chart_type, title, empty_state={"title": "Not enough grouped data", "message": "Choose a grouping to display a chart.", "icon_key": "chart"}, accessibility_summary="No grouped chart data is available.")
        values = tuple({"x": row.group, "y": row.values.get("sum", 0)} for row in result.rows)
        return ChartView(chart_id, chart_type, title, (ChartSeries("primary", title, values),), accessibility_summary=f"{len(values)} grouped values are available.")
