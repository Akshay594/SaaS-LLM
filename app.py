from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
<<<<<<< HEAD
from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
)
from llama_index.core.query_engine.pandas import PandasInstructionParser
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI


import pandas as pd

from run_keys import set_keys
set_keys()


instruction_str = (
    "1. Convert the query to executable Python code using Pandas.\n"
    "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
    "3. The code should represent a solution to the query.\n"
    "4. PRINT ONLY THE EXPRESSION.\n"
    "5. Do not quote the expression.\n"
)

pandas_prompt_str = (
    "You are working with a pandas dataframe in Python.\n"
    "The name of the dataframe is `df`.\n"
    "This is the result of `print(df.head())`:\n"
    "{df_str}\n\n"
    "Follow these instructions:\n"
    "{instruction_str}\n"
    "Query: {query_str}\n\n"
    "Expression:"
)
response_synthesis_prompt_str = (
    "Given an input question, synthesize a response from the query results.\n"
    "Query: {query_str}\n\n"
    "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
    "Pandas Output: {pandas_output}\n\n"
    "Response: "
)
=======
import os

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
>>>>>>> origin/main

class StudentAgent:
    def __init__(self, file_path:str) -> None:
        reader = SimpleDirectoryReader(input_dir=file_path)
        self.documents = reader.load_data()
        self.index = None
<<<<<<< HEAD
        self.__input_dir = file_path
        print(f"Document has been loaded from : `{file_path}` folder.")


    def build_query_pipeline(self, df, llm):
        pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
            instruction_str=instruction_str, df_str=df.head(5)
        )
        pandas_output_parser = PandasInstructionParser(df)
        response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)
        qp = QP(
            modules={
                "input": InputComponent(),
                "pandas_prompt": pandas_prompt,
                "llm1": llm,
                "pandas_output_parser": pandas_output_parser,
                "response_synthesis_prompt": response_synthesis_prompt,
                "llm2": llm,
            },
            verbose=True,
        )
        qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
        qp.add_links(
            [
                Link("input", "response_synthesis_prompt", dest_key="query_str"),
                Link(
                    "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
                ),
                Link(
                    "pandas_output_parser",
                    "response_synthesis_prompt",
                    dest_key="pandas_output",
                ),
            ]
        )
        # add link from response synthesis prompt to llm2
        qp.add_link("response_synthesis_prompt", "llm2")
        return qp

    def make_query(self, query, llm, file_name="marksheet.csv"):
        df = pd.read_csv(f"{self.__input_dir}/{file_name}")
        qp = self.build_query_pipeline(df, llm)
        response = qp.run(
            query_str=query,
        )
        return response
      



agent = StudentAgent("data")
query_str = "How many students do we have in the data?"
llm = OpenAI(model="gpt-3.5-turbo")
response = agent.make_query(query_str, llm)
print(response)
=======
        print(f"Document has been loaded from : `{file_path}` folder.")

    def make_index(self):
        self.index = VectorStoreIndex.from_documents(self.documents)
        print("Index has been made: ", self.index)

    def make_query(self, query):
        query_engine = self.index.as_query_engine()
        return query_engine.query(query)
    


agent = StudentAgent("data")
agent.make_index()
response = agent.make_query("How many students do we have in the data?")
print(response)

>>>>>>> origin/main
