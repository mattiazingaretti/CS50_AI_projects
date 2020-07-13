import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
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
    result = dict()
    
    links = corpus[page] #links is a set
    
    probability = (1-damping_factor)/ len(corpus)
    linked_pages_prob = 0 #Just to initialize to a neutral value
    
    #Needed only if page has at least 1 link
    if len(links) != 0:
        linked_pages_prob = damping_factor/len(links)
    
    for p in corpus:
        #if p has no link
        if len(corpus[p]) == 0:
            result[p] = 1/len(corpus)
        else:
            if p not in links:
                result[p] = probability
            else:
                result[p] = probability + linked_pages_prob
    #DEBUG check that will sum at 1
    if round(sum(result.values()),5) != 1:
        print(f'ERROR! not addding up to 1')
    print(result,corpus)
    return result
            

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    
    #First sample generated at random
    if len(corpus)> 0:
        first_sample = random.choice(list(corpus.keys()))
        result[first_sample] = 1/(len(corpus)*n)
    tm = transition_model(corpus, first_sample, damping_factor)
    
    # n- 1 samples
    for i in range(n-1):
        
        if i == 0:
            next_sample = random.choices(population = list(tm.keys()), weights = list(tm.values()))
        else:
            next_sample = random.choices(population = list(next_tm.keys()), weights = list(next_tm.values()))
        if next_sample[0] in list(result.keys()):
            result[next_sample[0]] += (1/(len(corpus)*n))
        else:
            result[next_sample[0]] = 1/(len(corpus)*n)
        
        next_tm = transition_model(corpus, next_sample[0], damping_factor)
    
    return result
    
        

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
