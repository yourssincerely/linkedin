import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
import json

def create_sql_engine(path:str = "login/mysql_login.json"):
    """
    path: str 
        Defaults to login/mysql_login.json. 
        The path to any JSON file that contains this information:
            {"username" : "db username",
            "password" : "db password"} 
        
    return: (sqlalchemy.engine.base.Engine, sqlalchemy.orm.session.Session)
    
    Returns a tuple with a sqlalchemy engine and session based on the log in
    information provided.
    """
    with open(path) as f:
        file = json.load(f)   
    username = file["username"]
    password = file["password"]
    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@localhost/linkedin")
    session = Session()
    return engine, session

def pandas_to_mysql(df:pd.core.frame.DataFrame, table:str, if_exists:str = "replace"):
    """
    df: pandas.core.frame.DataFrame 
    table: str 
        Name of the table taht will be added to the database.
    if_exists: str {'fail', 'replace', 'append'}
        Defaults to "replace".
        fail: If table exists, do nothing.
        replace: If table exists, drop it, recreate it, and insert data.
        append: If table exists, insert data. Create if does not exist.
    
    Takes a pandas.core.frame.DataFrame object and creates a table in the mysql database
    'linkedin'.
    """
    engine, session = create_sql_engine()
    df.to_sql(name = table,
        con = engine,
        if_exists = if_exists,
        index = False)
    session.commit()
    print(f"{df.shape[0]} entries were added to the table {table}!")

def sql_query_to_pandas(query:str):
    """
    query: str 
        Any SQL query.

    return: pd.core.frame.DataFrame
    
    Connects to the 'linkedin' mySQL database and returns a pandas.core.frame.DataFrame 
    with the results of the query provided.
    """
    engine, session = create_sql_engine()
    results = engine.execute(query).mappings().all()
    df = pd.DataFrame.from_dict(results)
    return df