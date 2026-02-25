from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
from shiny import App, reactive, render, ui

from app.providers.factory import get_provider

USGS_PROVIDER = get_provider("usgs")


def _fetch_earthquakes(
    *,
    starttime: str,
    endtime: str,
    minmagnitude: float,
    limit: int,
    orderby: str,
) -> dict:
    return USGS_PROVIDER.fetch_events(
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


def _time_window_dates(window_key: str) -> tuple[date, date]:
    end = date.today()
    mapping = {"1d": 1, "7d": 7, "14d": 14, "30d": 30}
    days = mapping.get(window_key, 30)
    start = end - timedelta(days=days)
    return start, end


def _region_ranges(region_key: str) -> tuple[float, float, float, float]:
    # min_lat, max_lat, min_lon, max_lon
    regions = {
        "global": (-90.0, 90.0, -180.0, 180.0),
        "pacific_ring": (-60.0, 65.0, -180.0, -70.0),
        "north_america": (5.0, 75.0, -170.0, -50.0),
        "east_asia": (-10.0, 60.0, 90.0, 170.0),
        "mediterranean": (20.0, 50.0, -10.0, 45.0),
    }
    return regions.get(region_key, regions["global"])


def _apply_geo_filter(df: pd.DataFrame, region_key: str) -> pd.DataFrame:
    if df.empty:
        return df
    min_lat, max_lat, min_lon, max_lon = _region_ranges(region_key)
    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    mask = (lat >= min_lat) & (lat <= max_lat) & (lon >= min_lon) & (lon <= max_lon)
    return df[mask.fillna(False)].copy()


app_ui = ui.page_fluid(
    ui.h2("Seismic Intel Hub"),
    ui.p("Simple and stable dashboard for Posit Connect Cloud"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "time_window",
                "Time range",
                choices={
                    "1d": "Last 1 day",
                    "7d": "Last 7 days",
                    "14d": "Last 14 days",
                    "30d": "Last 30 days",
                },
                selected="30d",
            ),
            ui.input_select(
                "region",
                "Latitude/Longitude range",
                choices={
                    "global": "Global (-90~90, -180~180)",
                    "pacific_ring": "Pacific Ring",
                    "north_america": "North America",
                    "east_asia": "East Asia",
                    "mediterranean": "Mediterranean",
                },
                selected="global",
            ),
            ui.input_select(
                "minmagnitude",
                "Min magnitude",
                choices={"3.0": ">= 3.0", "4.0": ">= 4.0", "5.0": ">= 5.0"},
                selected="4.0",
            ),
            ui.input_select(
                "limit",
                "Limit",
                choices={"30": "30", "50": "50", "80": "80"},
                selected="50",
            ),
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
        try:
            start, end = _time_window_dates(str(input.time_window()))
            data = _fetch_earthquakes(
                starttime=str(start),
                endtime=str(end),
                minmagnitude=float(str(input.minmagnitude())),
                limit=int(str(input.limit())),
                orderby=str(input.orderby()),
            )
            return {"error": "", "data": data}
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc), "data": None}

    @reactive.calc
    def events_df() -> pd.DataFrame:
        return _events_df(data_bundle()["data"])

    @reactive.calc
    def filtered_df() -> pd.DataFrame:
        return _apply_geo_filter(events_df(), str(input.region()))

    @reactive.calc
    def magnitude_stats() -> tuple[float | None, float | None, float | None]:
        df = filtered_df()
        if df.empty:
            return None, None, None
        mags = pd.to_numeric(df["magnitude"], errors="coerce").dropna()
        if mags.empty:
            return None, None, None
        return float(mags.max()), float(mags.min()), round(float(mags.mean()), 2)

    @output
    @render.text
    def status() -> str:
        bundle = data_bundle()
        if bundle["error"]:
            return "Status: failed to load data"
        df = filtered_df()
        count = len(df)
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

        df = filtered_df()
        max_mag, min_mag, avg_mag = magnitude_stats()
        return ui.tags.ul(
            ui.tags.li(f"Count: {len(df)}"),
            ui.tags.li(f"Max magnitude: {max_mag}"),
            ui.tags.li(f"Min magnitude: {min_mag}"),
            ui.tags.li(f"Avg magnitude: {avg_mag}"),
        )

    @output
    @render.data_frame
    def top_places():
        df = filtered_df()
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
        return render.DataGrid(filtered_df(), width="100%")


app = App(app_ui, server)
