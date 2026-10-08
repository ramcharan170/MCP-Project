import arxiv
import json
import os
from typing import List
from dotenv import load_dotenv
import anthropic

paper_Dir="papers"
def search_papers(topic: str, max_results: int=5)-> List:
    """Search for papers on aiXiv based on a Topc and Storetheir information.
    Args:
    topic: the topic to Search for
    max_results: Maximum number of results to retrieve
    Returns: List of paper Ids found in the search.
    """
    client=arxiv.Client()

    search=arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
        # What is this sortby?
    )
    papers=client.results(search)
    # create the dictionary for this topic
    path=os.path.join(paper_Dir,topic.lower().replace(" ", "_"))
    os.makedirs(path,exist_ok=True)
    file_path=os.path.join(path, "papers_info.json")
    # Try to learn the make directories code..
    # Try to load existing papers info

    

    try:
        with open(file_path,"r") as json_file:
            papers_info=json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info={}

    # process Each paper and add to papers_info
    paper_ids=[]
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info={
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url':paper.pdf_url,
            'published':str(paper.published.date())
        }
        papers_info[paper.get_short_id()]=paper_info
        # Save the updated  papers into a json file
        with open(file_path, "w") as json_file:
            json.dump(papers_info,json_file, indent=2)
        print(f"Results are saved in: {file_path}")
        return paper_ids

if __name__=="__main__":
    search_papers("computers")
