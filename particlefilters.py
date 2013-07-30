
# Now we want to simulate robot
# motion with our particles.
# Each particle should turn by 0.1
# and then move by 5. 
#
#
# Don't modify the code below. Please enter
# your code at the bottom.
from numpy import *

from pylab import *
from math import *
import random

landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size	
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    def move_real(self, turn, forward,forward_noise,turn_noise):
            if forward < 0:
                raise ValueError, 'Robot cant move backwards'         
            mean_dist_d=0.0
            mean_dist_t=0.0
            var_dist_d=forward_noise
            #print 'forward noise',forward_noise
            #print 'turn noise',turn_noise
            var_dist_t=turn_noise
            mean_turn_d=0.0
            mean_turn_t=0.0
            var_turn_t=turn_noise
            var_turn_d=forward_noise
            
            dist=random.gauss(forward*mean_dist_d+turn*mean_dist_t,forward**2*var_dist_d+turn**2*var_dist_t)
            #print 'distance is',dist
            # turn, and add randomness to the turning command
            turn_dist=random.gauss(forward*mean_turn_d+turn*mean_turn_t,forward**2*var_turn_d+turn**2*var_turn_t)
            #print 'turn is',turn_dist
            orientation = self.orientation + float(turn_dist) 
            orientation %= 2 * pi
            '''
            # move, and add randomness to the motion command
            
            x = self.x + (cos(orientation) * dist)
            y = self.y + (sin(orientation) * dist)
            x %= world_size    # cyclic truncate
            y %= world_size
            '''
            # now make a new motion model according to Elzar paper
            #dist=float(forward)+random.gauss(0,0,self.forward_noise)
            # according to Elzar paper dist comes from a distribtuion
            
            orientation_new=self.orientation+float(turn_dist)/2
            orientation_new %= 2*pi
            x=self.x+(cos(orientation_new)*dist)
    
            y = self.y + (sin(orientation_new) * dist)
            
            x %= world_size    # cyclic truncate
            y %= world_size        
            
            
            # set particle
            res = robot()
            res.set(x, y, orientation)
            res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
            return res    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        mean_dist_d=0.0
        mean_dist_t=0.0
        var_dist_d=self.forward_noise
        var_dist_t=self.turn_noise
        mean_turn_d=0.0
        mean_turn_t=0.0
        var_turn_t=self.turn_noise
        var_turn_d=self.forward_noise
        dist=random.gauss(forward*mean_dist_d+turn*mean_dist_t,forward**2*var_dist_d+turn**2*var_dist_t)
        
        # turn, and add randomness to the turning command
        turn_dist=random.gauss(forward*mean_turn_d+turn*mean_turn_t,forward**2*var_turn_d+turn**2*var_turn_t)
        
        orientation_real = self.orientation + float(turn_dist) 
        orientation_real %= 2 * pi
        '''
        # move, and add randomness to the motion command
        
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        '''
        # now make a new motion model according to Elzar paper
        #dist=float(forward)+random.gauss(0,0,self.forward_noise)
        # according to Elzar paper dist comes from a distribtuion
        
        orientation_new=self.orientation+float(turn_dist)/2
        orientation_new %= 2*pi
        x=self.x+(cos(orientation_new)*dist)

        y = self.y + (sin(orientation_new) * dist)
        
        x %= world_size    # cyclic truncate
        y %= world_size        
        
        
        # set particle
        res = robot()
        res.set(x, y, orientation_real)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        dist_sum=0.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
            dist_sum+=dist
        return prob,dist_sum
    # so you actually move but the sensor reading would point otherwise
    def kidnapp(self):
        self.x = random.random() * world_size	
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi        
        
    
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))



def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]



####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####

myrobot = robot()

N = 500
p = []
test=arange(1,10)
world=zeros((world_size,world_size))

for i in range(4):
    world[landmarks[i][0],landmarks[i][1]]=1

#print myrobot.x,myrobot.y

#show()
world[myrobot.x,myrobot.y]=2
#print  world[landmarks[i][0],landmarks[i][1]]
#print world
ion()
for i in range(N):
        x = robot()
    
        x.set_noise(0.05,0.05,5.0)
        p.append(x)
w_mean=[]
for t in range(10):
    
    clf()
    for i in range(4):
        hold(1)
        plot(landmarks[i][0],landmarks[i][1],'bo')

    world[myrobot.x,myrobot.y]=0
    if t<=5:
        myrobot = myrobot.move_real(0.0,5.0,0.05,0.05) #turn,forward
    else:
        print ' I am on a different terrain'
        myrobot=myrobot.move_real(0.0,5.0,0.15,0.15)
    #myrobot=myrobot.move_real(0.0,5.0,0.05,0.05)
    plot(myrobot.x,myrobot.y,'r^')
    world[myrobot.x,myrobot.y]=2

    
   
    Z=myrobot.sense()
    p2 =[]
    for i in range(N):
        p2.append(p[i].move(0.0,5.0)) # turn,forward
            
      
    
    
    w=[]
    
    p_previous=p
    p=p2
    # I think there is a missing p=p2 .. need to verify this
    for i in range(N):
        prob_sensor,dist_sensor=p2[i].measurement_prob(Z)
        #print prob_sensor
        w.append(prob_sensor)
        
        #dist_w.append(dist_sensor)
    #print 'the difference is',diff_odom
    figure(1)
    
    #figure(1)
    #print w
    
    
    #resampling step
    
    p3=[]
    index = int(random.random() * N)
    beta = 0.0
    mw = max(w)
    diff_odom_x=[]
    
    for i in range(int(N)):
        beta += random.random() * 2.0 * mw
        while beta > w[index]:
            beta -= w[index]
            index = (index +1) % N
            
        p3.append(p[index])
        diff_odom_x.append(np.sqrt(((p[index].x-p_previous[index].x)**2)+((p[index].y-p_previous[index].y)**2)))
    
    
    diff_odom=np.asarray(diff_odom_x)
    print 'the mean is',np.mean(diff_odom)
    print 'the variance is',np.var(diff_odom)
    #print 'the difference in the x is',diff_odom_x
   
    
 
    p=p3
    
    #print p
    print len(p)
  
    print 'The actual location of the robot',myrobot
    particle_location=get_position(p)
    print 'The predicted location',particle_location    
    plot(particle_location[0],particle_location[1],'r*')
    raw_input("Press enter to see the robot move")

print myrobot
#print p


#print p