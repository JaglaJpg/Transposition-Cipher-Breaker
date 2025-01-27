import random


class Cipher:

  def __init__(self, key):
    self.key = key

  def Encrypt(self, msg):

    cols = len(self.key)
    rows = (len(msg) + cols - 1) // cols
    pad = rows * cols - len(msg)
    msg += "_" * pad

    indices = [i for i in range(cols)]
    indices.sort(key=lambda x: self.key[x])

    lst = [msg[0 + cols * x:(cols + cols * x)] for x in range(rows)]
    matrix = []

    for x in lst:
      matrix.append([*x])

    ciphertext = []
    for x in range(cols):
      for y in matrix:
        ciphertext.append(y[indices.index(x)])

    return "".join(ciphertext)

  def Decrypt(self, ct, key):

    cols = len(key)
    rows = (len(ct) + cols - 1) // cols

    indices = [i for i in range(cols)]
    indices.sort(key=lambda x: key[x])

    matrix = [[0 for j in range(cols)] for i in range(rows)]

    for x in range(cols):
      y = ct[0 + rows * x:rows + rows * x]
      for _ in range(len(y)):
        matrix[_][indices.index(x)] = y[_]

    plain = ""
    for x in matrix:
      plain += "".join(x)

    return plain


class GeneticAlgorithm(Cipher):

  def __init__(self, popSize, target):
    self.popSize = popSize
    self.target = target

  def Generate(self, keyLen):
    a = "abcdefghijklmnopqrstuvwxyz"
    a = a[:keyLen]
    return "".join(random.sample(a, keyLen))

  def Fitness(self, key):

    digrams = {
      "TH": 3.88, "HE": 3.68, "IN": 2.28,
      "ER": 2.18, "AN": 2.14, "RE": 1.75,
      "ND": 1.57, "ON": 1.42, "EN": 1.38,
      "AT": 1.33, "OU": 1.28, "ED": 1.27,
      "HA": 1.27, "TO": 1.17, "OR": 1.15,
      "IT": 1.13, "IS": 1.11, "HI": 1.09,
      "ES": 1.09, "NG": 1.05
    }

    trigrams = {
      "THE": 3.67, "AND": 1.7, "ING": 1.06,
      "HER": 0.73, "YOU": 0.72, "VER": 0.69,
      "WAS": 0.66, "HAT": 0.58, "FOR": 0.56,
      "NOT": 0.56, "THI": 0.55, "THA": 0.54,
      "HIS": 0.49, "ENT": 0.48, "ION": 0.47,
      "ITH": 0.47, "ERE": 0.47, "WIT": 0.46,
      "ALL": 0.45, "EVE": 0.43
    }

    wrong = {"  ": -5, "   ": -5}

    score = 0
    plain = self.Decrypt(self.target, key)
    plain = plain.upper()
    for x in digrams:
      score += (plain.count(x)) * (digrams[x])
    for x in trigrams:
      score += (plain.count(x)) * (trigrams[x])
    for x in wrong:
      score += (plain.count(x)) * (wrong[x])
    if plain[0 - (plain.count("_")):] == "_" * plain.count("_"):
      score += 10
    return score

  def Swap(self, word):
    i = word.index(random.choice(word))
    j = word.index(random.choice(word))
    list1 = list(word)
    list1[i], list1[j] = list1[j], list1[i]
    return ''.join(list1)

  def Breed(self, par1, par2):
    gen = []
    t = self.popSize
    for x in range(t // 2):
      os1 = par1[0] + par1[1]
      os2 = par2[0] + par2[1]
      end1 = par1[2:]
      end2 = par2[2:]
      os1 += (end1[1:] + end1[0])
      os2 += (end2[1:] + end2[0])
      os1, os2 = self.Swap(os1), self.Swap(os2)
      gen.append(os1), gen.append(os2)
    return gen

  def Run(self, keyLen):
    st = ""
    index = 0
    optimal = (len(self.target)) * 2.5
    speed = optimal
    i = 1
    gen = 0
    pop = []
    pop = [self.Generate(keyLen) for x in range(self.popSize)]
    while True:
      index += 1
      gen += 1
      pop = sorted(pop, key=lambda x: self.Fitness(x))
      st += f"{pop[-1]}\n"
      if index % speed == 0:
        print(st)
        st = ""
      pop = self.Breed(pop[-1], pop[-2])
      if self.Fitness(pop[-1]) >= optimal:
        break
      elif gen == 200 * i:
        optimal -= 1
        i += 1
    return pop[-1]


key = "abcdefghijk"
tc = Cipher(key)
target = tc.Encrypt("I cant just think of anything dude")
ask = input(f"The encrypted msg is {target}, would you like to continue? ")
ga = GeneticAlgorithm(12, target)
print(f"The target is '{target}'\n The message is '{tc.Decrypt(target ,ga.Run(len(poopoo)))}'")
