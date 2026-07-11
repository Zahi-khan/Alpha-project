import Card from "./Card"; import styles from "./MetricCard.module.css";
export default function MetricCard({ card }) { return <Card className={styles.card}><span>{card.label}</span><strong className="metricValue">{card.formatted_value}</strong><small>{card.supporting_text}</small></Card>; }
