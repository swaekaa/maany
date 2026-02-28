# test_rg_generate.py
from RAG1 import rag_query, rg_generate
pre = {"query_en":"When was the Computer Science department established?", "lang":"en", "query":"When was...","thread_id":"t1","user_id":"u1","safety":{"safe":True}}
rag = rag_query(pre["query_en"])
ans, sources = rg_generate(pre["user_id"], pre["thread_id"], pre, rag)
print(ans)
print(sources)
