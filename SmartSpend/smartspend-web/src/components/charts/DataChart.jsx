import styles from "./DataChart.module.css";

const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export default function DataChart({ chart, detailTo }) {
  if (!chart || chart.empty_state) return <section className={styles.empty}><h3>{chart?.title ?? "Analysis"}</h3><p>{chart?.empty_state?.message ?? "No chart data is available yet."}</p></section>;
  const raw = chart.series?.[0]?.values ?? [];
  const points = chart.type === "line" ? raw : [...raw].sort((a, b) => Math.abs(Number(b.y)) - Math.abs(Number(a.y))).slice(0, 8);
  const maximum = Math.max(...points.map(point => Math.abs(Number(point.y))), 1);
  return <section className={styles.chart} aria-label={chart.accessibility_summary}><div className={styles.heading}><div><p className={styles.kicker}>{chart.type === "line" ? "Over time" : "Breakdown"}</p><h2 className="h2">{chart.title}</h2></div>{detailTo && <a href={detailTo}>View transactions</a>}</div><div className={styles.rows}>{points.map((point, index) => { const value = Number(point.y); const size = Math.max(3, Math.abs(value) / maximum * 100); return <div className={styles.row} key={point.x}><div className={styles.label}><span title={point.x}>{point.x}</span><strong className={value < 0 ? styles.negative : ""}>{currency.format(value)}</strong></div><div className={styles.track}><span className={`${styles.bar} ${value < 0 ? styles.negativeBar : ""}`} style={{ "--bar-size": `${size}%`, animationDelay: `${index * 85}ms` }} /></div></div>; })}</div><p className={styles.summary}>{chart.accessibility_summary}</p></section>;
}
