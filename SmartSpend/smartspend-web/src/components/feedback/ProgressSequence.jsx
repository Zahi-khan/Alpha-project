import { useEffect, useState } from "react";
import styles from "./ProgressSequence.module.css";

export default function ProgressSequence({ active, stages, interval = 2000 }) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (!active) {
      setIndex(0);
      return undefined;
    }
    const timer = window.setInterval(() => setIndex(current => Math.min(current + 1, stages.length - 1)), interval);
    return () => window.clearInterval(timer);
  }, [active, interval, stages.length]);

  if (!active) return null;
  return <div className={styles.status} role="status" aria-live="polite"><span className={styles.label}>Preparing your statement</span><strong key={stages[index]} className={styles.stage}>{stages[index]}</strong><span className={styles.count}>Step {index + 1} of {stages.length}</span></div>;
}
