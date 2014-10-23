#!/usr/bin/env/python3
#Esther Schenau, Cameron Miller
#-----Collection of Lists-------

class Election(object): 
	def __init__(self):
		self.list_candidates = []
		self.list_ballots = []
		self.hasWinner = False
		self.hasTie = False
		self.winner = []
	def add_candidate(self, candidate):
		self.list_candidates.append(candidate)
	def add_ballot(self, ballot):
		self.list_ballots.append(ballot)
	def return_Candidates(self): 
		return self.list_candidates
	def look_for_winner (self):
		if len(self.list_candidates) == 1:
			self.hasWinner = True
			self.list_candidates[0].isWinner = True
		else:
			for t in range(len(self.list_candidates)):
				if not self.list_candidates[t].isInRunning:
					continue
				assert self.list_candidates
				if self.list_candidates[t].count_ballots() > .5 * len(self.list_ballots):
					self.hasWinner = True
					self.list_candidates[t].isWinner = True 
					for candidate in self.list_candidates[:t]:
						candidate.isInRunning = False
					for candidate in self.list_candidates[t + 1:]:
						candidate.isInRunning = False
					self.winner = [self.list_candidates[t].name]
		return self.hasWinner
	def look_for_tie (self):
		tie_check = [self.list_candidates[0].count_ballots() == candidate.count_ballots() for candidate in self.list_candidates[1:] if candidate.isInRunning]
		theres_a_tie = True
		for check in tie_check:
			theres_a_tie = theres_a_tie and check
		if theres_a_tie:
			for candidate in self.list_candidates:
				if candidate.isInRunning:
					candidate.isWinner = True
				self.winner = [cand.name for cand in self.list_candidates if cand.isInRunning]
		self.hasTie = theres_a_tie
		return theres_a_tie
	def mark_the_losers (self):
		loss_threshold = min(t.count_ballots() for t in self.list_candidates if t.isInRunning)
		for cand in self.list_candidates:
			if cand.count_ballots() <= loss_threshold:
				cand.isInRunning = False
	def pass_votes (self):
		losers = [t for t in self.list_candidates if not t.isInRunning]
		for non_candidate in losers:
			for ballot in non_candidate.ballots:
				assert ballot in non_candidate.ballots
				non_candidate.take_ballot(ballot)
				while not self.list_candidates[ballot.votes[ballot.owner] - 1].isInRunning:
					ballot.owner += 1
					self.list_candidates[ballot.votes[ballot.owner] - 1].give_ballot(ballot)

class Candidate (object):
	def __init__ (self, name):
		self.name = name
		self.ballots = []
		self.isInRunning = True
		self.isWinner = False
	def give_ballot (self, ballot):
		self.ballots.append(ballot)
	def take_ballot (self, ballot):
		self.ballots.remove(ballot)
	def count_ballots (self):
		return len(self.ballots)

class Ballot (object):
	def __init__ (self, preferences):
		self.votes = tuple(preferences)
		self.owner = 0
	def show_ballot (self): 
		print (self.votes)

def read_file (reader):
	for line in reader:
		yield line

def RunElection(election):
	while not (election.hasWinner or election.hasTie):
		winner = election.look_for_winner()
		if not winner:
			tie = election.look_for_tie()
		if not (winner or tie):
			election.mark_the_losers()
			election.pass_votes()

def VotingSolve(aReader,aWriter):
	line = read_file(aReader)
	reached_EOF = False
	number_of_elections = None
	index_election = -1
	while not reached_EOF:
		try:
			render_line = next(line).strip()
		except StopIteration:
			reached_EOF = True
			continue
		if render_line == '':
			if -1 < index_election < number_of_elections:
				RunElection(list_elections[index_election])
			index_election += 1
		elif render_line.isdigit():
			if not number_of_elections:
				number_of_elections = int(render_line)
				list_elections = [Election() for i in range(number_of_elections)]
			else:
				list_elections[index_election].number_of_candidates = int(render_line)
		elif render_line[-1].isdigit():
			rerender_line = [int(t) for t in render_line.split()]
			ballotize = Ballot(rerender_line)
			list_elections[index_election].add_ballot(ballotize)
			list_elections[index_election].list_candidates[ballotize.votes[0] - 1].give_ballot(ballotize)
		else:
			list_elections[index_election].add_candidate(Candidate(render_line))
	else:
		RunElection(list_elections[index_election])
	for election in list_elections: 
		for candidate in election.winner:
			print (candidate)
		print () 