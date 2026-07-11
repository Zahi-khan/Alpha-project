import { request } from "./client";

export const createSession = () => request("/sessions", { method: "POST" });
export const getSession = (id) => request(`/sessions/${id}/status`);
export const getDashboard = (id) => request(`/sessions/${id}/presentation/dashboard`);
export const getTransactions = (id) => request(`/sessions/${id}/presentation/transactions`);
export const getInsights = (id) => request(`/sessions/${id}/presentation/insights`);
export const getExplanation = (id, entityId) => request(`/sessions/${id}/presentation/explanations/${entityId}`);
export const previewStatement = (id, file) => upload(`/sessions/${id}/preview`, file);
export const analyzeStatement = (id, file) => upload(`/sessions/${id}/analyze`, file);
export const deleteSession = (id) => request(`/sessions/${id}`, { method: "DELETE" });
export const reportUrl = (id) => `${import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000"}/sessions/${id}/report.pdf`;

async function upload(path, file) {
  const form = new FormData(); form.append("file", file);
  return request(path, { method: "POST", body: form });
}
