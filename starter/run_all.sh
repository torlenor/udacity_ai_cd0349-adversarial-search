cat heuristics.txt | parallel python run_match.py -r 1 -o MINIMAX -r 1000 -t 1000 -p 2 -f -e {}