from pandasai.llm.local_llm import LocalLLM
import streamlit as st 
import pandas as pd 
from pandasai import SmartDataframe

# C:\Users\grant\proj_query_sql\app.py
# https://docs.getpanda.ai/library#config
import os



p_api_k=os.environ["PANDASAI_API_KEY"]
print(p_api_k)
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="qwen2.5-coder",
    
    
)



st.title("Data analysis with PandasAI")

uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head(4))
    if st.checkbox("Is there a dependent data set"):
        uploaded_file_1=st.file_uploader("upload your dependet file")
        if uploaded_file_1:
            data1=pd.read_csv(uploaded_file_1)
            st.write(data1.head(3))
    df = SmartDataframe(data, config={"llm": model,"custom_whitelisted_dependencies": ["scikit-learn","sqlalchemy","typing","io","pandasai","os","chr","glob","collections","sys","pathlib"],"security":"none","enable_cache":False})
    prompt = st.text_area("Enter your prompt:")
    
    print(prompt)


    if st.button("Generate"):   
        if prompt:
            if uploaded_file_1:
                file_name= uploaded_file_1.name
                
                print(file_name)
            with st.spinner("Generating response..."):
                st.write(df.chat(prompt))