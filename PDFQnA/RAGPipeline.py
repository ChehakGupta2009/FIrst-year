import chromadb, uuid
from groq import Groq
from chromadb.utils import embedding_functions
#Creating a pipeline
class RAGPipeline:
    #initialise the chunksize, overlap and key
    def __init__(self,groq_key,overlap=10,top_k=2,chunk_size=50):
        self.groq_key=Groq(api_key=groq_key)
        self.client = Groq( 
        api_key=groq_key
                )
        #initialisation
        self.overlap=overlap
        self.top_k=top_k
        self.chunk_size=chunk_size
        embed_fn= embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        #creating a chroma database
        chroma_db=chromadb.Client()
        self.col=chroma_db.create_collection(
            name="rag"+uuid.uuid4().hex[:6],
            embedding_function=embed_fn
        )

    def chunk(self,doc):
        #breaking the document into chunks and appending them into an array
        index=0
        chunks=[]
        words=doc.split(" ")
        while index<len(words):
            chunk=" ".join(words[index:self.chunk_size])
            chunks.append(chunk)
            #keep a record of number of chunks
            index+=(self.chunk_size-self.overlap)
        return chunks

    def index(self,docs,sources):
        '''
        creates index in chromadb
        docs-array of pages from the pdf
        sources-name of all files from which each entry in docs has been taken
        ''' 
        content=[]
        metadata=[]
        indx=[]
        for i,doc in enumerate(docs):
            chunks=self.chunk(doc)
            name=sources[i]
            for idx,chk in enumerate(chunks):
               content.append(chk)
               indx.append(f"{name}_chunk_{idx}")
               metadata.append({"source":name,"idx":idx})
        self.col.add(ids=indx,metadatas=metadata,documents=content)
        print("indexed")

    def ask(self,user_prompt,context,temp=1.0):
        '''
        completion function which asks the user entered quesion from ai and returns the response
        user_prompt-the user entered prompt
        context-the context of the question 
        '''
        msg=([
            {
                "role": "system",
                "content": f"Answer the question given in the content only using the information present in context:{context}.Don't hallucinate."
            } 
        ])
        msg+= [{
                        "role": "user",
                        "content": user_prompt
                    }]
        respo = self.client.chat.completions.create(
        model="allam-2-7b",messages=msg,temperature=temp)
        return respo.choices[0].message.content
    
    def query(self,question):
        # creates a query ffrom the question asked and returns the related chunks/answers
        context=""
        ret=self.col.query(query_texts=[question],n_results=3,include=["metadatas","documents","distances"])
        meta=ret["metadatas"][0]
        doc=ret["documents"][0]
        dist=ret["distances"][0]
        relevant=[(d,m) for d,distances,m in zip(doc,dist,meta) if distances<0.85]
        context="\n\n".join([f"{d}" for d in relevant])
        answer=self.ask(question,context)
        return answer
