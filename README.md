# graphs-of-wikipedia

CSC111 Final Project 2 

# Proposal Docs
https://docs.google.com/document/d/1ezulcVQjRDMUXfZqLp5jb7Ybjxgoc2sCfNWQQUa2XYA/edit

# Written Report
https://docs.google.com/document/d/1ToBFi4Q5BQbz96f43Byr7zsaZ32mNc5NoW_L4xGs43U/edit

# About

I hate wikipedia now thanks 📜✨

## Authors 🖊️

- **[Lapatrada (Claire) Jaroonjetjumnong](https://github.com/help)**  - cpu destroyer 3000
- **[Sataphon (Puyefang) Obra](https://github.com/puyepuye)** - front end master
- **[Thitiwut (Mac) Pattanasuttinont](https://github.com/aFluffyHotdog)** - curious algorithm warrior
- **[Yi-an (Kimi) Chu](https://github.com/??????)** - literal academic weapon princess

## Ongoing - Updates
Claire - Getting Wikipedia pages, titles, and links probably can't get any better than this. Right now I just have to run create_graph overnight many times to destroy my cpu and add more stuff to the graph, but it's 21.9 MB right now so I actually don't know if I should. I only ran it twice on wiki/Tree and wiki/University_Of_Toronto lol ;-;

### create_graph.py
This function recursively explores links on a webpage up to a specified level. It starts from a given `start_url` and collects links from the page. For each link, it adds the link's title to a dictionary `data` with the title of the `start_url` as the key. If the current level is less than the specified `level`, the function recursively calls itself for each link found, incrementing the current level. Once it reaches the specified `level`, it saves the `visited` set and the `data` dictionary to files (`visited_file` and `graph_file`, respectively).

### bfs.py
This code defines a breadth-first search (BFS) function BFS_path that finds a path between two nodes (s1 and s2) in a graph (G). It uses a queue (Q) to traverse the graph starting from the s1 node. The function also handles loading a graph from a file using the load_dict_from_file function. 

## TODO
- graph making more efficiently (claire)
- return multiple paths (claire)
- interactive ui (puye)
- expand the graph (claire)
- clean up pyTA
- The latex stuff
- Improve readability (Mac)
- Automcomplete for when you input something (Mac)

## Getting Started 🚀

Clone the repository and help pls bb:

```bash
git clone https://github.com/puyepuye/graphs-of-wikipedia.git
cd graphs-of-wikipedia
python bfs.py

git add .
git commit -m "message"
git push
