import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time


# Create figure object for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)



xs = []
ys = []
n = 10
test = 1


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    global test
    print ( test)
    test = test +1
    xs = []
    ys = []

    # Variable to print
    #temp_c = np.random.random()
    #temp_c = np.sin(i+1)
    # Add x and y to lists

    for a in range(n):
       # xs.insert(a, a+1)
      #  ys.insert(np.random.random(), a+1)
        xs.append(a)
        ys.append(np.random.random())
   # print (xs)
    print (len(xs))
   # print (ys)
    print(len(ys))

    # Limit x and y lists to 20 items
    #xs = xs[-n:]
    #ys = ys[-n:]

    # Draw x and y lists
    ax.clear()
    ax.set(xlim=(0, 15), ylim=(0, 5))
    #ax.bar(xs, ys,color='darkblue',width=.8)
    ax.plot(xs, ys ,color='black', linewidth=.5)

    # Format plot
    plt.xticks(rotation=45, ha='right')
   # plt.subplots_adjust(bottom=.3)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')


# Set up plot to call animate() function periodically
print("hey")




ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000,blit=False )
plt.show()

