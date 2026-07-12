import { Route, Routes } from "react-router-dom";
import HomePage from "../pages/Home/HomePage";
import AboutPage from "../pages/About/AboutPage";
import PrivacyPage from "../pages/Privacy/PrivacyPage";
import HowItWorksPage from "../pages/HowItWorks/HowItWorksPage";
import StatementTipPage from "../pages/StatementTip/StatementTipPage";
import UploadPage from "../pages/Upload/UploadPage";
import ProcessingPage from "../pages/Processing/ProcessingPage";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import TransactionsPage from "../pages/Transactions/TransactionsPage";
import InsightsPage from "../pages/Insights/InsightsPage";
import ExplanationPage from "../pages/Explanation/ExplanationPage";
import NotFoundPage from "../pages/NotFound/NotFoundPage";
import ScrollReveal from "../components/feedback/ScrollReveal";

export default function App() {
  return <><ScrollReveal/><Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/upload" element={<UploadPage />} />
    <Route path="/session/:sessionId/processing" element={<ProcessingPage />} />
    <Route path="/session/:sessionId/dashboard" element={<DashboardPage />} />
    <Route path="/session/:sessionId/transactions" element={<TransactionsPage />} />
    <Route path="/session/:sessionId/insights" element={<InsightsPage />} />
    <Route path="/session/:sessionId/explanations/:entityId" element={<ExplanationPage />} />
    <Route path="/about" element={<AboutPage />} />
    <Route path="/privacy" element={<PrivacyPage />} />
    <Route path="/how-it-works" element={<HowItWorksPage />} />
    <Route path="/statement-tip" element={<StatementTipPage />} />
    <Route path="*" element={<NotFoundPage />} />
  </Routes></>;
}
