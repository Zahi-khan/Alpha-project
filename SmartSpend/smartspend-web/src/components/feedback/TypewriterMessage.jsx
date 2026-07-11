import styles from "./TypewriterMessage.module.css";
export default function TypewriterMessage({ text }) { return <p className={styles.message} aria-live="polite"><span aria-hidden="true">{text}</span><span className="srOnly">{text}</span></p>; }
