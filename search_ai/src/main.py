import re
from datetime import datetime

from search_ai import HuggyLLM,Agent
from search_ai.src.prompts.query_refiner import QUERY_REFINER_PROMPT
from pyopengenai.query_master import SearchRetriever

llm = HuggyLLM()
query_refiner = Agent('query_refiner',llm,QUERY_REFINER_PROMPT+f"TODAY DATE: {datetime.now().strftime('%Y-%m-%d')}")
search_query_generator = Agent('search_query_generator',llm,
                               """You are a SearchQueryGenerator ,Generate a Google search query  based on the user's query,
                               Below is the previous generated search queries, please Analyze the results  
                               PREVIOUS_SEARCH_QUERIES_AND_RESULTS:
                               <memory>
                               {memory}
                               </memory>
                               DO NOT start like Here is, Below is .., start generating directly
                               DONOT GENERATE in formats like site:abc//...dated(..) or brackets.. JUST ONE SINGLE CONCISE SENTENCE  etc.."""+ datetime.now().strftime("%Y-%m-%d")
                               )
compressor = Agent("compressor",llm,description="""
                           You are a Compressor, Compress the search results into a concise that feels relevant to GOAL:{goal}
                           PICK ONLY RELEVANT SENTENCES OR DATA .
                           your task is to compress it as much as possible and DO NOT generate additonal explanation or information.
                           start generating directly, without saying here is .. etc.
                           """)
answer_scorer = Agent("answer_scorer",llm,description="""
                           You are an AnswerScorer, Score the answers from the search results that satisfies  the GOAL:{goal}, respond with a integer score between 1 to 10 .
                           
                           Start generating directl the score, do not add extra information.
                           Respond only with one SINGLE INTEGER score without additional information or explanation.
                           """)
final_answer_generator= Agent("final_answer_generator",llm,description="""
                           You are a FinalAnswerGenerator, your task is to Generate a final answer in nice MARKDOWN FORMAT that answers our GOAL:{goal} from the USER_RESULTS.
                           user will provide the USER_RESULTS below.
                           Start generating directly, do not add extra information.
                           """)


web_search = SearchRetriever(extract_pdf=False)

max_turns = 5
turn = 0
memory = ""

while(turn<max_turns):
    turn+=1

    if turn==1:
        user_query = "python code of openai new package swarm" # + ", if they have github code tthat will be great"
        goal = query_refiner.act(user_query,silent=False)

    search_int=3
    search_results=""
    while(search_int and search_results==""):
        search_int-=1
        search_query = search_query_generator.act(goal,memory=memory,silent=False)
        search_results = "\n".join(web_search.query_based_content_retrieval(goal,topk=15).topk_chunks)
        print(f"## SEARCH RESULTS:\n\n{search_results}\n")


    result = compressor.act(search_results,goal=goal,silent=False)
    answer_score = answer_scorer.act(result, goal=goal, silent=False)
    score_regex = re.findall(r'\d+',answer_score)
    score = int(score_regex[-1]) if score_regex else -1
    if score>5:
        memory+=f'SEARCH_QUERY:\n{search_query}\nRESULT:{result}\nGOAL_SCORE:{score}/10\n'
    if memory and score==-1 or score==10 or turn==max_turns :
        final_answer_generator.act(memory,silent=False)
        break




