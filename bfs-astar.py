class Path:
	def __init__(self, after, cost):
		self.after = after
		self.__cost = cost
	
	def init(self):
		global nodes
		self.__cost_est = self.__cost + nodes[self.after].est
		
	def cost(self, est=False):
		if est:
			return self.__cost_est
		else:
			return self.__cost
	

class Node:
	def __init__(self, id, name, est, paths):
		self.id = id
		self.name = name
		self.est = est
		self.__paths_dict = {path.after:path for path in paths}
		self.__paths_keys = [path.after for path in paths]
		for path in paths:
			path.before = self.id
	
	def path(self, after):
		return self.__paths_dict[after]
		
	def cost(self, after, est=False):
		return self.__paths_dict[after].cost(est)
		
	def paths(self):
		return self.__paths_keys
		
	def init(self):
		for path in self.__paths_dict.values():
			path.init()
		

nodes = {
	1: Node(1, "Semarang", 8, [Path(2, 3), Path(3, 3), Path(5, 5)]),
	2: Node(2, "Yogyakarta", 9, [Path(1, 3), Path(3, 1), Path(6, 7)]),
	3: Node(3, "Solo", 7, [Path(1, 3), Path(2, 1), Path(4, 2), Path(6, 5)]),
	4: Node(4, "Madiun", 6, [Path(3, 2), Path(5, 3), Path(6, 4)]),
	5: Node(5, "Surabaya", 24, [Path(1, 5), Path(4, 3), Path(7, 2)]),
	6: Node(6, "Malang", 4, [Path(2, 7), Path(3, 5), Path(4, 4), Path(7, 3)]),
	7: Node(7, "Pasuruan", 6, [Path(5, 2), Path(6, 3), Path(8, 1)]),
	8: Node(8, "Probolinggo", 0, [Path(7, 1)])
}


class Route:
	def __init__(self, route, cost):
		self.route = route
		self.total_cost = cost
		
	def branch(self, after, est=False):
		new_route = list(self.route)
		new_route.append(after)
		return Route(new_route, self.total_cost + nodes[self.last()].cost(after, est))
		
	def last(self):
		return self.route[-1]
		
	def branches(self, est=False):
		last = self.last()
		global nodes
		last_node = nodes[last]
		
		#generate branches
		#make sure not to circle around
		ret = [self.branch(path, est) for path in last_node.paths() if path not in self.route]
		
		return ret
		
	def calc_total_cost(self, est=False):
		count = len(self.route)
		if count <= 1:
			return 0
		
		cost = 0
		for i in range(0, count-1):
			before = self.route[i]
			after = self.route[i+1]
			cost += nodes[before].cost(after, est)
		
		return cost
	
	def __str__(self):
		global nodes
		return "Route: " + " => ".join([nodes[x].name for x in self.route]) + "; Total cost: " + str(self.total_cost)
		
	
def init():
	for node in nodes.values():
		node.init()
		
	
def bfs(start, end, astar=False):
	root = Route([start], 0)
	shortest = {start:0}
	routes = [root]
	
	found = None
	found_cost = float("inf")
	
	#keep looping if there's still paths left to explore, even if found
	while len(routes) > 0:
		
		#select best route to branch out of
		best = min(routes, key=lambda route: route.total_cost)
		
		#remove best value from list because it will be replaced by its branches
		routes.remove(best)
		
		#generate new branches from best
		branches = best.branches(astar)
		
		#remove long branch if shorter is known
		if len(branches) > 0:
			branches = [route for route in branches if route.last() not in shortest or route.total_cost <= min(found_cost, shortest[route.last()])] 
		
		#append branches to routes
		if len(branches) > 0:
			routes.extend(branches)
		
		#if no route is left from this point, early break
		if len(routes) == 0:
			break
		
		#refresh shortest known, update if found shorter route, while also searching for (shorter) end node
		for route in routes:
			last = route.last()
			cost = route.total_cost
			if last not in shortest or shortest[last] > cost:
				shortest[last] = cost
			#is it the end node and is it shorter than known valid route?
			if last==end and cost < found_cost:
				found = route
				found_cost = cost
		
		#remove long route if shorter is known
		routes = [route for route in routes if route.total_cost <= min(found_cost, shortest[route.last()])] 
	
	return found

def main():
	init()
	
	print("?? Jarak Terdekat ??")
	
	print()
	print("Pilih metode")
	print("1. Best First Search")
	print("2. A*")
	method = input("Metode: ")
	method = int(method)
	
	print()
	print("Pilih titik awal")
	for node in nodes.values():
		print("%d. %s" % (node.id, node.name))
	start = input("Titik awal: ")
	start = int(start)
	
	print()
	print("Pilih titik tujuan")
	for node in nodes.values():
		print("%d. %s" % (node.id, node.name))
	end = input("Titik tujuan: ")
	end = int(end)
	
	print()
	route = bfs(start, end, method == 2)
	
	if route is None:
		print("Rute tidak ditemukan")
	else:
		print(route)

if __name__== "__main__":
	main()
