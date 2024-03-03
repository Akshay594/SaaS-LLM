from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
import os

os.environ["OPENAI_API_KEY"] = "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"

class StudentAgent:
    def __init__(self, file_path:str) -> None:
        reader = SimpleDirectoryReader(input_dir=file_path)
        self.documents = reader.load_data()
        self.index = None
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

