import { Link } from "react-router-dom";
import MarketingLayout from "../../layouts/MarketingLayout";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";
import styles from "./StatementTipPage.module.css";

export default function StatementTipPage(){return <MarketingLayout><main id="main-content" className={`container page ${styles.page}`}><header><p className={styles.eyebrow}>Statement tip</p><h1 className="display">What do I do if I have a locked PDF?</h1><p className="bodyLarge">SmartSpend cannot read a password-protected statement PDF. Create an unlocked copy on your device before uploading it.</p></header><Card><h2 className="h2">Create an unlocked copy</h2><ol><li>Open the statement PDF using the password provided by your bank.</li><li>Choose <strong>Print</strong> in your PDF viewer.</li><li>Select <strong>Save as PDF</strong> or <strong>Print to PDF</strong> as the printer or destination.</li><li>Save the new PDF, then upload that copy to SmartSpend.</li></ol><p className={styles.note}>Only do this on a device you trust. The new PDF should be stored securely and deleted when you no longer need it.</p></Card><Link to="/upload"><Button>Back to statement analysis</Button></Link></main></MarketingLayout>}
