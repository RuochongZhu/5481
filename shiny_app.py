from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

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


def _events_to_df(payload: dict) -> pd.DataFrame:
    events = payload.get("events", []) if isinstance(payload, dict) else []
    if not events:
        return pd.DataFrame(
            columns=["id", "magnitude", "place", "time", "latitude", "longitude", "depth_km", "tsunami", "type"]
        )

    df = pd.DataFrame(events)
    keep = ["id", "magnitude", "place", "time", "latitude", "longitude", "depth_km", "tsunami", "type"]
    for col in keep:
        if col not in df.columns:
            df[col] = None
    df = df[keep]
    df["magnitude"] = pd.to_numeric(df["magnitude"], errors="coerce")
    df["depth_km"] = pd.to_numeric(df["depth_km"], errors="coerce")
    return df


def _severity_rows(df: pd.DataFrame) -> list[tuple[str, int, str]]:
    if df.empty or "magnitude" not in df:
        return [("Minor (<4.0)", 0, "#22c55e"), ("Moderate (4.0-5.9)", 0, "#f59e0b"), ("Strong (>=6.0)", 0, "#ef4444")]

    minor = int((df["magnitude"] < 4.0).fillna(False).sum())
    moderate = int(((df["magnitude"] >= 4.0) & (df["magnitude"] < 6.0)).fillna(False).sum())
    strong = int((df["magnitude"] >= 6.0).fillna(False).sum())
    return [("Minor (<4.0)", minor, "#22c55e"), ("Moderate (4.0-5.9)", moderate, "#f59e0b"), ("Strong (>=6.0)", strong, "#ef4444")]


def _time_trend_rows(df: pd.DataFrame) -> list[tuple[str, int]]:
    if df.empty or "time" not in df:
        return []
    ts = pd.to_datetime(df["time"], errors="coerce", utc=True)
    grouped = (
        pd.DataFrame({"d": ts.dt.date})
        .dropna()
        .groupby("d", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("d", ascending=False)
        .head(10)
        .sort_values("d")
    )
    return [(str(row["d"]), int(row["count"])) for _, row in grouped.iterrows()]


today = date.today()
default_start = today - timedelta(days=30)

app_ui = ui.page_fluid(
    ui.tags.style(
        """
        :root { --bg: #0b1020; --panel: #131a2d; --panel-2: #1c2640; --text: #e8ecf8; --muted: #9aa4bf; }
        body { background: radial-gradient(circle at top right, #1c2d5a, #0b1020 45%); color: var(--text); }
        .app-wrap { max-width: 1280px; margin: 0 auto; }
        .hero { background: linear-gradient(135deg, #2563eb, #7c3aed); border-radius: 16px; padding: 20px 24px; margin: 10px 0 16px; }
        .hero h2 { margin: 0; color: #fff; }
        .hero p { margin: 8px 0 0; color: #e5e7eb; }
        .card { background: var(--panel); border: 1px solid #2a365a; border-radius: 14px; }
        .kpi-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 12px; }
        .kpi { background: var(--panel-2); border: 1px solid #314170; border-radius: 12px; padding: 14px; }
        .kpi .label { font-size: 12px; color: var(--muted); }
        .kpi .value { font-size: 24px; font-weight: 700; margin-top: 6px; }
        .bar-wrap { margin: 8px 0 12px; }
        .bar-top { display: flex; justify-content: space-between; font-size: 13px; color: var(--muted); }
        .bar-bg { height: 10px; border-radius: 99px; background: #233154; overflow: hidden; margin-top: 6px; }
        .bar-fill { height: 10px; border-radius: 99px; }
        .status { color: var(--muted); font-size: 13px; margin-bottom: 8px; }
        .viz-box { background: var(--panel); border: 1px solid #2a365a; border-radius: 14px; padding: 12px; }
        .trend-row { display: grid; grid-template-columns: 95px 1fr 40px; gap: 10px; align-items: center; margin: 8px 0; font-size: 13px; }
        .map-wrap { width: 100%; overflow: hidden; border-radius: 12px; border: 1px solid #2a365a; background: linear-gradient(180deg, #0f1d3a, #0b1020); }
        @media (max-width: 900px) { .kpi-row { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
        """
    ),
    ui.div(
        {"class": "app-wrap"},
        ui.div(
            {"class": "hero"},
            ui.h2("Seismic Intel Hub"),
            ui.p("Interactive earthquake dashboard powered by USGS API"),
        ),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_date("starttime", "Start date", value=default_start),
                ui.input_date("endtime", "End date", value=today),
                ui.input_numeric("minmagnitude", "Min magnitude", value=4.0, min=0, max=10, step=0.1),
                ui.input_numeric("limit", "Limit", value=120, min=1, max=500, step=1),
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
                ui.input_switch("auto_refresh", "Auto refresh on filter change", value=True),
                ui.layout_columns(
                    ui.input_action_button("load", "Refresh now", class_="btn-primary"),
                    ui.input_action_button("reset", "Reset filters"),
                    col_widths=[6, 6],
                ),
                open="desktop",
                width=320,
            ),
            ui.div(
                ui.output_text("status_text"),
                ui.output_ui("error_alert"),
                ui.output_ui("kpis"),
                ui.layout_columns(
                    ui.card(ui.card_header("Magnitude mix"), ui.output_ui("severity_bars")),
                    ui.card(ui.card_header("Top locations"), ui.output_data_frame("top_places")),
                    col_widths=[6, 6],
                ),
                ui.layout_columns(
                    ui.card(ui.card_header("Daily trend (last 10 days with events)"), ui.output_ui("trend_bars")),
                    ui.card(ui.card_header("Geo scatter view"), ui.output_ui("geo_map")),
                    col_widths=[6, 6],
                ),
                ui.card(ui.card_header("Earthquake events"), ui.output_data_frame("events_table")),
            ),
        ),
    ),
)


def server(input, output, session):  # noqa: ANN001,ARG001
    refresh_token = reactive.Value(0)
    last_error = reactive.Value("")
    last_success = reactive.Value("")

    @reactive.effect
    def _initial_load():
        if refresh_token.get() == 0:
            refresh_token.set(1)

    @reactive.effect
    @reactive.event(input.load)
    def _manual_refresh():
        refresh_token.set(refresh_token.get() + 1)

    @reactive.effect
    @reactive.event(input.reset)
    def _reset_filters():
        ui.update_date("starttime", value=default_start)
        ui.update_date("endtime", value=today)
        ui.update_numeric("minmagnitude", value=4.0)
        ui.update_numeric("limit", value=120)
        ui.update_select("orderby", selected="time")

    @reactive.effect
    def _auto_refresh_when_filter_changes():
        if not input.auto_refresh():
            return
        input.starttime()
        input.endtime()
        input.minmagnitude()
        input.limit()
        input.orderby()
        refresh_token.set(refresh_token.get() + 1)

    @reactive.calc
    def payload() -> dict:
        refresh_token.get()

        start = input.starttime()
        end = input.endtime()
        if start is None or end is None:
            raise ValueError("Start date and end date are required.")
        if start > end:
            raise ValueError("Start date cannot be later than end date.")

        days = (end - start).days
        if days > 365:
            raise ValueError("Date range is too large. Please keep it within 365 days.")

        result = _fetch_earthquakes(
            starttime=str(start),
            endtime=str(end),
            minmagnitude=float(input.minmagnitude()),
            limit=int(input.limit()),
            orderby=str(input.orderby()),
        )
        last_error.set("")
        last_success.set(datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"))
        return result

    @reactive.calc
    def safe_df() -> pd.DataFrame:
        try:
            data = payload()
            return _events_to_df(data)
        except Exception as exc:  # noqa: BLE001
            last_error.set(str(exc))
            return _events_to_df({})

    @output
    @render.text
    def status_text() -> str:
        err = last_error.get()
        if err:
            return "Status: Error detected. Please adjust filters and retry."
        stamp = last_success.get()
        return f"Status: Live data loaded. Last update: {stamp}" if stamp else "Status: Ready"

    @output
    @render.ui
    def error_alert():
        err = last_error.get()
        if not err:
            return ui.div()
        return ui.div({"class": "alert alert-danger"}, f"Error: {err}")

    @output
    @render.ui
    def kpis():
        try:
            data = payload()
            summary = data.get("summary", {})
            max_mag = summary.get("max_magnitude")
            avg_mag = summary.get("avg_magnitude")
            count = summary.get("count")
            tsunami_count = int(safe_df()["tsunami"].fillna(False).sum()) if not safe_df().empty else 0
        except Exception:  # noqa: BLE001
            max_mag = avg_mag = count = "-"
            tsunami_count = 0

        cards = [
            ("Events", count),
            ("Max Magnitude", max_mag),
            ("Avg Magnitude", avg_mag),
            ("Tsunami Flags", tsunami_count),
        ]
        return ui.div(
            {"class": "kpi-row"},
            *[
                ui.div(
                    {"class": "kpi"},
                    ui.div({"class": "label"}, label),
                    ui.div({"class": "value"}, str(value)),
                )
                for label, value in cards
            ],
        )

    @output
    @render.ui
    def severity_bars():
        df = safe_df()
        rows = _severity_rows(df)
        total = max(len(df), 1)

        return ui.div(
            *[
                ui.div(
                    {"class": "bar-wrap"},
                    ui.div({"class": "bar-top"}, ui.span(name), ui.span(f"{count} ({round(count * 100 / total)}%)")),
                    ui.div(
                        {"class": "bar-bg"},
                        ui.div({"class": "bar-fill", "style": f"width: {count * 100 / total}%; background: {color};"}),
                    ),
                )
                for name, count, color in rows
            ]
        )

    @output
    @render.data_frame
    def top_places():
        df = safe_df()
        if df.empty:
            return render.DataGrid(pd.DataFrame(columns=["place", "count"]), width="100%")
        top = (
            df.assign(place=df["place"].fillna("Unknown"))
            .groupby("place", as_index=False)
            .size()
            .rename(columns={"size": "count"})
            .sort_values("count", ascending=False)
            .head(12)
        )
        return render.DataGrid(top, width="100%")

    @output
    @render.ui
    def trend_bars():
        df = safe_df()
        rows = _time_trend_rows(df)
        if not rows:
            return ui.div({"class": "status"}, "No trend data yet.")
        max_count = max(c for _, c in rows)
        return ui.div(
            *[
                ui.div(
                    {"class": "trend-row"},
                    ui.span(day),
                    ui.div(
                        {"class": "bar-bg"},
                        ui.div(
                            {
                                "class": "bar-fill",
                                "style": f"width: {max(8, int(count * 100 / max_count))}%; background: #60a5fa;",
                            }
                        ),
                    ),
                    ui.span(str(count)),
                )
                for day, count in rows
            ]
        )

    @output
    @render.ui
    def geo_map():
        df = safe_df()
        if df.empty:
            return ui.div({"class": "status"}, "No map data yet.")

        lat = pd.to_numeric(df["latitude"], errors="coerce")
        lon = pd.to_numeric(df["longitude"], errors="coerce")
        mag = pd.to_numeric(df["magnitude"], errors="coerce").fillna(0)
        m = pd.DataFrame({"lat": lat, "lon": lon, "mag": mag}).dropna().head(250)
        if m.empty:
            return ui.div({"class": "status"}, "No valid coordinates.")

        points = []
        for _, row in m.iterrows():
            x = (float(row["lon"]) + 180.0) / 360.0 * 800.0
            y = (90.0 - float(row["lat"])) / 180.0 * 360.0
            r = max(2.0, min(10.0, float(row["mag"]) * 1.6))
            color = "#ef4444" if row["mag"] >= 6.0 else ("#f59e0b" if row["mag"] >= 4.0 else "#22c55e")
            points.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='{color}' fill-opacity='0.65' stroke='white' stroke-width='0.5' />")

        svg = (
            "<svg viewBox='0 0 800 360' width='100%' height='320' xmlns='http://www.w3.org/2000/svg'>"
            "<rect x='0' y='0' width='800' height='360' fill='#0f1d3a'/>"
            "<line x1='0' y1='180' x2='800' y2='180' stroke='#253660' stroke-width='1'/>"
            "<line x1='400' y1='0' x2='400' y2='360' stroke='#253660' stroke-width='1'/>"
            "<line x1='0' y1='90' x2='800' y2='90' stroke='#1d2a4b' stroke-width='1'/>"
            "<line x1='0' y1='270' x2='800' y2='270' stroke='#1d2a4b' stroke-width='1'/>"
            + "".join(points)
            + "</svg>"
        )
        legend = ui.tags.div(
            {"class": "status"},
            "Legend: ",
            ui.tags.span("●", style="color:#22c55e"), " <4.0  ",
            ui.tags.span("●", style="color:#f59e0b"), " 4.0-5.9  ",
            ui.tags.span("●", style="color:#ef4444"), " >=6.0",
        )
        return ui.div({"class": "map-wrap"}, ui.HTML(svg), legend)

    @output
    @render.data_frame
    def events_table():
        df = safe_df()
        if df.empty:
            return render.DataGrid(df, width="100%", filters=True)

        show = df.copy()
        show["magnitude"] = show["magnitude"].round(2)
        show["depth_km"] = show["depth_km"].round(1)
        return render.DataGrid(show, width="100%", filters=True)


app = App(app_ui, server)
