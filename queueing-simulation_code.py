import numpy as np
import matplotlib.pyplot as plt
import math
# np.random.seed(42)  # For reproducible runs 
serviceTime = [(10, 3), (6, 2)]
serviceTimeProbabilty = [0.4, 0.6]
serverNotAccesible = [0.1, 0.2, 0.3]
ArrivedTime = []
queueLength = [[], [], []]
fullWaitTime = [[], [], []]
busyServerTime = [0, 0, 0]
noServiceTime = [0, 0, 0]

def simulateServers(): 
    global customerLeftCount,currentTime

    queues = [[], [], []]
    servers = [0, 0, 0] 
    currentTime = 0
    customerLeftCount = 0
    for l in range(10000):
        # Generate exponential inter-arrival time (mean = 5 min) and advance the simulation clock — requirement (c)
        interArrivalTime = -5 * math.log(np.random.random())
        currentTime += interArrivalTime
        ArrivedTime.append(currentTime)

        # Route the customer to the shortest queue (ties → lowest index) — requirement (d)
        currentLengthOfQueue = []
        for q in queues:
            qlen = len(q)
            currentLengthOfQueue = currentLengthOfQueue + [qlen]

        minLen = min(currentLengthOfQueue)
        shortestQueue = []
        for i, l in enumerate(currentLengthOfQueue):
            if l == minLen:
                shortestQueue = shortestQueue + [i]

        firstQueueDefault = shortestQueue[0]

        # Allow queue switching to the current shortest queue with probability 0.7 — requirement (e)
        queues[firstQueueDefault] = queues[firstQueueDefault] + [currentTime]

        if np.random.random() < 0.7:
            currentLengthOfQueue = []
            for q in queues:
                qlen = len(q) 
                currentLengthOfQueue = currentLengthOfQueue + [qlen]
            
            newMinLength = min(currentLengthOfQueue)

            newShortestQueue = []
            for i, l in enumerate(currentLengthOfQueue):
                if l == newMinLength:
                    newShortestQueue = newShortestQueue + [i]

            newFirstQueueDefault = newShortestQueue[0]
            if newFirstQueueDefault != firstQueueDefault:
                queues[firstQueueDefault].remove(currentTime)
                queues[newFirstQueueDefault] = queues[newFirstQueueDefault] + [currentTime]


        for i in range(3):# Process server i and its queue while the server is available
            while queues[i] and servers[i] <= currentTime:
                arrivalTime = queues[i].pop(0)
                waitingTime = currentTime - arrivalTime

                # Reneging: leave if waiting > 6 min (p = 0.8) or > 3 min (p = 0.4) — requirements (f, g)
                if waitingTime > 6:
                    if np.random.random() < 0.8: 
                        customerLeftCount = customerLeftCount+ 1
                        continue
                elif waitingTime > 3:
                    if np.random.random() < 0.4:
                        customerLeftCount = customerLeftCount+ 1
                        continue
                # Service time (mixture): 40% ~ N(10, 3) and 60% ~ N(6, 2) — requirement (h)
                if(np.random.random() < 0.4):
                    customerServiceTime = np.random.normal(10,3)
                else:
                    customerServiceTime = np.random.normal(6,2)

                servers[i] = currentTime + customerServiceTime
                busyServerTime[i] = busyServerTime[i] + customerServiceTime
                fullWaitTime[i] = fullWaitTime[i] + [waitingTime]

                # After each service, the server may go down (S1: 0.1, S2: 0.2, S3: 0.3); downtime ~ Exp(mean = 3) — requirement (i)
                if np.random.random() < serverNotAccesible[i]:
                    out_of_customerServiceTime = np.random.exponential(3)
                    servers[i] = servers[i] + out_of_customerServiceTime
                    noServiceTime[i] =noServiceTime[i]+ out_of_customerServiceTime
        # Track queue lengths over time for plotting LQ_i(t) and L(t)
        for i in range(3):
            qlen = len(queues[i])
            queueLength[i] = queueLength[i] + [qlen]

simulateServers()

L=0
for queue in queueLength:
    L = L+len(queue)
L = L / 10000

print(f'L = {L}')

LQ = []
for l in queueLength:
    LQ =LQ+[sum(l)/10000]

print(f'LQ1 ={LQ[0]}')
print(f'LQ2 ={LQ[1]}')
print(f'LQ3 ={LQ[2]}')

servedCustomers = 10000 - customerLeftCount  # فقط کسانی که سرویس گرفتن

W = 0
for w in fullWaitTime:
    W += sum(w)

W = W / servedCustomers
print(f'W = {W:.4f}')


WQ = []
for w in fullWaitTime:
    if w:
        WQ.append(sum(w) / len(w))
    else:
        WQ.append(0)

print(f'WQ1 = {WQ[0]}')
print(f'WQ2 = {WQ[1]}')
print(f'WQ3 = {WQ[2]}')

P = []
for time in busyServerTime:
    P =  P + [time / currentTime]

print(f'p1 = {P[0]}')
print(f'p2 = {P[1]}')
print(f'p3 = {P[2]}')

print(f'sum Of Out of service times for each of the servers: server 1 = {noServiceTime[0]} server 2 = {noServiceTime[1]} server 3 = {noServiceTime[2]}')
print(f"number of customers who left the system: {customerLeftCount}")


total_customers = []
for i in range(len(queueLength[0])):
    total = 0
    for j in range(3):
        total = total + queueLength[j][i]
    total_customers = total_customers + [total]

# Plot system-level L(t) and per-queue LQ_i(t) over simulation time
plt.figure(figsize=(14, 6))
plt.plot(ArrivedTime, total_customers, label="L(t)", linewidth=0.5, color="black")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Total Customers")
plt.title("L(t)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.show()


plt.figure(figsize=(14, 4))
plt.plot(ArrivedTime, queueLength[0], label=f"LQ1(t)", 
            linewidth=0.5, color="black")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Total Customers")
plt.title("LQ1(t)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.show()

plt.figure(figsize=(14, 4))
plt.plot(ArrivedTime, queueLength[1], label=f"LQ2(t)", 
            linewidth=0.5, color="black")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Total Customers")
plt.title("LQ2(t)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.show()

plt.figure(figsize=(14, 4))
plt.plot(ArrivedTime, queueLength[2], label=f"LQ3(t)", 
            linewidth=0.5, color="black")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Total Customers")
plt.title("LQ3(t)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.show()