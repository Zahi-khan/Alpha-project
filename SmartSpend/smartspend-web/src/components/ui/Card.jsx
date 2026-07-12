import styles from "./Card.module.css";
export default function Card({ children, className = "", reveal = true }) { return <section {...(reveal ? { "data-reveal": "" } : { "data-no-reveal": "" })} className={`${styles.card} ${className}`}>{children}</section>; }
