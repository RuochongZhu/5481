from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
from shiny import App, reactive, render, ui

from app.providers.factory import get_provider


def _fetch_earthquakes(
    *,
    starttime: str,
    endtime: str,
    minmagnitude: float,
    limit: int,
    orderby: str,
) -> dict:
    provider = get_provider("usgs")
    return provider.fetch_events(
        starttime=starttime,
        endtime=endtime,
        minmagnitude=minmagnitude,
        limit=limit,
        orderby=orderby,
    )


today = date.today()
default_start = today - timedelta(days=30)

app_ui = ui.page_fluid(
    ui.h2("Seismic Intel Hub (Shiny)"),
    ui.p("USGS Earthquake Catalog API dashboard for Posit Connect Cloud"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_date("starttime", "Start date", value=default_start),
            ui.input_date("endtime", "End date", value=today),
            ui.input_numeric("minmagnitude", "Min magnitude", value=4.0, min=0, max=10, step=0.1),
            ui.input_numeric("limit", "Limit", value=100, min=1, max=500, step=1),
            ui.input_select(
                "orderby",
                "Order by",
                choices={
                    "time": "time",
                    "time-asc": "time-asc",
                    "magnitude": "magnitude",
                    "magnitude-asc": "magnitude-asc",
                },
                selected="time",
            ),
            ui.input_action_button("load", "Load earthquakes"),
        ),
        ui.card(
            ui.h4("Summary"),
            ui.output_ui("summary"),
        ),
        ui.card(
            ui.h4("Events"),
            ui.output_data_frame("events_table"),
        ),
    ),
)


def server(input, output, session):  # noqa: ANN001,ARG001
    @reactive.calc
    @reactive.event(input.load)
    def quake_data() -> dict:
        return _fetch_earthquakes(
            starttime=str(input.starttime()),
            endtime=str(input.endtime()),
            minmagnitude=float(input.minmagnitude()),
            limit=int(input.limit()),
            orderby=str(input.orderby()),
        )

    @output
    @render.ui
    def summary():
        try:
            data = quake_data()
        except Exception as exc:  # noqa: BLE001
            return ui.p(f"Failed to load data: {exc}")

        s = data.get("summary", {})
        return ui.tags.ul(
            ui.tags.li(f"Count: {s.get('count')}"),
            ui.tags.li(f"Max magnitude: {s.get('max_magnitude')}"),
            ui.tags.li(f"Min magnitude: {s.get('min_magnitude')}"),
            ui.tags.li(f"Avg magnitude: {s.get('avg_magnitude')}"),
        )

    @output
    @render.data_frame
    def events_table():
        try:
            events = quake_data().get("events", [])
            if not events:
                return render.DataGrid(pd.DataFrame(columns=["id", "magnitude", "place", "time"]))
            df = pd.DataFrame(events)[
                [
                    "id",
                    "magnitude",
                    "place",
                    "time",
                    "latitude",
                    "longitude",
                    "depth_km",
                    "tsunami",
                    "type",
                ]
            ]
            return render.DataGrid(df, width="100%")
        except Exception as exc:  # noqa: BLE001
            err_df = pd.DataFrame([{"error": str(exc)}])
            return render.DataGrid(err_df, width="100%")


app = App(app_ui, server)
