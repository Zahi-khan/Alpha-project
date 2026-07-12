import { useMemo, useState } from "react";
import styles from "./DataChart.module.css";

const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export default function DataChart({ chart, detailTo }) {
  const [graphType, setGraphType] = useState("bar");
  const [chooserOpen, setChooserOpen] = useState(false);
  const raw = chart?.series?.[0]?.values ?? [];
  const points = chart?.type === "line" ? raw : [...raw].sort((a, b) => Math.abs(Number(b.y)) - Math.abs(Number(a.y))).slice(0, 8);
  const maximum = Math.max(...points.map(point => Math.abs(Number(point.y))), 1);
  const linePoints = useMemo(() => points.map((point, index) => `${points.length === 1 ? 50 : index / (points.length - 1) * 100},${100 - Math.abs(Number(point.y)) / maximum * 86}`).join(" "), [points, maximum]);
  if (!chart || chart.empty_state) return <section className={styles.empty}><h3>{chart?.title ?? "Analysis"}</h3><p>{chart?.empty_state?.message ?? "No chart data is available yet."}</p></section>;
  const renderBars = () => <div className={styles.rows}>{points.map((point, index) => { const value = Number(point.y); const size = Math.max(3, Math.abs(value) / maximum * 100); return <div className={styles.row} key={point.x}><div className={styles.label}><span title={point.x}>{point.x}</span><strong className={value < 0 ? styles.negative : ""}>{currency.format(value)}</strong></div><div className={styles.track}><span className={`${styles.bar} ${value < 0 ? styles.negativeBar : ""}`} style={{ "--bar-size": `${size}%`, animationDelay: `${index * 85}ms` }} /></div></div>; })}</div>;
  const renderLine = () => <div className={styles.lineChart} key={graphType}><svg viewBox="0 0 100 100" role="img" aria-label={`${chart.title} ${graphType} graph`} preserveAspectRatio="none">{graphType === "area" && <polygon className={styles.area} points={`0,100 ${linePoints} 100,100`} />}<polyline className={styles.line} points={linePoints} /></svg><div className={styles.lineLabels}>{points.map(point=><span key={point.x} title={currency.format(Number(point.y))}>{point.x}</span>)}</div></div>;
  return <section className={styles.chart} aria-label={chart.accessibility_summary}><div className={styles.heading}><div><p className={styles.kicker}>{graphType === "bar" ? "Breakdown" : "Over time"}</p><h2 className="h2">{chart.title}</h2></div>{detailTo && <a href={detailTo}>View transactions</a>}</div>{graphType === "bar" ? renderBars() : renderLine()}<div className={styles.chooser}><button type="button" className={styles.chooseButton} aria-expanded={chooserOpen} onClick={()=>setChooserOpen(value=>!value)}>Choose type of graph</button>{chooserOpen&&<div className={styles.options} role="group" aria-label="Choose graph type">{["bar", "line", "area"].map(type=><button type="button" className={graphType===type?styles.selected:""} key={type} onClick={()=>{setGraphType(type);setChooserOpen(false)}}>{type[0].toUpperCase()+type.slice(1)}</button>)}</div>}</div><p className={styles.summary}>{chart.accessibility_summary}</p></section>;
}
