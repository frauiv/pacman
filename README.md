# pacman
Project 1 for 411
Jazbel Lopez
Ivana Pavlovic

http://ai.berkeley.edu/search.html

To get our UCS to work with how we implement the search and the data we stored we created an updated version of update() from the priority queue class. Our function started at 209 of útil.py. We called it update2() we have included útil.py in our zipped file but I will also add the function below to for quicker access. 



#new function
    def update2(self, item, priority, successor):
        for index,(p, c, i) in enumerate(self.heap):
    #when found the same state in queue 
            if i[2][0] == successor[0]:
       # if priority not less than current do nothing
                if p <= priority:
                    break
                 #else update in queue and then heapify
                i[0] = item[0]
                i[1] = priority
                i[2] = successor
                heapq.heapify(self.heap)

