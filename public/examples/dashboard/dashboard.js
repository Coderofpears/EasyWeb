const activity = [
  { day: "Mon", value: 46 },
  { day: "Tue", value: 62 },
  { day: "Wed", value: 54 },
  { day: "Thu", value: 81 },
  { day: "Fri", value: 72 },
  { day: "Sat", value: 42 },
  { day: "Sun", value: 66 },
];

const updates = [
  { type: "content", title: "A new field note was published", detail: "Field Notes / 18 minutes ago", value: "+2.8k views" },
  { type: "community", title: "Community replies are up this week", detail: "Signal / 42 minutes ago", value: "+24%" },
  { type: "product", title: "The new onboarding path is live", detail: "Northstar / 1 hour ago", value: "shipped" },
];

const chart = document.querySelector("#activity-chart");
const list = document.querySelector("#activity-list");
const filter = document.querySelector("#activity-filter");
const refresh = document.querySelector("#refresh-button");

function renderChart() {
  chart.replaceChildren(...activity.map((item) => {
    const column = document.createElement("div");
    column.className = "chart-column";
    const bar = document.createElement("div");
    bar.className = "chart-bar";
    bar.style.height = `${item.value}%`;
    bar.title = `${item.day}: ${item.value} activity points`;
    const label = document.createElement("span");
    label.className = "chart-label";
    label.textContent = item.day;
    column.append(bar, label);
    return column;
  }));
}

function renderUpdates() {
  const selected = filter.value;
  const visible = selected === "all" ? updates : updates.filter((item) => item.type === selected);
  list.replaceChildren(...visible.map((item) => {
    const row = document.createElement("div");
    row.className = "activity-row";
    row.innerHTML = `<span class="activity-dot"></span><div><strong>${item.title}</strong><span>${item.detail}</span></div><span class="activity-value">${item.value}</span>`;
    return row;
  }));
}

filter.addEventListener("change", renderUpdates);
refresh.addEventListener("click", () => {
  refresh.textContent = "Updated just now ✓";
  window.setTimeout(() => { refresh.textContent = "Refresh data ↻"; }, 1800);
});

renderChart();
renderUpdates();
