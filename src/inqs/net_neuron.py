import math
import re
import time
from collections import defaultdict
from pathlib import Path

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggy import HuggingChat
# from pyopengenai import QueryRefiner, SearchQueryToNSubquery
# from pyopengenai.query_master import RealTimeGoogleSearchProvider,UrlTextParser
#
# def net_neuron(query,llm):
#     n_splits = 5
#     rq = QueryRefiner.refine_query(llm,query)
#     splits = SearchQueryToNSubquery.ai_splits(llm,rq,n_splits)
#     searcher = RealTimeGoogleSearchProvider(animation=False)
#     content_fetcher = UrlTextParser(extract_pdf=False)
#     queries = splits.get("refined_splits")
#     urls = searcher.perform_batch_search(queries,max_urls=n_splits*6)
#     print("URLs:",len(urls))
#     urls = list(set(urls))
#     print("URLs:",len(urls))
#     res = content_fetcher.parse_html(urls)
#     content = "<DOCUMENT_SEP>".join([_ for _ in res if _])
#     Path("content.txt").write_text(content)
#
#
# def main():
#     llm = HuggingChat(hf_email="santhoshkammari1999@gmail.com",
#                       hf_password="SK99@pass123")
#     print(net_neuron("who is modi?", llm))

# if __name__ == '__main__':
#     main()


import re
from pathlib import Path

from langchain_community.graphs.rdf_graph import cls_query_rdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from wordllama import WordLlama
import math

def split_words(text):
    return re.findall(r'\b[\w\']+\b|[.,!?;]', text)

def split_sentences(text):
    return re.findall(r'[^.!?]+[.!?]', text)


def cluster_words(words, cluster_indices):
    # Create a dictionary to store clusters
    clusters = defaultdict(list)

    # Iterate through words and their corresponding cluster indices
    for word, index in zip(words, cluster_indices):
        clusters[index].append(word)

    # Convert the dictionary to a list of lists
    result = list(clusters.values())

    return result

wl = WordLlama.load()
content = Path("content.txt").read_text()
content = content.split("<DOCUMENT_SEP>")[0]


def n_gram_split_sentences(content):
    sentences = []
    for N in range(100,500,10):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=N,chunk_overlap=int(math.sqrt(N)))
        sentences.append(text_splitter.split_text(content))
    return sentences


word_groups = n_gram_split_sentences(content)
cluster_words_all = []
for words in word_groups:
    cluster = wl.cluster(words,k=int(math.sqrt(len(words))))
    cluster_words_all.extend([" ".join(_) for _ in cluster_words(words,cluster[0])])

print(wl.topk("when is modi born?", cluster_words_all))

