import { useRef } from "react";
import styles from "./FileDropzone.module.css";
export default function FileDropzone({ file, onChange }) { const ref=useRef(); return <button type="button" className={`${styles.zone} focus`} onClick={()=>ref.current?.click()}><input ref={ref} type="file" accept=".csv,.pdf,text/csv,application/pdf" onChange={(e)=>onChange(e.target.files?.[0])}/><strong>{file ? file.name : "Choose a statement"}</strong><span>{file ? `${Math.ceil(file.size/1024)} KB selected` : "CSV or text-based PDF - up to 50 MB"}</span></button>; }
