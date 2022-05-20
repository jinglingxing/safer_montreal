import sys
sys.path.append('../')
sys.path.append('../definitions/')
from node import Node
from typing import List, Set, Dict


class AStar:
    def __init__(self):
       return None

    @staticmethod
    def h_score(curr_node: Node, end_node: Node) -> float:
        """ h_score(heuristic function) represents the estimation to reach the end node """
        euclidean_distance = curr_node.distance(end_node)
        return euclidean_distance

    def search_best_node(self, open_set: Set[Node], f_score: Dict[Node, float]) -> Node:
        """
        find the best node to search for
        @param  open_set: includes the node
        """
        # initialize the start point from open set as best node
        best_node = list(open_set)[0]
        best_score = f_score[best_node]

        for node in list(open_set)[1::]:
            score = f_score[node]
            if score < best_score:
                best_score = score
                best_node = node
        return best_node

    @staticmethod
    def backtrack(came_from: Dict[Node, Node], end_node: Node, start_node: Node) -> List[Node]:
        """ find the path from end node to start node with the best score """
        path = []
        path.append(end_node)
        while end_node != start_node:
            pre_node = came_from[end_node]
            path.append(pre_node)
            end_node = pre_node
        return path[::-1]

    def find_path(self, start_node: Node, end_node: Node) -> List[Node]:
        # list of nodes we should visit using a set
        open_set = set()
        open_set.add(start_node)

        # store the path in a hash map: from next node to current node
        came_from = {}

        # cost to arrive at the current node from starting node
        g_score = {}
        g_score[start_node] = 0

        # fScore[n](total score) represents our current best guess
        # f_score = g_score + h_score, h_score(heuristic function) represents the estimation to reach the end node
        f_score = {}
        f_score[start_node] = self.h_score(start_node, end_node)

        while open_set:
            # find the node in open set having the lowest fScore value
            curr_node = self.search_best_node(open_set, f_score)

            # remove current node from open set
            open_set.remove(curr_node)

            if curr_node == end_node:
                # found the path
                return self.backtrack(came_from, end_node, start_node)

            # check the neighbors of current node if we didn't find the path
            neighbors = curr_node.get_neighbours()
            for nei in neighbors:
                # d(current,neighbor) is the weight of the edge from current to neighbor
                d_score = nei.get_weight()
                # tentative_gScore is the distance from start to the neighbor through current
                tentative_g_score = g_score[curr_node] + d_score
                if nei not in g_score or tentative_g_score < g_score[nei]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[nei] = curr_node
                    # update g_score and f_score
                    g_score[nei] = tentative_g_score
                    f_score[nei] = tentative_g_score + self.h_score(nei, end_node)
                    if nei not in open_set:
                        open_set.add(nei)
        # failure: no path found
        return None


if __name__ == "__main__":
    from crime import Crime
    a_star = AStar()
    start = Node(0, 0)
    end = Node(2, 0)
    nei1 = Node(0, 1)
    nei2 = Node(1, 1)
    nei3 = Node(2, 1)
    nei4 = Node(0, 2)
    nei5 = Node(1, 2)
    nei6 = Node(2, 2)
    nei7 = Node(1, 0)

    crime = Crime(1, 0, 'Car', 'Day', 'Dec', '2012')
    for _ in range(5):
        nei7.add_crime_occurrence(crime)
        #nei2.add_crime_occurrence(crime)

    start._neighbours = [nei1, nei7]
    nei1._neighbours = [start, nei4, nei2]
    nei2._neighbours = [nei7, nei1, nei5, nei3]
    nei3._neighbours = [nei2, end, nei6]
    nei4._neighbours = [nei1, nei5]
    nei5._neighbours = [nei4,  nei2, nei6]
    nei6._neighbours = [nei5, nei3]
    nei7._neighbours = [start, end, nei2]
    end._neighbours = [nei7, nei3]

    l = a_star.find_path(start, end)
    for i in l:
        print(i)
