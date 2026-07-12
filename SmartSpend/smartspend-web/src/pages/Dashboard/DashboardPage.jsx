import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { getDashboard, reportUrl } from "../../app/api/sessions";
import Card from "../../components/ui/Card";
import InsightCard from "../../components/ui/InsightCard";
import MetricCard from "../../components/ui/MetricCard";
import PrivacyNotice from "../../components/ui/PrivacyNotice";
import StoryNav from "../../components/navigation/StoryNav";
import TypewriterMessage from "../../components/feedback/TypewriterMessage";
import SessionNotice from "../../components/feedback/SessionNotice";
import DataChart from "../../components/charts/DataChart";
import styles from "./DashboardPage.module.css";

export default function DashboardPage() {
  const { sessionId } = useParams();
  const { data, error, isLoading } = useQuery({ queryKey: ["dashboard", sessionId], queryFn: () => getDashboard(sessionId) });
  if (isLoading) return <main id="main-content" className="container page"><TypewriterMessage text="Patience is a virtue" /></main>;
  if (error) return <main id="main-content" className="container page">{error.message}</main>;
  const chart = id => data.charts.find(item => item.id === id);
  const transactionPath = `/session/${sessionId}/transactions`;
  const suggestions = data.top_insights.filter(insight => ["savings", "recurring"].includes(insight.type));
  const observations = data.top_insights.filter(insight => !["savings", "recurring"].includes(insight.type));

  return <><SessionNotice expiresAt={data.session.expires_at} /><div className="container"><StoryNav sessionId={sessionId} /></div><main id="main-content" className={`container page ${styles.page}`}><header className={styles.header}><div><p className={styles.eyebrow}>Your financial story</p><h1 className="h1">Your financial snapshot</h1></div><div><span>Private session - expires automatically</span><a href={reportUrl(sessionId)}>Download report</a></div></header><PrivacyNotice /><section id="snapshot" className={styles.metrics}>{data.summary_cards.map(card => <MetricCard key={card.id} card={card} />)}</section><section id="spending" className={styles.columns}><Card><DataChart chart={chart("category_spending")} detailTo={transactionPath} /></Card><Card><DataChart chart={chart("merchant_spending")} detailTo={transactionPath} /></Card></section><section id="patterns" className={styles.columns}><Card><DataChart chart={chart("monthly_cashflow")} detailTo={transactionPath} /></Card><Card><DataChart chart={chart("payment_methods")} detailTo={transactionPath} /></Card></section><section id="next-steps"><div className={styles.sectionHeader}><div><p className={styles.eyebrow}>Ways to save</p><h2 className="h2">Where you could cut back</h2></div></div><div className={styles.insights}>{suggestions.length ? suggestions.map(insight => <InsightCard key={insight.id} insight={insight} sessionId={sessionId} />) : <Card>No reliable saving opportunity was found in this statement period.</Card>}</div></section><section><div className={styles.sectionHeader}><div><p className={styles.eyebrow}>Explainable findings</p><h2 className="h2">Patterns we found</h2></div><Link to={`/session/${sessionId}/insights`}>View all insights</Link></div><div className={styles.insights}>{observations.length ? observations.map(insight => <InsightCard key={insight.id} insight={insight} sessionId={sessionId} />) : <Card>Not enough comparable history is available for reliable patterns yet.</Card>}</div></section><section id="attention" className={styles.storyPanel}><h2 className="h2">Detailed analysis</h2><p>Open any transaction to see its original description, category, payment method, statement reference, balance, and confidence. Account and card numbers stay hidden.</p><Link to={transactionPath}>Explore all transactions</Link></section><section className={styles.storyPanel}><h2 className="h2">What you can do next</h2><p>Open an insight to see its supporting evidence, or download a private report of this analysis.</p><a href={reportUrl(sessionId)}>Download private report</a></section></main></>;
}
