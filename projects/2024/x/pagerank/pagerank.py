import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python pagerank.py corpus")
    # corpus = crawl(sys.argv[1])
    corpus = crawl(r"D:\ProgramData\Ubuntu\rootfs\home\cs50\zhongyanmin\ai50\projects\2024\x\pagerank\corpus0")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist = {}

    if len(corpus[page]) > 0:
        for link in corpus:
            prob_dist[link] = round((1 - damping_factor) / len(corpus), 3)
            
        for link in corpus[page]:
            prob_dist[link] = round(prob_dist[link] + damping_factor / len(corpus[page]), 3)
    else:
        for link in corpus:
            prob_dist[link] = round(1 / len(corpus), 3)
      
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    for page in corpus:
        ranks[page] = 0
    page = random.choices(list(corpus.keys()))[0]
    
    for _ in range(1, n):
        tran = transition_model(corpus, page, damping_factor)
        element_list = [key for key in tran.keys() if key != page]
        prob_list = [tran[val] for val in element_list]
        page = random.choices(element_list, k=1, weights=prob_list)[0]
        ranks[page] += 1
            
    ranks_reg = {k: v / n for k, v in ranks.items()}
            
    return ranks_reg
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    threshold = 0.001
    N = len(corpus)
    
    for key in corpus:
        ranks[key] = 1 / N
    
    while True:
        count = 0
        for key in corpus:
            new = (1 - damping_factor) / N
            sigma = 0
            for link in corpus:
                if key in corpus[link]:
                    num_links = len(corpus[link])
                    sigma += ranks[link] / num_links
            
            new += damping_factor * sigma
            
            if abs(ranks[key] - new) < threshold:
                count += 1
            ranks[key] = new
            
        if count == N:
            break
                
    return ranks
            

if __name__ == "__main__":
    main()
