import json
import logging
from collections import defaultdict, deque

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/bugfixer/p1', methods=['POST'])
def expose():

    data = request.get_json()

    resultant_list = []
    for project in data:

        times = project.get('time')
        prereqs = project.get('prerequisites')

        n = len(times)  # Number of projects
        graph = defaultdict(list)  # Adjacency list for the graph
        in_degree = [0] * n  # Track the number of incoming edges for each project
        
        # Build the graph and in-degree array
        for a, b in prereqs:
            graph[a - 1].append(b - 1)  # Convert to zero-based index
            in_degree[b - 1] += 1
        
        # Queue for projects with no prerequisites (in-degree 0)
        queue = deque()
        for i in range(n):
            if in_degree[i] == 0:
                queue.append(i)
        
        total_time = [0] * n  # Array to hold the total time for each project

        while queue:
            project = queue.popleft()
            total_time[project] += times[project]  # Add the time of the current project
            
            # For each dependent project, reduce the in-degree and add to queue if it's zero
            for dependent in graph[project]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
                total_time[dependent] = max(total_time[dependent], total_time[project])  # Update total time
        
        resultant_list.append(max(total_time))
        
    return json.dumps(resultant_list)
