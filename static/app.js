const state = { charts: {} };
const $ = (id) => document.getElementById(id);

function initDateInputs() {
  const end = new Date();
  const start = new Date();
  start.setDate(end.getDate() - 30);
  $("endtime").value = end.toISOString().slice(0, 10);
  $("starttime").value = start.toISOString().slice(0, 10);
}

function format2(v) {
  return Number.isFinite(v) ? v.toFixed(2) : "--";
}

function normalizeDate(iso) {
  if (!iso) return "N/A";
  return iso.replace("T", " ").replace("Z", "").slice(0, 19);
}

function buildParams() {
  return new URLSearchParams({
    starttime: $("starttime").value,
    endtime: $("endtime").value,
    minmagnitude: $("minmagnitude").value,
    limit: $("limit").value,
    orderby: $("orderby").value,
    provider: "usgs",
  });
}

async function loadData() {
  const params = buildParams();
  const url = `/api/v1/earthquakes?${params.toString()}`;
  $("requestUrl").textContent = `${window.location.origin}${url}`;
  $("statusText").textContent = "Requesting...";

  try {
    const res = await fetch(url);
    const payload = await res.json();
    $("jsonOutput").textContent = JSON.stringify(payload, null, 2);
    if (!res.ok) throw new Error(payload.error || "Request failed");
    render(payload);
    $("statusText").textContent = `OK · ${payload.summary.count} events`;
  } catch (error) {
    $("statusText").textContent = `Error: ${error.message}`;
  }
}

function render(payload) {
  const events = payload.events || [];
  const summary = payload.summary || {};

  $("kpiCount").textContent = summary.count ?? "--";
  $("kpiMax").textContent = format2(summary.max_magnitude);
  $("kpiAvg").textContent = format2(summary.avg_magnitude);
  $("kpiTsunami").textContent = events.filter((e) => e.tsunami).length;

  renderTable(events);
  renderCharts(events);
}

function renderTable(events) {
  const table = $("eventsTable");
  table.innerHTML = "";
  events.slice(0, 60).forEach((event) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${normalizeDate(event.time)}</td>
      <td>${format2(event.magnitude)}</td>
      <td>${event.place || "Unknown"}</td>
      <td>${format2(event.depth_km)}</td>
      <td><span class="badge ${event.tsunami ? "on" : "off"}">${event.tsunami ? "YES" : "NO"}</span></td>
    `;
    table.appendChild(row);
  });
}

function upsertChart(key, config) {
  if (state.charts[key]) state.charts[key].destroy();
  state.charts[key] = new Chart(document.getElementById(key).getContext("2d"), config);
}

function renderCharts(events) {
  const magBins = { "4-5": 0, "5-6": 0, "6-7": 0, "7+": 0 };
  const byDate = {};

  for (const e of events) {
    const m = e.magnitude ?? 0;
    if (m < 5) magBins["4-5"] += 1;
    else if (m < 6) magBins["5-6"] += 1;
    else if (m < 7) magBins["6-7"] += 1;
    else magBins["7+"] += 1;

    const day = (e.time || "").slice(0, 10);
    if (day) byDate[day] = (byDate[day] || 0) + 1;
  }

  upsertChart("magChart", {
    type: "bar",
    data: {
      labels: Object.keys(magBins),
      datasets: [{ label: "Count", data: Object.values(magBins), backgroundColor: ["#65d8ff", "#87b9ff", "#9b6dff", "#ff7aa8"], borderRadius: 8 }],
    },
    options: baseOptions(),
  });

  const labels = Object.keys(byDate).sort();
  upsertChart("timeChart", {
    type: "line",
    data: {
      labels,
      datasets: [{ label: "Quakes / Day", data: labels.map((d) => byDate[d]), borderColor: "#65d8ff", backgroundColor: "rgba(101,216,255,.2)", fill: true, tension: .3 }],
    },
    options: baseOptions(),
  });
}

function baseOptions() {
  return {
    maintainAspectRatio: false,
    responsive: true,
    plugins: { legend: { labels: { color: "#e8ebff" } } },
    scales: {
      x: { grid: { color: "rgba(255,255,255,.07)" }, ticks: { color: "#9ea7c5" } },
      y: { grid: { color: "rgba(255,255,255,.07)" }, ticks: { color: "#9ea7c5" } },
    },
  };
}

function boot() {
  initDateInputs();
  $("refreshBtn").addEventListener("click", loadData);
  loadData();
}

document.addEventListener("DOMContentLoaded", boot);
