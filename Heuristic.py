



""""
Types of lines: Rows, Columns, Diagonals
Features to search for in the board and their respective scores:

1. 4 pieces or more = 1 (+1 per extra piece) (don't call on mirrored line)

2. 3 pieces then empty then 0 or more pieces = 0.5 (+0.5 per extra piece)

3. 2 pieces then 2 empties = 0.25 

4. 2 pieces then empty then 1 or 2 pieces = 0.5 or 1 

5. 1 piece with 3 empties around it = 0.125 (don't call on mirrored line)

6. 1 piece then next 3 places are empty exept place 2 or 3 has player piece = 0.25

7. 4 pieces then empty then 0 or more pieces = 4 (+0.5 per extra piece)

Note that searching for these features should be done left-to-right and right-to-left to not miss any features.
When looking for a feature with an empty piece, make sure the peice below it isn't empty
"""

matrix: list



def heuristic(board: list, aiPiece, humanPiece) -> float:
	global matrix
	matrix = board
	ai_h = get_h_for_player(aiPiece)
	human_h = get_h_for_player(humanPiece)
	return ai_h - human_h



def get_h_for_player(player: int) -> float:
	score: float
	lines: list = get_rows()
	lines.append(get_cols())
	lines.append(get_neg_diags())
	lines.append(get_pos_diags())

	for line in lines:
		score += line.find_feat1(line, player)
		score += line.find_feat2(line, player)
		score += line.find_feat3(line, player)
		score += line.find_feat4(line, player)
		score += line.find_feat5(line, player)
		score += line.find_feat6(line, player)
		line.reverse()
		score += line.find_feat2(line, player)
		score += line.find_feat3(line, player)
		score += line.find_feat4(line, player)
		score += line.find_feat6(line, player)
	return score


def find_feat1(line: list, player: int) -> float:
	count: int = 0
	score: float = 0
	for loc in line:
		piece = matrix[loc[0]][loc[1]]
		if piece == player: count += 1
		else: 
			if count >= 4:
				break
			count = 0
	score += count - 3
	return score


def find_feat2(line: list, player: int) -> float:
	count3: int = 0
	emptyFound = False
	score: float = 0
	i: int
	for i in range(len(line)):
		loc = line[i]
		piece = matrix[loc[0]][loc[1]]
		if count3 < 3:
			if piece == player: count3 += 1
			else: count3 = 0
		else:
			if piece == 0 and matrix[loc[0]+1][loc[1]] != 0: #If this piece is empty and below it is filled.
				emptyFound = True
				i += 1
				score = 0.5
				break
			else: return 0
	
	while i != len(line) and emptyFound:
		loc = line[i]
		piece = matrix[loc[0]][loc[1]]
		if piece != player: break
		else:
			score += 0.5
			i += 1
	return score


def find_feat3(line: list, player: int) -> float:
	count2: int = 0 
	score: float = 0
	i: int = 0
	for i in range(len(line)):
		loc = line[i]
		piece = matrix[loc[0]][loc[1]]
		if count2 != 2:
			if piece == player: count2 += 1
			else: count2 = 0
		else:
			if i == len(line) - 1: break
			nexLoc = line[i+1]
			nextPiece = matrix[nexLoc[0]][nexLoc[1]]
			if piece == 0 and matrix[loc[0]+1][loc[1]] != 0 and nextPiece == 0 and matrix[nexLoc[0]+1][nexLoc[1]] != 0:
				score = 0.25
				break	
			else: break
	return score


#4. 2 pieces then empty then 1 or 2 pieces maximum = 0.5 or 1 
def find_feat4(line: list, player: int) -> float:
	score: float = 0
	count2: int = 0
	extraCount = 0
	i = 0
	for i in range(len(line)):
		loc = line[i]
		piece = matrix[loc[0]][loc[1]]
		if count2 != 2:
			if piece != player: count2 = 0
			else: count2 += 1
		else:
			if piece == 0 and matrix[loc[0]+1][loc[1]] != 0:
				if i == len(line) - 1: break
				nextLoc = line[i+1]
				nextPiece = matrix[nextLoc[0]][nextLoc[1]]
				if nextPiece == 0: break
				for j in range(i+1, len(line)):
					loc2 = line[j]
					piece2 = matrix[loc2[0]][loc2[1]]
					if piece2 == player: extraCount += 1
					if extraCount > 2:
						extraCount = 0
						break
				score = 0.5 * extraCount
				break
			else: break
	return score


#5. 1 piece then 3 empties = 0.125
def find_feat5(line: list, player: int) -> float:
	return 0
	score: float = 0
	i = 0
	while i < len(line) - 3:
		loc = line[i]
		piece = matrix[loc[0]][loc[1]]
		if piece == player: # If encounters 1 player piece
			i += 1
			loc = line[i]
			piece = matrix[loc[0]][loc[1]]
			if piece == player: #If 2 player pieces together.
				#Continue until you reach a non-player piece 
				i += 1
				while i < len(line):
					loc = line[i]
					piece = matrix[loc[0]][loc[1]]
					if piece != player: #If encountered a non player piece then start looking for a single piece again 
						i += 1
						break
					else: i += 1
			elif piece == 0 and matrix[loc[0]+1][loc[1]] != 0: #Found player piece alone
				emptyCount = 1
				i += 1
				#Look left

				#Look right
				while i < len(line): #Count empty pieces
					loc = line[i]
					piece = matrix[loc[0]][loc[1]]
					if piece == 0: 
						emptyCount += 1
						i += 1
					else:
						break
				if emptyCount >= 3:
					score = 0.125
					break
			else: #Second piece is opponent
				i += 1
				continue
		else: i+= 1	

	return score
		

def find_feat6(line: list, player: int) -> float:
	
	
	return 0


def get_rows() -> list:
	rows: list = []
	for y in range(len(matrix)):
		row: list = []
		for x in range(len(matrix[0])):
			row.append((y,x))
		rows.append(row)
	return rows

def get_cols() -> list:
	cols: list = []
	for x in range(len(matrix[0])):
		col: list = []
		for y in range(len(matrix)):
			col.append((y,x))
		cols.append(col)
	return cols

def get_pos_diags() -> list:
	diags: list = []
	for i in range(3):
		diag: list = []
		j = 6
		while j >= 0 and i < 6:
			diag.append((i,j))
			i += 1
			j -= 1
		diags.append(diag)
	for j in range(3,6):
		diag: list = []
		i = 0
		while j >= 0  and i < 6:
			diag.append((i,j))
			i += 1
			j -= 1
		diags.append(diag)
	return diags

def get_neg_diags() -> list:
	diags: list = []
	for i in range(3):
		diag: list = []
		j = 0
		while j < 7 and i < 6:
			diag.append((i,j))
			i += 1
			j += 1
		diags.append(diag)
	for j in range(1,4):
		diag: list = []
		i = 0
		while j < 7 and i < 6:
			diag.append((i,j))
			i += 1
			j += 1
		diags.append(diag)
	return diags


def count_empties_around(loc: tuple, line: list) -> int:
	return 0