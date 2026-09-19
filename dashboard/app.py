import os,requests,pandas as pd,streamlit as st
API_URL=os.getenv("API_URL","http://api:8000")
st.set_page_config(page_title="iPrint Recommendation Dashboard",layout="wide")
st.title("iPrint News Recommendation & Ranking System")
try:
 h=requests.get(f"{API_URL}/health",timeout=5).json(); status=h["status"]; model=h["model_version"]
except Exception: status="offline"; model="unknown"
a,b,c,d=st.columns(4); a.metric("API",status); b.metric("Model",model); c.metric("Monitoring","Prometheus"); d.metric("Cache","Redis")
st.divider(); st.subheader("Live Recommendation Explorer")
user=st.text_input("User ID","demo-user"); category=st.selectbox("Category",["general","technology","business","sports","science"]); k=st.slider("Top-K",1,20,10)
if st.button("Get Recommendations",type="primary"):
 r=requests.post(f"{API_URL}/recommend",json={"user_id":user,"category":category,"top_k":k},timeout=10); r.raise_for_status(); p=r.json()
 st.success(f"Model {p['model_version']} | Cache hit: {p['cached']}")
 st.dataframe(pd.DataFrame([{"Rank":i,"Article ID":x["article_id"],"Title":x["title"],"Score":x["score"]} for i,x in enumerate(p["recommendations"],1)]),use_container_width=True,hide_index=True)
st.subheader("Model Evaluation")
st.dataframe(pd.DataFrame({"Metric":["Precision@10","Recall@10","NDCG@10","MRR","Coverage","Diversity","Novelty"],"Value":[0.0]*7}),use_container_width=True,hide_index=True)
