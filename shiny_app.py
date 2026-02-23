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


def _events_df(payload: dict | None) -> pd.DataFrame:
    events = payload.get("events", []) if isinstance(payload, dict) else []
    if not events:
        return pd.DataFrame(columns=["id", "magnitude", "place", "time", "latitude", "longitude", "depth_km"])

    df = pd.DataFrame(events)
    keep = ["id", "magnitude", "place", "time", "latitude", "longitude", "depth_km"]
    for col in keep:
        if col not in df.columns:
            df[col] = None
    out = df[keep].copy()
    out["magnitude"] = pd.to_numeric(out["magnitude"], errors="coerce").round(2)
    out["depth_km"] = pd.to_numeric(out["depth_km"], errors="coerce").round(1)
    return out


today = date.today()
default_start = today - timedelta(days=30)

app_ui = ui.page_fluid(
    ui.h2("Seismic Intel Hub"),
    ui.p("Simple and stable dashboard for Posit Connect Cloud"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_date("starttime", "Start date", value=default_start),
            ui.input_date("endtime", "End date", value=today),
            ui.input_numeric("minmagnitude", "Min magnitude", value=4.0, min=0, max=10, step=0.1),
            ui.input_numeric("limit", "Limit", value=80, min=1, max=200, step=1),
            ui.input_select(
                "orderby",
                "Order by",
                choices={
                    "time": "Latest first",
                    "time-asc": "Oldest first",
                    "magnitude": "Largest first",
                    "magnitude-asc": "Smallest first",
                },
                selected="time",
            ),
            ui.input_action_button("load", "Load data", class_="btn-primary"),
        ),
        ui.card(
            ui.card_header("Status"),
            ui.output_text("status"),
            ui.output_ui("error_box"),
        ),
        ui.layout_columns(
            ui.card(ui.card_header("Summary"), ui.output_ui("summary")),
            ui.card(ui.card_header("Top locations"), ui.output_data_frame("top_places")),
            col_widths=[6, 6],
        ),
        ui.card(ui.card_header("Earthquake events"), ui.output_data_frame("events_table")),
    ),
)


def server(input, output, session):  # noqa: ANN001,ARG001
    @reactive.calc
    @reactive.event(input.load, ignore_none=False)
    def data_bundle() -> dict:
        start = input.starttime()
        end = input.endtime()
        if start is None or end is None:
            return {"error": "Start date and end date are required.", "data": None}
        if start > end:
            return {"error": "Start date cannot be later than end date.", "data": None}

        days = (end - start).days
        if days > 365:
            return {"error": "Date range should be within 365 days.", "data": None}

        try:
            data = _fetch_earthquakes(
                starttime=str(start),
                endtime=str(end),
                minmagnitude=float(input.minmagnitude()),
                limit=int(input.limit()),
                orderby=str(input.orderby()),
            )
            return {"error": "", "data": data}
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc), "data": None}

    @output
    @render.text
    def status() -> str:
        bundle = data_bundle()
        if bundle["error"]:
            return "Status: failed to load data"
        count = bundle["data"].get("summary", {}).get("count", 0) if bundle["data"] else 0
        return f"Status: loaded successfully ({count} events)"

    @output
    @render.ui
    def error_box():
        err = data_bundle()["error"]
        if not err:
            return ui.div()
        return ui.div({"class": "alert alert-danger"}, f"Error: {err}")

    @output
    @render.ui
    def summary():
        bundle = data_bundle()
        data = bundle["data"]
        if not data:
            return ui.p("No data available.")

        s = data.get("summary", {})
        return ui.tags.ul(
            ui.tags.li(f"Count: {s.get('count')}"),
            ui.tags.li(f"Max magnitude: {s.get('max_magnitude')}"),
            ui.tags.li(f"Min magnitude: {s.get('min_magnitude')}"),
            ui.tags.li(f"Avg magnitude: {s.get('avg_magnitude')}"),
        )

    @output
    @render.data_frame
    def top_places():
        df = _events_df(data_bundle()["data"])
        if df.empty:
            return render.DataGrid(pd.DataFrame(columns=["place", "count"]), width="100%")
        top = (
            df.assign(place=df["place"].fillna("Unknown"))
            .groupby("place", as_index=False)
            .size()
            .rename(columns={"size": "count"})
            .sort_values("count", ascending=False)
            .head(10)
        )
        return render.DataGrid(top, width="100%")

    @output
    @render.data_frame
    def events_table():
        df = _events_df(data_bundle()["data"])
        return render.DataGrid(df, width="100%", filters=True)


app = App(app_ui, server)
