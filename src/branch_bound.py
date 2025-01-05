from heapq import heappush, heappop


class Node:
    def __init__(self, level, profit, weight, bound, included_idx):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound
        self.included_idx = included_idx

    def __lt__(self, other):
        """used to determine the priority of the node in the priority queue.
        higher bound means higher priority"""

        return self.bound > other.bound


def branch_and_bound(weights, vals, n, capacity):
    # sort items by value/weight ratio
    items = sorted(zip(weights, vals), key=lambda x: x[1] / x[0], reverse=True)
    weights, vals = zip(*items)

    def bound(node):
        """
        calculate the bound of a node using the fractional knapsack approach
        """

        # infesible node
        if node.weight >= capacity:
            return 0

        profit_bound = node.profit
        j = node.level + 1
        total_weight = node.weight

        while j < n and total_weight + weights[j] <= capacity:
            total_weight += weights[j]
            profit_bound += vals[j]
            j += 1

        # if there are still items left, add fraction of the next item
        if j < n:
            profit_bound += (capacity - total_weight) * (vals[j] / weights[j])

        return profit_bound

    # create a priority queue
    pq = []
    root = Node(-1, 0, 0, 0, [])
    root.bound = bound(root)
    heappush(pq, root)

    max_profit = 0
    included_items_idx = []

    while pq:
        node = heappop(pq)

        # prune
        if node.bound <= max_profit or node.level == n - 1:
            continue

        # branch
        # left child (take the next item)
        left = Node(
            node.level + 1,
            node.profit + vals[node.level + 1],
            node.weight + weights[node.level + 1],
            0,
            node.included_idx + [node.level + 1],
        )

        # if the left child is feasible and has a better profit, update
        if left.weight <= capacity and left.profit > max_profit:
            max_profit = left.profit
            included_items_idx = left.included_idx

        left.bound = bound(left)

        # if the left child has a better bound, consider it for further exploration
        if left.bound > max_profit:
            heappush(pq, left)

        # right child (don't take the next item)
        right = Node(
            node.level + 1,
            node.profit,
            node.weight,
            0,
            node.included_idx,
        )

        right.bound = bound(right)
        if right.bound > max_profit:
            heappush(pq, right)

    return max_profit, included_items_idx
