"# E_E_query_analytics" 


Here is a example output :
![alt text](./Screenshot 2025-03-24 174156.png)

make sure we update pandas after requirements files are installed 
because the llm requests for lower versoin of pandas but pandasai requests for latest versoin of pandas.

cmd:
pip install -U pandas

![alt text](./image.png)


When we don’t white list the libraries then we face this issue

to resolve this we need to add the library to the below line

df1_sdf = SmartDataframe(df1, config={"llm": model,"custom_whitelisted_dependencies": ["scikit-learn","sqlalchemy","typing","io","pandasai","os","chr","glob","collections","sys","pathlib","future"     <><><><><>APPEND HERE<><><><><>],"security":"none","enable_cache":False})


the current working and updated file is new_code.py