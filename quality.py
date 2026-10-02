"""Transparent rules, robust outliers, and drift on synthetic claims."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED=['claim_id','patient_id','service_date','amount','provider']
def assess(frame):
    missing=[c for c in REQUIRED if c not in frame]
    if missing: raise ValueError('Missing columns: '+', '.join(missing))
    rows=frame.copy().reset_index(drop=True)
    amounts=pd.to_numeric(rows.amount, errors='coerce')
    valid=amounts[np.isfinite(amounts) & amounts.ge(0)]
    median=float(valid.median()) if len(valid) else 0.0
    mad=float((valid-median).abs().median()) if len(valid) else 0.0
    scores=(amounts-median).abs()/(1.4826*mad) if mad>0 else pd.Series(np.nan,index=rows.index)
    dates=pd.to_datetime(rows.service_date,errors='coerce',format='ISO8601')
    duplicate=rows.claim_id.duplicated(keep=False) & rows.claim_id.notna()
    issues=[]
    def add(i,check,severity,recommendation):
        issues.append({'row_id':int(i),'claim_id':str(rows.at[i,'claim_id']),'check':check,'severity':severity,'recommendation':recommendation})
    for i in rows.index:
        for col in REQUIRED:
            if pd.isna(rows.at[i,col]) or str(rows.at[i,col]).strip()=='':
                add(i,'missing_'+col,'error','Verify against source; do not invent a replacement.')
        if duplicate[i]: add(i,'duplicate_claim_id','error','Review source records before merging or removal.')
        if not np.isfinite(amounts[i]): add(i,'invalid_amount','error','Verify numeric amount against source.')
        elif amounts[i]<0: add(i,'negative_amount','error','Check whether adjustment/refund or incorrect value.')
        if pd.isna(dates[i]): add(i,'invalid_date','error','Verify service date format and source value.')
        if pd.notna(scores[i]) and scores[i]>3.5: add(i,'robust_amount_outlier','review','Review unusual amount; statistical anomaly is not proof of error.')
    issue_frame=pd.DataFrame(issues,columns=['row_id','claim_id','check','severity','recommendation'])
    affected=int(issue_frame.row_id.nunique())
    summary={'rows':len(rows),'issues':len(issues),'affected_rows':affected,'unflagged_rows':len(rows)-affected,'median_amount':median,'mad_amount':mad,'outlier_threshold':3.5,'outlier_check_available':mad>0,'checks':issue_frame.check.value_counts().to_dict()}
    return issue_frame,summary

def psi(reference,current,bins=10):
    a=pd.to_numeric(pd.Series(reference),errors='coerce').to_numpy(dtype=float)
    b=pd.to_numeric(pd.Series(current),errors='coerce').to_numpy(dtype=float)
    a,b=a[np.isfinite(a)],b[np.isfinite(b)]
    if not len(a) or not len(b): return None
    edges=np.unique(np.quantile(a,np.linspace(0,1,bins+1)))
    if len(edges)<2:
        v=a[0]; width=max(abs(v)*.01,1.0); edges=np.array([v-width,v+width])
    # Keep finite boundary bins even for constant references.
    edges=np.r_[-np.inf,edges,np.inf]
    p=np.histogram(a,edges)[0].astype(float)+.5
    q=np.histogram(b,edges)[0].astype(float)+.5
    p/=p.sum(); q/=q.sum()
    return float(np.sum((q-p)*np.log(q/p)))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',default='data/current.csv')
    parser.add_argument('--reference',default='data/reference.csv')
    parser.add_argument('--output',default='results')
    args=parser.parse_args()
    current=pd.read_csv(args.input); reference=pd.read_csv(args.reference)
    issues,report=assess(current)
    report['amount_psi']=psi(reference.amount,current.amount)
    report['added_columns']=sorted(set(current)-set(reference))
    report['removed_columns']=sorted(set(reference)-set(current))
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    issues.to_csv(out/'issues.csv',index=False)
    (out/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
