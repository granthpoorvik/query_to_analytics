from pandasai.llm.local_llm import LocalLLM
# For the UI interface designing .
import streamlit as st
import pandas as pd
#SDF is used for the whole LLM process.
from pandasai import SmartDataframe
import os


p_api_k = os.environ.get("PANDASAI_API_KEY", "")

# Initiating the model 
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="qwen2.5-coder",
)

st.title("PandasAI")

# Upload main dataset
uploaded_file = st.file_uploader("Upload the main CSV file", type=['csv'])

if uploaded_file:
    df1 = pd.read_csv(uploaded_file)
    st.write("Main Dataset (df1.head(3)):")
    st.write(df1.head(3))
    
    resp=st.checkbox("Is ther any dependent data?")
    
    if resp:
      # Upload dependent dataset
      uploaded_file_1 = st.file_uploader("Upload your dependent CSV file", type=['csv'])
      if uploaded_file_1:
          df2 = pd.read_csv(uploaded_file_1)
          st.write("Dependent Dataset (df2.head(3)):")
          st.write(df2.head(4))

          
          # df1_sdf = SmartDataframe(df1, config={"llm": model})
          # relationship_prompt = f"find the linking :\n\n" \
          #                     f"df1.head(3): {df1.head(3).to_string()}\n\n" \
          #                     f"df2.head(3): {df2.head(3).to_string()}"
          
          # with st.spinner("Analyzing relationship..."):
          #     relationship = df1_sdf.chat(relationship_prompt)
          #     st.write("### Auto-Detected Relationship:")
          #     st.write(relationship)
    df1_sdf = SmartDataframe(df1, config={"llm": model,"custom_whitelisted_dependencies": ["scikit-learn","sqlalchemy","typing","io","pandasai","os","chr","glob","collections","sys","pathlib","future"],"security":"none","enable_cache":False})

    # User prompt
    user_prompt = st.text_area("Enter your prompt:")

    if st.button("Generate"):
        if user_prompt:
            if resp:
              """ the below relationship created a ambiguity in the code processing 
                  currently we are not using this process.
              """ 
              relationship=r'''
"You are given multiple CSV datasets representing different entities. Your task is to:

Identify potential relationships between the datasets by detecting common keys, even if the column names differ.

Automatically map datasets on the most relevant common fields.

Learn the schema, column names, and their context to generate meaningful insights from the combined data.

Answer user-defined analytical questions  data."
'''
              
              #final_prompt = f"{relationship}  \n\n CSV example data\n data1:\n{df1.head(5)}\n--------------------------\ndata2:\n{df2.head(5)}\n\n  file :-  {uploaded_file_1.name}\n\n{user_prompt}"
              final_prompt = f"{user_prompt}\n\n\ndata reference \n{df2.head(5)}\n\n   related data files path :- \n.\{uploaded_file_1.name}\n\n"
              print(final_prompt)
            else:
                final_prompt = f"{user_prompt}"
            with st.spinner("Generating response..."):
                response = df1_sdf.chat(final_prompt)
                st.write("### Response:")
                st.write(response)
                
