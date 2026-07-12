import { useEffect, useState } from "react";
import styles from "./SessionNotice.module.css";

export default function SessionNotice({ expiresAt }) {
  const [message, setMessage] = useState("Temporary private session has begun.");

  useEffect(() => {
    const introduction = window.setTimeout(() => setMessage(null), 5200);
    const expiry = new Date(expiresAt).getTime();
    const warningDelay = Math.max(0, expiry - Date.now() - 15 * 60 * 1000);
    const warning = window.setTimeout(() => setMessage("Your session will end soon. Download your report or finish reviewing your analysis."), warningDelay);
    return () => { window.clearTimeout(introduction); window.clearTimeout(warning); };
  }, [expiresAt]);

  if (!message) return null;
  return <aside className={styles.notice} role="status" aria-live="polite"><strong>Private session</strong><span>{message}</span></aside>;
}
