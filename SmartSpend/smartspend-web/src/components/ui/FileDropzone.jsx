import { useRef } from "react";
import styles from "./FileDropzone.module.css";
export default function FileDropzone({ file, onChange }) { const ref=useRef(); return <button type="button" className={`${styles.zone} focus`} onClick={()=>ref.current?.click()}><input ref={ref} type="file" accept=".csv,text/csv" onChange={(e)=>onChange(e.target.files?.[0])}/><strong>{file ? file.name : "Choose a CSV statement"}</strong><span>{file ? `${Math.ceil(file.size/1024)} KB selected` : "CSV files up to 10 MB"}</span></button>; }
