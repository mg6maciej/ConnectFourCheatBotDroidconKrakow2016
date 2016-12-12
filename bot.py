import socket
import dryscrape
import re
import random
import time

pattern = re.compile("<div id=\"sol(\d)[^\n]*>(-?\d+)</div>")

data = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("platinum.edu.pl", 4242))
s.send("NAME mg6maciej\n")
s.send("JOIN droidcon\n")
session = dryscrape.Session()
while True:
  newData =  s.recv(1024)
  if not newData: break
  data += newData
  print "data:", data
  index = data.find('\n')
  while index >= 0:
    command = data[:index]
    data = data[index+1:]
    print "command:", command
    if command == "YOUR_MOVE":
      while True:
        session.visit("http://connect4.gamesolver.org/?pos=" + moves)
        time.sleep(3)
        response = session.body()
        #print response
        res = pattern.findall(response)
        #print res
        if len(res) > 0:
          break
        time.sleep(1)
      res2 = [(int(x[0]), int(x[1])) for x in res]
      #print res2
      for i in reversed(range(len(res2))):
        if moves.count(str(res2[i][0] + 1)) == 6:
          del res2[i]
      print res2
      mx = max(x[1] for x in res2)
      print mx
      bestMoves = [x[0] for x in res2 if x[1] == mx]
      print bestMoves
      pick = random.randint(0, len(bestMoves)-1)
      #print "picked move:", pick
      pickedMove = bestMoves[pick]
      print "picked move2:", pickedMove
      s.send("PUT " + str(pickedMove) + "\n")
      moves += str(pickedMove + 1)
      #print "send put"
    elif command == "NEW_GAME":
      moves = ""
    elif command[:4] == "PUT ":
      moves += str(1+int(command[4:]))
      print "moves:", moves
    index = data.find('\n')
