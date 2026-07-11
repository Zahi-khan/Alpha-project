import styles from "./Card.module.css";
export default function Card({ children, className = "" }) { return <section data-reveal className={`${styles.card} ${className}`}>{children}</section>; }
