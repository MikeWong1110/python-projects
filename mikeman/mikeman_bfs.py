class BFS():
    def solve(self, start, end):
        self.start=start
        self.end=end
        self.parents={}
        self.queue = [start]
        self.explored = [start]

        while len(self.queue) != 0:

            v = self.queue.pop(0)
            if v == end:
                print("Pathfind Successful")
                return True

            for n in v.get_neighbors():
                if n not in self.explored:
                    self.parents[n]=v
                    self.queue.append(n)
                    self.explored.append(n)

        return False

    def get_path(self):
        v = self.end
        path=[v]
        if v in self.parents:
            while v!=self.start:
                v=self.parents[v]
                path.append(v)
            return list(reversed(path))

        else:
            print("Pathfind Unsuccessful")
            return []


