from random import *

width, height = 500, 800

def setup():
    global birdpng, backimage
    size(width, height, P3D)
    textSize(20)
    stroke(0)
    birdpng = loadImage("bird.png")
    backimage = loadImage("background.png")
    
class Bird():
    
    def __init__(self, x, y, vy, radius):
        self.x = x
        self.y = y
        self.vy = vy
        self.radius = radius
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getVy(self):
        return self.vy
    
    def getRadius(self):
        return self.radius
    
    def setX(self, dx):
        self.x = dx
        
    def setY(self, dy):
        self.y = dy
    
    def setVy(self, dvy):
        self.vy = dvy
        
    def setAy(self, day):
        self.ay = day
        
    def jump(self, jumpvalue, t):
        self.setVy(0)
        self.setY(jumpvalue*t**2 + self.getVy()*t + self.getY())
        self.setVy(jumpvalue*t + self.getVy())
        
    def draw(self, birdpng):
        fill(230, 247, 22)
        
        #circle(self.getX(), self.getY(), self.getRadius()*2)
        image(birdpng, self.getX()-(self.getRadius()*3)/2, self.getY()-(self.getRadius()*3)/2, self.getRadius()*3, self.getRadius()*3)
        
    def calculNewPos(self, t, ay):
        self.setY((1/2)*ay*t**2 + self.getVy()*t + self.getY())
        self.setVy(ay*t + self.getVy())
            
class Spike():
    
    def __init__(self, altitude, spikehole, spikelarge, bout_hauteur, bout_largeur):
        self.altitude = altitude
        self.hole = spikehole
        self.large = spikelarge
        self.bout_hauteur = bout_hauteur
        self.bout_largeur = bout_largeur
        self.xpos = width+bout_largeur
        self.sens = choice([True, False])
        self.verticalspeed = uniform(1, 2)
        
    def getX(self):
        return self.xpos
    
    def getAltitude(self):
        return self.altitude
    
    def getHole(self):
        return self.hole
    
    def getSpikeLarge(self):
        return self.large
    
    def getSens(self):
        return self.sens
    
    def getVerticalSpeed(self):
        return self.verticalspeed
    
    def getBoutHauteur(self):
        return self.bout_hauteur
    
    def getBoutLargeur(self):
        return self.bout_largeur
    
    def setX(self, dx):
        self.xpos = dx
        
    def setAltitude(self, da):
        self.altitude = da
        
    def changeSens(self):
        if self.getSens():
            self.sens = False
        else:
            self.sens = True
        
    def draw(self, horizontalspeed, mooving):
        
        altitude = self.getAltitude()
        vertical_speed = self.getVerticalSpeed()
        bout_hauteur = self.getBoutHauteur()
        bout_largeur = self.getBoutLargeur()
        hole = self.getHole()
        sens = self.getSens()
        spike_large = self.getSpikeLarge()
        
        strokeWeight(2)
        fill(59, 234, 81)
        
        self.setX(self.getX()-horizontalspeed) # Déplacement du spike vers le joueur
        
        if mooving:
            if sens: # Gère le sens vertical du déplacement
                self.setAltitude(altitude+vertical_speed)
            else:
                self.setAltitude(altitude-vertical_speed)
            
            if altitude < 110+bout_hauteur and sens == False:
                self.changeSens()
            if altitude+hole > height-bout_hauteur and sens:
                self.changeSens()
    
        rect(self.getX()-bout_largeur, altitude+hole, 2*bout_largeur+spike_large, bout_hauteur)
        rect(self.getX()-bout_largeur, altitude, 2*bout_largeur+spike_large, -bout_hauteur)
        rect(self.getX(), 110, spike_large, altitude-(110+bout_hauteur))
        rect(self.getX(), altitude+hole+bout_hauteur, spike_large, height-altitude-hole)
        
def createSpike():
    global spikes_, spikehole, bout_hauteur, bout_largeur
    spikes_.append(Spike(randint(110+bout_hauteur, height-spikehole-bout_hauteur), spikehole, spikelarge, bout_hauteur, bout_largeur))
    
def collision(spike):
    global score
    
    x = bird.getX()
    y = bird.getY()
    radius = bird.getRadius()
    
    spikex = spike.getX()
    spikealtitude = spike.getAltitude()
    spikehole = spike.getHole()
    spikelarge = spike.getSpikeLarge()
    bouthauteur = spike.getBoutHauteur()
    boutlargeur = spike.getBoutLargeur()
    
    if y-radius < 110: # Collision du sol
        return True
    
    if y+radius > height: # Collision du plafond
        return True
    
    if x+radius > spikex and x-radius < spikex:
        if y+radius < spikealtitude or y-radius > spikealtitude+spikehole+bouthauteur:
            return True 
        
    if x+radius > spikex-boutlargeur and x-radius < spikex-boutlargeur:
        if y-radius < spikealtitude and y+radius > spikealtitude:
            return True
        if y+radius > spikealtitude+spikehole and y-radius < spikealtitude+spikehole+bouthauteur:
            return True
    
    if x+radius > spikex-boutlargeur and x-radius < spikex+spikelarge+boutlargeur:
        if y+radius > spikealtitude+spikehole and y-radius < spikealtitude+spikehole:
            return True
        if y-radius < spikealtitude and y+radius > spikealtitude:
            return True
        
    return False

def reset():
    bird.setY(500)
    bird.setVy(0)
    
    return [], 0, score if score > highscore else highscore, 0, 0, False, True

bird = Bird(150, 500, 0, 15)
spikes_= []

horizontalspeed = 3  # Vitesse des spikes
mooving = False      # Les spikes bougent ou pas
ecart = 100          # Ecart entre deux tuyaux
spikehole = 150      # Ecart du trou
spikelarge = 50      # Epaisseur du tuyau
bout_hauteur = 25    # Epaisseur de la fin du tuyau
bout_largeur = 15    # Largeur de la fin du tuyau

t = 1
move = 0
lenobj = 0
score = 0
highscore = 0

def draw(): 
    global t, horizontalspeed, move, lenobj, score, spikes_, mooving, highscore
    
    background(36, 195, 255)
    image(backimage, 0, 0, width, height)
    rotateX(PI)
    translate(0, -height)
    
    fill(229, 135, 72)
    rect(0, 0, width, 100)
    fill(68, 224, 69)
    rect(0, 100, width, 10)
    
    bird.calculNewPos(t, -0.4)
    bird.draw(birdpng)

    if move%ecart == 0:
        createSpike()
        lenobj += 1
        
    i = 0
    while i < lenobj:
        spikes_[i].draw(horizontalspeed, mooving)
        
        if spikes_[i].getX()+spikelarge+bout_largeur <= 0:
            spikes_.remove(spikes_[i])
            lenobj-=1
            score+=1
            i-=1
        i+=1
        
    fill(0)
    strokeWeight(2)
    rotateX(PI)
    textAlign(LEFT)
    text("Meilleur Score : {}".format(highscore), 20, -height+30)
    text("Score : {}".format(score), 20, -height+60)
    
    if mooving == False and score >= 5:
        mooving = True
        
    move+=t          
        
    if len(spikes_) > 0 and collision(spikes_[0]):
        spikes_, score, highscore, move, lenobj, mooving, pause = reset()
    
    textAlign(RIGHT)
    text("FPS : {}".format(frameRate), width-20, -height+30)
    
def keyPressed():    
    if key == " ":
        bird.jump(7, t)
