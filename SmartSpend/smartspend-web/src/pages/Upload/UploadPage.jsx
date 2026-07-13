import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import {
  createSession,
  previewStatement,
  unlockAndPreviewStatement,
} from "../../app/api/sessions";
import MarketingLayout from "../../layouts/MarketingLayout";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";
import FileDropzone from "../../components/ui/FileDropzone";
import PrivacyNotice from "../../components/ui/PrivacyNotice";
import ProgressSequence from "../../components/feedback/ProgressSequence";
import styles from "./UploadPage.module.css";

const previewStages = ["Initializing", "Queued", "Running", "Executing", "Processing", "Synchronizing", "Compiling", "Deploying", "Finalizing", "Validating", "Reconciling", "Indexing", "Optimizing", "Generating", "Publishing"];
const passwordErrorCodes = new Set(["pdf_password_required", "invalid_pdf_password"]);

export default function UploadPage() {
  const [file, setFile] = useState();
  const [session, setSession] = useState();
  const [preview, setPreview] = useState();
  const [passwordRequired, setPasswordRequired] = useState(false);
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const mutation = useMutation({
    mutationFn: async () => {
      const active = session ?? await createSession();
      setSession(active);
      return passwordRequired
        ? unlockAndPreviewStatement(active.session_id, file, password)
        : previewStatement(active.session_id, file);
    },
    onSuccess: result => {
      setPreview(result);
      setPasswordRequired(false);
    },
    onError: error => {
      if (passwordErrorCodes.has(error.code)) setPasswordRequired(true);
    },
    onSettled: () => setPassword(""),
  });
  const lockedOut = mutation.error?.code === "pdf_password_attempt_limit";

  const selectFile = selected => {
    setFile(selected);
    setPreview(undefined);
    setPasswordRequired(false);
    setPassword("");
    mutation.reset();
  };

  return <MarketingLayout>
    <main id="main-content" className={`container page ${styles.page}`}>
      <div>
        <p className={styles.eyebrow}>Statement analysis</p>
        <h1 className="h1">Review your statement before analysis.</h1>
        <p className="bodyLarge">Select a CSV or text-based PDF up to 50 MB, preview the detected rows, then confirm when you are ready.</p>
      </div>
      <Card>
        <FileDropzone file={file} onChange={selectFile}/>
        {passwordRequired && <form className={styles.passwordBox} onSubmit={event => { event.preventDefault(); mutation.mutate(); }}>
          <div>
            <label htmlFor="pdf-password">PDF password</label>
            <p>SmartSpend will use it once to unlock and parse this statement in memory.</p>
          </div>
          <input
            id="pdf-password"
            type="password"
            value={password}
            autoComplete="off"
            spellCheck="false"
            disabled={mutation.isPending || lockedOut}
            onChange={event => setPassword(event.target.value)}
          />
          <Button type="submit" disabled={!password || lockedOut} loading={mutation.isPending}>Unlock and preview</Button>
          <small>The password is discarded after this request and is never added to your session.</small>
        </form>}
        <div className={styles.actions}>
          {!passwordRequired && <Button disabled={!file} loading={mutation.isPending} onClick={() => mutation.mutate()}>Preview statement</Button>}
          {preview && <Button tone="secondary" onClick={() => navigate(`/session/${session.session_id}/processing`, { state: { previewId: preview.preview_id } })}>Confirm and analyze</Button>}
        </div>
        <ProgressSequence active={mutation.isPending} stages={previewStages}/>
        {mutation.error && <p className={styles.error} role="alert">{mutation.error.message}</p>}
        {preview && <p className={styles.preview}>SmartSpend found {preview.total_rows} rows. No data has been permanently stored.</p>}
      </Card>
      <aside className={styles.locked}>
        <span><strong>Have a locked PDF?</strong> Do not worry. SmartSpend uses your password only to unlock this statement securely in memory. It is never saved, logged, or included in your report.</span>
      </aside>
      <PrivacyNotice/>
    </main>
  </MarketingLayout>;
}
