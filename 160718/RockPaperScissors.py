import unittest;

# Task outline:

# First pomodoro
#
# 3 classes
# superclass Thing
# all have a method "beats" takes an object
# of class Thing (or a subclass) and returns
# True, False or None
#
# Second pomodoro
# 
# Change the classes so that of all the 
# conditionals are gotten rid of.
#
# Third pomodoro
#
# Extension: the "Lizard Spock" way.
# see https://en.wikipedia.org/wiki/Rock-paper-scissors#Additional_weapons

# remarks:
# we don't actually need classes for this - these are simply enums
#
# we could just test the "beats" method in isolation - as there are many test 
# cases, and there is a very simple implementation, it is probably more 
# reasonable to incorporate the 'beats' logic into the Thing class as 
# parameters, maybe a class, which 

class Thing:

  # initializes the class to use the default logic when evaluating who wins
  @classmethod
  def set_default_rules(cls):
    Thing.set_rules(
      {(Thing, Rock): None,
       (Rock, Scissors): True,
       (Rock, Lizard): True,
       (Paper, Rock): True,
       (Paper, Spock): True,
       (Scissors, Paper): True,
       (Scissors, Lizard): True,
       (Spock, Scissors): True,
       (Spock, Rock): True,
       (Lizard, Spock): True,
       (Lizard, Paper): True}
    )

  # automatically extends the ruleset for consistency and assigns it to the 
  # class of Things
  @classmethod
  def set_rules(cls, who_beats_who):
    things_1 = {pair[0] for pair in who_beats_who}
    things_2 = {pair[1] for pair in who_beats_who}
    things = things_1.union(things_2)

    # add asymmetry (if A beats B then B is beaten by A)
    for pair, beats in who_beats_who.items():
      if beats is not None:
        (A, B) = pair
        who_beats_who[(B, A)] = not beats

    # add "diagonal" (thing - thing: undecisive, i.e. tie)
    for thing in things:
      who_beats_who[(thing, thing)] = None

    # add tie against a generic Thing
    for thing in things:
      who_beats_who[(Thing, thing)] = None
      who_beats_who[(thing, Thing)] = None

    Thing.__who_beats_who__ = who_beats_who

  def beats(self, another_thing):
    return(Thing.__who_beats_who__[(self.__class__, \
                                    another_thing.__class__)])

class Rock(Thing): pass

class Scissors(Thing): pass

class Paper(Thing): pass

class Lizard(Thing): pass

class Spock(Thing): pass

class TestThings(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    Thing.set_default_rules()

  def assert_beats(self, class1, class2, result):
    t1 = class1()
    t2 = class2()
    self.assertEquals(t1.beats(t2), result)

  def test_Thing_ties_Thing(self):
    self.assert_beats(Thing, Thing, None)

  def test_Thing_ties_Rock(self):
    self.assert_beats(Thing, Rock, None)

  def test_Rock_ties_Rock(self):
    self.assert_beats(Rock, Rock, None)

  def test_Rock_beats_Scissors(self):
    self.assert_beats(Rock, Scissors, True)

  def test_Scissors_beatenby_Rock(self):
    self.assert_beats(Scissors, Rock, False)

  def test_Paper_beats_Rock(self):
    self.assert_beats(Paper, Rock, True)

  def test_Paper_beats_Spock(self):
    self.assert_beats(Paper, Spock, True)

  def test_Rock_beats_Lizard(self):
    self.assert_beats(Rock, Lizard, True)

  def test_Scissors_beat_Lizard(self):
    self.assert_beats(Scissors, Lizard, True)

  def test_Spock_beats_Scissors(self):
    self.assert_beats(Spock, Scissors, True)

  def test_Spock_beats_Rock(self):
    self.assert_beats(Spock, Rock, True)

  def test_Lizard_beats_Spock(self):
    self.assert_beats(Lizard, Spock, True)

  def test_Lizard_beats_Paper(self):
    self.assert_beats(Lizard, Paper, True)


if __name__ == "__main__":
  unittest.main()
