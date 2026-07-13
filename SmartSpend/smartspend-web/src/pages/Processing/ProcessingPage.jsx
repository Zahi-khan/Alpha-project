import { useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { analyzePreview } from "../../app/api/sessions";
import Card from "../../components/ui/Card";
import TypewriterMessage from "../../components/feedback/TypewriterMessage";
import SiteNav from "../../components/navigation/SiteNav";
import styles from "./ProcessingPage.module.css";

const stages=["Reading the statement","Identifying transaction fields","Normalising transaction details","Resolving merchants","Understanding spending categories","Building your financial story"];
export default function ProcessingPage(){const {sessionId}=useParams();const {state}=useLocation();const navigate=useNavigate();const mutation=useMutation({mutationFn:()=>analyzePreview(sessionId,state.previewId),onSuccess:()=>navigate(`/session/${sessionId}/dashboard`)});useEffect(()=>{if(!state?.previewId)navigate("/upload");else mutation.mutate()},[]);return <><SiteNav sessionId={sessionId}/><main id="main-content" className={`container page ${styles.page}`}><Card><div className={styles.spinner}/><h1 className="h1">Your statement is being read</h1><TypewriterMessage text="Your statement is being read"/><p>SmartSpend is preparing a private, explainable overview. Stages appear only when the analysis is ready to advance.</p><ol>{stages.map(stage=><li key={stage}>{stage}</li>)}</ol>{mutation.error&&<p className={styles.error}>{mutation.error.message}</p>}</Card></main></>}
