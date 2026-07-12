import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { getTransactions } from "../../app/api/sessions";
import Card from "../../components/ui/Card";
import SiteNav from "../../components/navigation/SiteNav";
import styles from "./TransactionsPage.module.css";

export default function TransactionsPage() {
  const { sessionId } = useParams();
  const [expanded, setExpanded] = useState(null);
  const { data, error, isLoading } = useQuery({ queryKey: ["transactions", sessionId], queryFn: () => getTransactions(sessionId) });
  if (isLoading) return <main className="container page">Loading transactions…</main>;
  if (error) return <main className="container page">{error.message}</main>;
  return <><SiteNav sessionId={sessionId} /><main id="main-content" className={`container page ${styles.page}`}><Link to={`/session/${sessionId}/dashboard`}>← Overview</Link><div><p className={styles.eyebrow}>Detailed analysis</p><h1 className="h1">Every transaction, clearly explained.</h1><p className="bodyLarge">Open any row to see the statement details used in this private analysis. Account and card numbers are never displayed.</p></div><Card><div className={styles.table}><div className={`${styles.row} ${styles.head}`}><b>Date</b><b>Merchant</b><b>Category</b><b>Payment</b><b>Amount</b><b>Details</b></div>{data.data.map(item=>{const isOpen=expanded===item.id;return <div className={styles.transaction} key={item.id}><div className={styles.row}><span>{item.formatted_date}</span><span>{item.merchant_name??item.fallback_description}</span><span>{item.category_name??"Uncategorized"}</span><span>{item.payment_name??"Unknown"}</span><strong>{item.formatted_amount}</strong><button type="button" className={styles.detailButton} aria-expanded={isOpen} onClick={()=>setExpanded(isOpen?null:item.id)}>{isOpen?"Hide":"View"}</button></div>{isOpen&&<div className={styles.details}><Detail label="Original description" value={item.original_description??item.fallback_description}/><Detail label="Transaction type" value={item.source_type??item.direction}/><Detail label="Confidence" value={item.confidence_label}/><Detail label="Statement category" value={item.category_name}/><Detail label="Payment method" value={item.payment_name}/><Detail label="Statement reference" value={item.statement_reference}/><Detail label="Balance after transaction" value={item.balance}/><Detail label="Industry" value={item.industry_name}/>{item.warning_flags.length>0&&<Detail label="Review notes" value={item.warning_flags.join(" · ")}/>}</div>}</div>})}</div></Card></main></>;
}

function Detail({ label, value }) { return value ? <div><span>{label}</span><strong>{value}</strong></div> : null; }
