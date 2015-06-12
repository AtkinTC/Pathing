def a_star(nodes, start, end, real = True):
    closedset = []
    openset = [start]
    came_from = {}

    def dist(n1, n2):
        if real:
            xy1 = nodes[n1]['loc']
            xy2 = nodes[n2]['loc']
            return pow(pow(xy2[0]-xy1[0],2) + pow(xy2[1]-xy1[1],2),0.5)
        else:
            return 1

    #g_score is the distance to in current best path
    g_score = {start : 0}

    #f_score is an estimate of the total distance through this node
    #f_score must be <= to the unknown real distance
    f_score = {start : g_score[start] + dist(start, end)}

    while len(openset) > 0:
        short = -1
        for k in openset:
            if short is -1 or f_score[k] < f_score[short]:
                short = k
                
        current = short

        if current is end:
            return construct_path(came_from, end)

        openset.remove(current)
        closedset.append(current)
        for node in nodes[current]['links']:
            if node in closedset:
                continue

            temp_g_score = g_score[current] + dist(current, node)

            if node not in openset or temp_g_score < g_score[node]:
                came_from[node] = current
                g_score[node] = temp_g_score
                f_score[node] = g_score[node] + dist(node, end)
                if node not in openset:
                    openset.append(node)
    return []
        
def construct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]
