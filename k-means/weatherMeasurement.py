import numpy
import random
from scipy.spatial import distance

class WeatherMeasurement:
   'Base class for datapoints'
   date = None
   label = None
   centroid = None
   centroidDistance = None

   def __init__(self, fg, tg, tn, tx, sq, dr, rh):
      self.fg = fg
      self.tg = tg
      self.tn = tn
      self.tx = tx
      self.sq = sq
      self.dr = dr
      self.rh = rh

   def setDate(self, date):
      self.date = date
      if self.date>=20010101:
         if self.date < 20010301:
            self.label='winter'
         elif 20010301 <= self.date < 20010601:
            self.label='lente'
         elif 20010601 <= self.date < 20010901:
            self.label='zomer'
         elif 20010901 <= self.date < 20011201:
            self.label='herfst'
         else: # from 01-12 to end of year
            self.label='winter'  
      else:         
         if self.date < 20000301:
            self.label='winter'
         elif 20000301 <= self.date < 20000601:
            self.label='lente'
         elif 20000601 <= self.date < 20000901:
            self.label='zomer'
         elif 20000901 <= self.date < 20001201:
            self.label='herfst'
         else: # from 01-12 to end of year
            self.label='winter'

   def removeLabeldata():
      self.date=None
      self.label=None

   def measureDistance(self, measurment):
      return numpy.linalg.norm(
         numpy.array((
         self.fg,
         self.tg,
         self.tn,
         self.tx,
         self.sq,
         self.dr,
         self.rh))
         -
         numpy.array((
         measurment.fg,
         measurment.tg,
         measurment.tn,
         measurment.tx,
         measurment.sq,
         measurment.dr,
         measurment.rh)))
      
   def random():
      return WeatherMeasurement(
         random.randrange(0, 101),
         random.randrange(0, 101),
         random.randrange(0, 101),
         random.randrange(0, 101),
         random.randrange(0, 101),
         random.randrange(0, 101),
         random.randrange(0, 101),
         )

   def __str__(self):
      if (not self.label):
         return (
         "\n" + "================" + "\n"
         "fg: " + str(self.fg) + "\n" +
         "tg: " + str(self.tg) + "\n" +
         "tn: " + str(self.tn) + "\n" +
         "tx: " + str(self.tx) + "\n" +
         "sq: " + str(self.sq) + "\n" +
         "dr: " + str(self.dr) + "\n" +
         "rh: " + str(self.rh) + "\n" +
         "================" + "\n"
         )

      return (
         "\n" + "================" + "\n"
         "Date: " + str(self.date) + "\n" +
         "Label: " + self.label + "\n" +
         "fg: " + str(self.fg) + "\n" +
         "tg: " + str(self.tg) + "\n" +
         "tn: " + str(self.tn) + "\n" +
         "tx: " + str(self.tx) + "\n" +
         "sq: " + str(self.sq) + "\n" +
         "dr: " + str(self.dr) + "\n" +
         "rh: " + str(self.rh) + "\n" +
         "================" + "\n"
         )
   def __add__(self,other):
      fg = self.fg + other.fg
      tg = self.tg + other.tg
      tn = self.tn + other.tn
      tx = self.tx + other.tx
      sq = self.sq + other.sq
      dr = self.dr + other.dr
      rh = self.rh + other.rh
      return WeatherMeasurement(fg,tg,tn,tx,sq,dr,rh)