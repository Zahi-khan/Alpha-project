import { Link } from "react-router-dom";
import MarketingLayout from "../../layouts/MarketingLayout";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";
import styles from "./HowItWorksPage.module.css";

const steps = [
  ["01", "Upload your statement", "Choose a supported CSV statement. SmartSpend creates a temporary private session—no account or bank connection is required."],
  ["02", "Review before analysis", "Check the selected file, its format, and its size before you explicitly begin the analysis."],
  ["03", "Follow your financial story", "Move from a calm snapshot through spending, patterns, attention points, and supporting evidence at your own pace."],
  ["04", "Keep your report, not your data", "Download your report when you are ready. Your temporary session can be deleted at any time and expires automatically."],
];

export default function HowItWorksPage(){return <MarketingLayout><main id="main-content" className={`container page ${styles.page}`}><header className={styles.header}><p className={styles.eyebrow}>A considered process</p><h1 className="display">A clearer way to understand a statement.</h1><p className="bodyLarge">SmartSpend turns transaction records into a private, explainable financial story—without asking for bank credentials or a permanent account.</p></header><section className={styles.steps} aria-label="How SmartSpend works">{steps.map(([number,title,copy])=><Card key={number}><span className={styles.number}>{number}</span><h2 className="h2">{title}</h2><p>{copy}</p></Card>)}</section><section className={styles.closing}><div><p className={styles.eyebrow}>Ready when you are</p><h2 className="h1">Start with one statement.</h2></div><Link to="/upload"><Button>Analyse Your Statement</Button></Link></section></main></MarketingLayout>}
