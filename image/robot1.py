# class Robot(object):
# '''
#     基于五子棋规则写的一个机器人
# '''

#     def __init__(self, _board):
#         self.board = _board



    # def empty(chesslist, i, j, score):
    # 	if you_tuple[0] == you_tuple[1] == you_tuple[2] == you_tuple[3] == you_tuple[4] == []:
    # 		for k in range(5)
    # 			score[i + k, j] += 7
    # 	if xia_tuple[0] == xia_tuple[2] == xia_tuple[3] == xia_tuple[4] == xia_tuple[5] == []:
    # 		for k in range(5)
    # 			score[i, j + k] += 7
    # 	if youxia_tuple[0] == youxia_tuple[1] == youxia_tuple[2] == youxia_tuple[3] == youxia_tuple[4] ==[]:
    # 		for k in range(5)
    # 			score[i + k, j + k] += 7

    # 	if zuoxia_tuple[0] == zuoxia_tuple[1] == zuoxia_tuple[2] == zuoxia_tuple[3] == zuoxia_tuple[4] ==[]:
    # 		for k in range(5)
    # 			score[i - k, j + k] += 7
	


    def Score(chesslist, i, j, score):

	    for k in range(5):
			you_tuple[k] = chesslist[i + k][j]
			xia_tuple[k] = chesslist[i][j + k]
			youxia_tuple[k] = chesslist[i + k][j + k]
			zuoxia_tuple[k] = chesslist[i - k][j + k]

    	you_black = you_tuple.count(0)
    	you_white = you_tuple.count(1)
    	you_blank = you_tuple.count([])

    	zuo_black = zuo_tuple.count(0)
    	zuo_white = zuo_tuple.count(1)
    	zuo_blank = zuo_tuple.count([])

    	youxia_black = youxia_tuple.count(0)
    	youxia_white = youxia_tuple.count(1)
    	youxia_blank = youxia_tuple.count([])

    	zuoxia_black = zuoxia_tuple.count(0)
    	zuoxia_white = zuoxia_tuple.count(1)
    	zuoxia_blank = zuoxia_tuple.count([]) 

    	if you_blank == 5:
    		for k in range(5)
    			score[i + k, j] += 7
    	if xia_blank == 5: 
    		for k in range(5)
    			score[i, j + k] += 7
    	if youxia_blank == 5:
    		for k in range(5)
    			score[i + k, j + k] += 7       			
    	if zuoxia_blank == 5:
    		for k in range(5)
    			score[i - k, j + k] += 7

    	
    	if you_black == 1 and you_blank == 4:
    		for k in range(5)
    			score[i + k, j] += 35
    	if xia_blank == 1 and xia_blank == 4: 
    		for k in range(5)
    			score[i, j + k] += 35
    	if youxia_black == 1 and youxia_blank == 4:
    		for k in range(5)
    			score[i + k, j + k] += 35      			
    	if zuoxia_black == 1 and zuoxia_blank == 4:
    		for k in range(5)
    			score[i - k, j + k] += 35


    	if you_black == 2 and you_blank == 3:
    		for k in range(5)
    			score[i + k, j] += 800
    	if xia_blank == 2 and xia_blank == 3: 
    		for k in range(5)
    			score[i, j + k] += 800
    	if youxia_black == 2 and youxia_blank == 3:
    		for k in range(5)
    			score[i + k, j + k] += 800      			
    	if zuoxia_black == 2 and zuoxia_blank == 3:
    		for k in range(5)
    			score[i - k, j + k] += 800


    	if you_black == 3 and you_blank == 2:
    		for k in range(5)
    			score[i + k, j] += 15000
    	if xia_blank == 3 and xia_blank == 2: 
    		for k in range(5)
    			score[i, j + k] += 15000
    	if youxia_black == 3 and youxia_blank == 2:
    		for k in range(5)
    			score[i + k, j + k] += 15000      			
    	if zuoxia_black == 3 and zuoxia_blank == 2:
    		for k in range(5)
    			score[i - k, j + k] += 15000


    	if you_black == 4 and you_blank == 1:
    		for k in range(5)
    			score[i + k, j] += 800000
    	if xia_blank == 4 and xia_blank == 1: 
    		for k in range(5)
    			score[i, j + k] += 800000
    	if youxia_black == 4 and youxia_blank == 1:
    		for k in range(5)
    			score[i + k, j + k] += 800000      			
    	if zuoxia_black == 4 and zuoxia_blank == 1:
    		for k in range(5)
    			score[i - k, j + k] += 800000

   
    	if you_white == 1 and you_blank == 4:
    		for k in range(5)
    			score[i + k, j] += 15
    	if xia_white == 1 and xia_blank == 4: 
    		for k in range(5)
    			score[i, j + k] += 15
    	if youxia_white == 1 and youxia_blank == 4:
    		for k in range(5)
    			score[i + k, j + k] += 15     			
    	if zuoxia_white == 1 and zuoxia_blank == 4:
    		for k in range(5)
    			score[i - k, j + k] += 15


    	if you_white == 2 and you_blank == 3:
    		for k in range(5)
    			score[i + k, j] += 400
    	if xia_white == 2 and xia_blank == 3: 
    		for k in range(5)
    			score[i, j + k] += 400
    	if youxia_white == 2 and youxia_blank == 3:
    		for k in range(5)
    			score[i + k, j + k] += 400    			
    	if zuoxia_white == 2 and zuoxia_blank == 3:
    		for k in range(5)
    			score[i - k, j + k] += 400


    	if you_white == 3 and you_blank == 2:
    		for k in range(5)
    			score[i + k, j] += 1800
    	if xia_white == 3 and xia_blank == 2: 
    		for k in range(5)
    			score[i, j + k] += 1800
    	if youxia_white == 3 and youxia_blank == 2:
    		for k in range(5)
    			score[i + k, j + k] += 1800   			
    	if zuoxia_white == 3 and zuoxia_blank == 2:
    		for k in range(5)
    			score[i - k, j + k] += 1800


    	if you_white == 4 and you_blank == 1:
    		for k in range(5)
    			score[i + k, j] += 100000
    	if xia_white == 4 and xia_blank == 1: 
    		for k in range(5)
    			score[i, j + k] += 100000
    	if youxia_white == 4 and youxia_blank == 1:
    		for k in range(5)
    			score[i + k, j + k] += 100000    			
    	if zuoxia_white == 4 and zuoxia_blank == 1:
    		for k in range(5)
    			score[i - k, j + k] += 100000
    			
# chesslist = 
# m = 0
# for i in  range(19):
# 	for j in range(15):
# 		for k in range(5):
# 			if chesslist[i][j + k] == chesslist[i][j]
# 			copylist2[l][k] = copy.copy(chesslist[j + k][i])
# 		m += 1

# n = 0		
# 	for i in range(15):
# 		for j in range(15):
# 			for k in range(5):
# 				copylist3[l][k] = copy.copy(chesslist[i + k][j + k])
# 				copylist4[l][k] = copy.copy(chesslist[i - k][j + k])
# 		n += 1

# for i in range(m):
# 	for k in range(5):
# 		if copylist1[i][k] == 
