import styles from "./Button.module.css";
export default function Button({ children, tone = "primary", loading, className = "", ...props }) { return <button className={`${styles.button} ${styles[tone]} focus ${className}`} disabled={loading || props.disabled} {...props}>{loading ? "Working…" : children}</button>; }
