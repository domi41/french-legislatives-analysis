import csv
from typing import List


class Candidate:
	name: str
	votes_t1: int
	votes_t2: int

	def __init__(self):
		self.votes_t1 = 0
		self.votes_t2 = 0

	def __str__(self) -> str:
		return f'{self.name} ({self.votes_t1} → {self.votes_t2})'


class CirconscriptionElection:
	year: int
	locality_code: str  # code département
	circonscription: int
	candidates: List[Candidate]

	def __init__(self):
		self.candidates = []

	def __str__(self) -> str:
		s: str = f'{self.year} - dept {self.locality_code} - circo {self.circonscription}'
		# s += f' : '
		# for i, candidate in enumerate(self.candidates):
		# 	if i > 3:
		# 		break
		# 	if i > 0:
		# 		s += f' | '
		# 	s += f'{candidate.name}'
		return s

	def find_candidate_by_name(self, name: str) -> Candidate:
		for candidate in self.candidates:
			if candidate.name == name:
				return candidate
		available = '\n'.join(map(lambda c: c.name, self.candidates))
		raise ValueError(f'Candidate {name} not found.\nAvailable candidates:\n{available}')

	def get_sorted_candidates_t1(self):
		return sorted(self.candidates, key=lambda candidate: candidate.votes_t1, reverse=True)

	def get_sorted_candidates_t2(self):
		return sorted(self.candidates, key=lambda candidate: candidate.votes_t2, reverse=True)


class Elections:
	elections: List[CirconscriptionElection]

	def __init__(self):
		self.elections = []

	def find_election(self, locality_code: str, circonscription: int) -> CirconscriptionElection:
		for election in self.elections:
			if (
				election.locality_code == locality_code
				and
				election.circonscription == circonscription
			):
				return election

		raise ValueError(f'Election not found')


common_headers = [
	'Code département',
	'département',
	'circonscription',
	'élu premier tour',
	'Inscrits',
	'Votants',
	'Exprimés',
	'Blancs et nuls',
	'Taux de participation (%)',
]


def process_year(year: int, dumb_format: bool = False):

	elections: Elections = Elections()
	turn = 1
	data_file_path = f"data/cdsp_legi{year}t{turn}_circ.csv"
	with open(data_file_path) as csv_file:
		# csv_reader = csv.reader(csv_file)
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			#print(row)

			if row['Code département'] == '':
				# print(f"Skipping acronyms row…")
				continue

			election = CirconscriptionElection()
			election.year = year
			election.locality_code = (row['Code département'])
			election.circonscription = int(row['circonscription'])

			if dumb_format:
				for i in range(1, 4):
					candidate_name = row[f'{i} Etiquette liste']
					if not candidate_name:
						break
					candidate_votes = int(row[f'{i} voix'])
					candidate = Candidate()
					candidate.name = candidate_name
					candidate.votes_t1 = candidate_votes
					election.candidates.append(candidate)
			else:
				for key in row:
					if key in common_headers:
						continue
					candidate = Candidate()
					candidate.name = key
					candidate.votes_t1 = int(row[key])
					election.candidates.append(candidate)

			elections.elections.append(election)


	turn = 2
	data_file_path = f"data/cdsp_legi{year}t{turn}_circ.csv"
	with open(data_file_path) as csv_file:
		# csv_reader = csv.reader(csv_file)
		csv_reader = csv.DictReader(csv_file)

		for row in csv_reader:

			if row['Code département'] == '':
				# print(f"Skipping acronyms row…")
				continue

			election_locality = (row['Code département'])
			election_circonscription = int(row['circonscription'])
			election = elections.find_election(election_locality, election_circonscription)
			#print(row)

			# for key in row:
			# 	if key in common_headers:
			# 		continue

				# for i in range(1, 4):
				# 	candidate_name = row[f'{i} Etiquette liste']
				# 	candidate_votes = row[f'{i} voix']
			if dumb_format:
				for i in range(1, 4):
					candidate_name = row[f'{i} Etiquette liste']
					if not candidate_name:
						break
					candidate_votes = int(row[f'{i} voix'])

					candidate = election.find_candidate_by_name(candidate_name)
					candidate.votes_t2 = candidate_votes

			else:
				for key in row:
					if key in common_headers:
						continue
					candidate_name = key
					candidate_votes = int(row[key] or 0)
					candidate = election.find_candidate_by_name(candidate_name)
					candidate.votes_t2 = candidate_votes



	surprises: List[CirconscriptionElection] = []

	for election in elections.elections:
		candidates_t1 = election.get_sorted_candidates_t1()
		candidates_t2 = election.get_sorted_candidates_t2()

		if candidates_t2[0] not in candidates_t1[0:2]:
			# print("Elected candidate was not in top two !")
			surprises.append(election)

	for election in surprises:
		candidates_t1 = election.get_sorted_candidates_t1()
		candidates_t2 = election.get_sorted_candidates_t2()
		# datum = []
		rank_t2 = 0
		print(election)
		for candidate in candidates_t2:
			rank_t1 = candidates_t1.index(candidate) + 1
			rank_t2 += 1

			print(f"#{rank_t2} {candidate.name} (was #{rank_t1})")

			if rank_t2 > 5:
				break

		# print('-----')

	percent_of_surprises = 100 * len(surprises) / float(len(elections.elections))
	print()
	print(f"{year}: found {len(surprises)} surprises ({percent_of_surprises:.1f}% des {len(elections.elections)}) on the second turn.")



if __name__ == '__main__':
	# process_year(1958)
	# process_year(1962)
	# process_year(1967)
	# process_year(1968)
	# process_year(1973)
	# process_year(1978)
	process_year(1981)
	# process_year(1988, dumb_format=True)
	# process_year(1993, dumb_format=True)
