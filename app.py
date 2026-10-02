import json
import pandas as pd
import streamlit as st
from quality import assess, psi
st.set_page_config(page_title='Data Quality Demo',layout='wide')
st.title('Data Quality Assessment Demo')
st.caption('Synthetic claims: transparent checks, review recommendations, robust outliers, and drift.')
upload=st.file_uploader('Current batch CSV',type='csv')
current=pd.read_csv(upload) if upload else pd.read_csv('data/current.csv')
baseline=st.file_uploader('Optional reference batch CSV',type='csv')
reference=pd.read_csv(baseline) if baseline else pd.read_csv('data/reference.csv')
try: issues,report=assess(current)
except ValueError as e: st.error(str(e)); st.stop()
report['amount_psi']=psi(reference.amount,current.amount) if 'amount' in reference else None
cols=st.columns(3)
for col,key in zip(cols,['rows','issues','affected_rows']): col.metric(key.replace('_',' ').title(),report[key])
st.subheader('Detected issues and recommended review'); st.dataframe(issues)
if report['checks']: st.bar_chart(pd.Series(report['checks']))
st.write('Amount PSI:',report['amount_psi'])
st.caption('PSI depends on bins and sample size. It is a review signal, not a statistical significance test.')
st.download_button('Download issues',issues.to_csv(index=False),'issues.csv','text/csv')
st.download_button('Download report',json.dumps(report,indent=2),'report.json','application/json')
st.info('No automatic repairs are applied. Review source data before changing records.')
