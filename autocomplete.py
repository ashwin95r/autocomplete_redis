import redis
import sys
import os

NUM_SUGGEST = 10
dic = open(sys.argv[1])
r = redis.StrictRedis(host = "localhost", port = 6379, db = 0)
r.flushdb()

def clear():
	os.system('cls' if os.name=='nt' else 'clear')


def add_words_to_dict():
	if r.exists('prefix_dict') != True:
		for line in dic:
			word = line.strip()
			for i in range(1, len(word)):
				pre_word = word[0:i]
				r.zadd('prefix_dict', 0, pre_word)
				#print pre_word
			r.zadd('prefix_dict', 0, word + '#')


if __name__ == "__main__":
	add_words_to_dict()
	word = ''
	ch = raw_input()
	while ch != '':
		clear()
		word = word + ch
		print "You typed : " + word
		rank = r.zrank('prefix_dict', word)	
		if rank == None:
			print "No suggestions"
			pass;
		else:
			ra = r.zrange('prefix_dict', rank, rank+100)
			print "suggestions : "
			mi = min(len(word), len(ra[0]))
			i = 0
			count = 0
			while True:
				if ra[i][-1] == '#':
					print ra[i][:-1]
					count = count + 1
				i = i + 1;
				if i<len(ra) and count < NUM_SUGGEST and word[:mi] == ra[i][:mi]:
					pass
				else:
					break
				mi = min(len(word), len(ra[i]))				
		ch = raw_input()				

