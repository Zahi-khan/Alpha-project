import { useEffect, useRef, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { deleteSession } from "../../app/api/sessions";
import Button from "../ui/Button";
import styles from "./SiteNav.module.css";

export default function SiteNav({ sessionId }) {
  const [open, setOpen] = useState(false);
  const [showRayyan, setShowRayyan] = useState(false);
  const [confirmExit, setConfirmExit] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");
  const navRef = useRef(null);
  const timeoutRef = useRef(null);
  const navigate = useNavigate();
  const close = () => setOpen(false);
  const animateLogo = () => { setShowRayyan(true); clearTimeout(timeoutRef.current); timeoutRef.current = setTimeout(() => setShowRayyan(false), 900); };
  const handleLogoClick = event => {
    close(); animateLogo();
    if (!sessionId) return;
    event.preventDefault();
    setConfirmExit(true);
  };
  const leaveAnalysis = async () => {
    setDeleting(true); setError("");
    try { await deleteSession(sessionId); navigate("/", { replace: true }); }
    catch (reason) { setError(reason.message); setDeleting(false); }
  };
  useEffect(() => {
    const dismiss = event => { if (!navRef.current?.contains(event.target)) close(); };
    const onKey = event => { if (event.key === "Escape") { close(); setConfirmExit(false); } };
    document.addEventListener("pointerdown", dismiss); document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("pointerdown", dismiss); document.removeEventListener("keydown", onKey); clearTimeout(timeoutRef.current); };
  }, []);
  return <><header className={styles.wrap}><nav ref={navRef} className={`container ${styles.nav}`} aria-label="Main navigation"><Link className={`${styles.logo} ${showRayyan ? styles.rayyan : ""} focus`} to="/" onClick={handleLogoClick} aria-label={sessionId ? "Return home and delete this analysis" : "RK SmartSpend home"}><span className={styles.mark}>{showRayyan ? "RAYYAN" : "RK"}</span><b className={styles.brand}><span className={styles.short}>SmartSpend</span><span className={styles.home}>Home</span></b></Link><button className={`${styles.menu} focus`} aria-label="Toggle navigation" aria-expanded={open} onClick={() => setOpen(!open)}>Menu</button><div className={`${styles.links} ${open ? styles.open : ""}`}><NavLink onClick={close} to="/about">About</NavLink><NavLink onClick={close} to="/upload">Statement Analysis</NavLink><NavLink onClick={close} to="/privacy">Privacy Policy</NavLink><Link className={styles.mobileCta} to="/upload" onClick={close}><Button>Analyse Your Statement</Button></Link></div><Link className={styles.cta} to="/upload" onClick={close}><Button>Analyse Your Statement</Button></Link></nav></header>{confirmExit && <div className={styles.backdrop} role="presentation"><section className={styles.dialog} role="dialog" aria-modal="true" aria-labelledby="exit-title"><p className={styles.dialogEyebrow}>Leave private analysis</p><h2 id="exit-title" className="h2">Are you sure?</h2><p>Going back home will delete this analysis and its temporary session. This cannot be undone.</p>{error && <p className={styles.error}>{error}</p>}<div className={styles.dialogActions}><button type="button" className={styles.noButton} disabled={deleting} onClick={() => setConfirmExit(false)}>No, stay here</button><button type="button" className={styles.yesButton} disabled={deleting} onClick={leaveAnalysis}>{deleting ? "Deleting…" : "Yes, delete and go home"}</button></div></section></div>}</>;
}
