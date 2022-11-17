



""""
Types of lines: Rows, Columns, Diagonals
Features to search for in the board and their respective scores:

1. 4 pieces or more = 1 (+1 per extra piece) (don't call on mirrored line)

2. 3 pieces then empty then 0 or more pieces = 0.5 (+0.5 per extra piece)

3. 2 pieces then 2 empties = 0.25 (special case with cols required)

4. 2 pieces then empty then 1 or 2 pieces = 0.5 or 1 (not in cols)

5. 1 piece with 3 empties around it = 0.125 (special case with cols required) (don't call on mirrored line)

6. 1 piece then next 3 places are empty except place 2 or 3 has player piece = 0.25 (not in cols) (don't call on mirrored line)

7. 4 pieces then empty then 1 or more pieces = 1.5 (+0.5 per extra piece) (not in cols)

8. 5 pieces then empty then 1 or more pieces = 2.5 (+0.5 per extra piece) (not in cols)

Note that searching for these features should be done left-to-right and right-to-left to not miss any features.
When looking for a feature with an empty piece, make sure the peice below it isn't empty
"""

matrix: list

def heuristic(board: list, aiPiece, humanPiece) -> float:
	global matrix
	matrix = board
	ai_h = get_h_for_player(aiPiece)
	human_h = get_h_for_player(humanPiece)
	#print(ai_h, human_h)
	return ai_h - human_h



def get_h_for_player(player: int) -> float:
	score: float = 0
	lines: list = get_rows()
	lines = lines + get_neg_diags() + get_pos_diags()
	cols: list = get_cols()
	for line in lines:
		score += find_feat1(line, player)
		score += find_feat2(line, player)
		score += find_feat3(line, player)
		score += find_feat4(line, player)
		score += find_feat5(line, player)
		score += find_feat6(line, player)
		score += find_feat7(line, player)
		line.reverse()
		score += find_feat2(line, player)
		score += find_feat3(line, player)
		score += find_feat4(line, player)
		score += find_feat7(line, player)
	for col in cols:
		col.reverse()
		score += find_feat1(col, player)
		score += find_feat2(col, player)
		score += find_feat3_col(col, player)
		score += find_feat5_col(col, player)
	
	return score


#1. 4 pieces or more = 1 (+1 per extra piece) (don't call on mirrored line)
def find_feat1(line: list, player: int) -> float:
	count: int = 0
	score: float = 0
	i = 0
	while i < len(line):
		count = count_piece(player, line, i)
		if count >= 4: break
		elif count == 0: i += 1
		else:
			i += count
			count = 0
	
	score = max(count - 3, 0)
	return score


#2. 3 pieces then empty then 0 or more pieces = 0.5 (+0.5 per extra piece)
def find_feat2(line: list, player: int) -> float:
	emptyFound = False
	score: float = 0
	i = 0
	while i < len(line):
		loc = line[i]
		count3 = count_piece(player, line, i)
		if count3 == 0:
			i += 1
			continue
		elif count3 != 3:
			i += count3
			continue
		else:
			i += count3
			if i >= len(line): break
			loc = line[i]
			if is_piece_available(loc):
				score = 0.5 + 0.5 * count_piece(player, line, i+1)
				break
			else:
				continue
	
	return score

#3. 2 pieces then 2 empties = 0.25 
def find_feat3(line: list, player: int) -> float:
	count: int = 0 
	score: float = 0
	i: int = 0
	while i < len(line):
		count = count_piece(player, line, i)
		if count == 0: i += 1
		elif count != 2: i += count
		else:
			i += count
			if i == len(line) - 1: break
			emptyCount = count_piece(0, line, i)
			if emptyCount >= 2:
				score = 0.25
				break
			else: i += 1
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
			if piece == 0 and is_piece_available(loc):
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


#5. 1 piece with 3 empties around it = 0.125
def find_feat5(line: list, player: int) -> float:
	score: float = 0
	i = 0
	while i < len(line):
		count = count_piece(player, line, i)
		if count == 0:
			i += 1
		elif count != 1:
			i += count
		else:
			if i >= len(line): break
			emptyCount = count_empties_around(i, line)
			if emptyCount >= 3:
				score = 0.125
				break
			else: i += 1
	return score
		

#6. 1 piece then next 3 places are empty except place 2 or 3 has player piece = 0.25
def find_feat6(line: list, player: int) -> float:
	score: float = 0
	i = 0
	while i < len(line) - 3:
		count = count_piece(player, line, i)
		if count == 0:
			i += 1
		elif count != 1:
			i += count
		else:
			i += 1
			loc = line[i]
			loc2 = line[i+1]
			loc3 = line[i+2]
			if not is_piece_available(loc): continue
			if is_piece_available(loc2):
				if matrix[loc3[0]][loc3[1]] == player: score = 0.25
			elif matrix[loc2[0]][loc2[1]] == player:#piece at place 2
				if is_piece_available(loc3): score = 0.25
			else: continue		
	return 0


#7. 4 pieces then empty then 1 or more pieces = 1.5 (+0.5 per extra piece)
def find_feat7(line: list, player: int) -> float:
	count: int = 0
	score: float = 0
	i = 0
	while i < len(line):
		count = count_piece(player, line, i)
		if count == 4:
			i += count
			if i >= len(line): break
			loc = line[i]

			if is_piece_available(loc):
				extraCount = count_piece(player, line, i+1)
				score += 0.5*extraCount
				break
		elif count == 0: i += 1
		else:
			i += count
			count = 0
	return score


#3. 2 pieces then 2 empties = 0.25 
def find_feat3_col(line: list, player: int) -> float:
	score: float = 0
	i: int = 0
	while i < len(line):
		count = count_piece(player, line, i)
		if count == 0: i += 1
		elif count != 2: i += count
		else:
			i += count
			if i >= len(line) - 1: break
			loc = line[i]
			
			if matrix[loc[0]][loc[1]] == 0 and i <= len(line) - 2:
				score = 0.25
				break
			else: i += 1
	return score

#5. 1 piece then 3 empties
def find_feat5_col(line: list, player: int) -> float:
	score = 0
	i = 0
	while i < len(line)-3:
		loc = line[i]
		loc2 = line[i+1]
		if matrix[loc[0]][loc[1]] == player and matrix[loc2[0]][loc2[1]]:
			score = 0.125
			break
		else: i += 2
	return score



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


def count_empties_around(loc_index: int, line: list) -> int:
	emptyCount = 0
	end1 = False
	end2 = False
	i1 = loc_index
	i2 = loc_index
	

	while not (end1 and end2):
		if not end1:
			i1 -= 1
			if i1 < 0: end1 = True
			else:
				loc1 = line[i1]
				if is_piece_available(loc1): 
					emptyCount += 1
					
				else: end1 = True
		if not end2:
			i2 += 1
			if i2 >= len(line): end2 = True
			else:
				loc2 = line[i2]
				if is_piece_available(loc2): 
					emptyCount += 1
				else: end1 = True
	return emptyCount


def count_piece(pieceType: int, line: list, startIndex: int) -> int:
	stopIndex = startIndex
	while stopIndex < len(line):
		loc = line[stopIndex]
		piece = matrix[loc[0]][loc[1]]
		if pieceType == 0 and not is_piece_available(loc): break
		elif piece != pieceType: break
		else:
			stopIndex += 1
			if stopIndex == len(line): break
	return stopIndex - startIndex


def is_piece_available(loc: tuple) -> bool:
	piece = matrix[loc[0]][loc[1]]
	if piece == 0 and (loc[0] == 5 or matrix[loc[0]+1][loc[1]] != 0):
		return True
	else:
		return False