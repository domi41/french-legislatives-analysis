from typing import List


class Candidate:
	name: str
	votes: int


class CirconscriptionElection:
	year: int
	locality_code: int  # code département
	circonscription: int
	candidates: List[Candidate]

	def __init__(self):
		self.candidates = []

	def __str__(self) -> str:
		s: str = f'{self.year} - {self.locality_code:02d} - {self.circonscription}'
		s += f' : '
		for i, candidate in enumerate(self.candidates):
			if i > 3:
				break
			if i > 0:
				s += f' | '
			s += f'{candidate.name}'
		return s

	def sort_candidates(self):
		self.candidates = sorted(self.candidates, key=lambda candidate: candidate.votes, reverse=True)


common_headers = [
	'Code département',
	'département',
	'circonscription',
	'élu premier tour',
	'Inscrits',
	'Votants',
	'Exprimés',
	'Blancs et nuls',
]

import csv

elections: List[CirconscriptionElection] = []

year = 1958
turn = 1
data_file_path = f"data/cdsp_legi{year}t{turn}_circ.csv"
with open(data_file_path) as csv_file:
	# csv_reader = csv.reader(csv_file)
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		print(row)

		if row['Code département'] == '':
			print(f"Skipping acronyms row…")
			continue

		election = CirconscriptionElection()
		election.year = year
		election.locality_code = int(row['Code département'])
		election.circonscription = row['circonscription']

		for key in row:
			if key in common_headers:
				continue
			candidate = Candidate()
			candidate.name = key
			candidate.votes = row[key]
			election.candidates.append(candidate)

		elections.append(election)

for election in elections:
	election.sort_candidates()
	print(election)
