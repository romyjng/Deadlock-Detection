# project2 - deadlock detection
# 2018310018 정찬휘
# 사유: C언어 사용법을 배우지 않아 파이썬으로 대체하여 작성해 보았습니다. 감사합니다.

f= open('C:\\Users\sprig\Desktop\input.txt', 'r')       # 바탕화면에 저장된 'input.txt'파일 읽기


line = f.readline()
pnum, rnum, u1, u2, u3 = line[0], line[2], line[4], line[6], line[8] # Process 개수, Resource Type 개수, Resource Unit별 개수를 각자 변수에 저장

# Alloc. matrix 저장
# P1 alloc
line = f.readline()
p1u1a, p1u2a, p1u3a = line[3], line[5], line[7]
p1a_list = [int(p1u1a), int(p1u2a), int(p1u3a)]

# P2 alloc
line = f.readline()
p2u1a, p2u2a, p2u3a = line[3], line[5], line[7]
p2a_list = [int(p2u1a), int(p2u2a), int(p2u3a)]

# P3 alloc
line = f.readline()
p3u1a, p3u2a, p3u3a = line[3], line[5], line[7]
p3a_list = [int(p3u1a), int(p3u2a), int(p3u3a)]


# allocation list 작성
alloclist = [p1a_list, p2a_list, p3a_list]      # calc_leftresource 함수 정의에 활용


# Req. matrix 저장
# P1 req
line = f.readline()
p1u1r, p1u2r, p1u3r = line[3], line[5], line[7]
p1r_list = [int(p1u1r), int(p1u2r), int(p1u3r)]


# P2 req
line = f.readline()
p2u1r, p2u2r, p2u3r = line[3], line[5], line[7]
p2r_list = [int(p2u1r), int(p2u2r), int(p2u3r)]


# P3 req
line = f.readline()
p3u1r, p3u2r, p3u3r = line[3], line[5], line[7]
p3r_list = [int(p3u1r), int(p3u2r), int(p3u3r)]


# request list 작성
original_reqlist = [p1r_list, p2r_list, p3r_list]       # 원본 request list 저장
reqlist = [p1r_list, p2r_list, p3r_list]    # 이후 자원 할당 및 반환 뒤 업데이트해서 사용 예정



# 남은 resource를 unit별로 계산 및 리스트에 저장
# leftr은 detect_deadlock 함수 내에서 alloc_able 함수의 인자로 활용됨 

leftr = [int(u1) - (int(p1u1a)+int(p2u1a)+int(p3u1a)), int(u2) - (int(p1u2a)+int(p2u2a)+int(p3u2a)), int(u3) - (int(p1u3a)+int(p2u3a)+int(p3u3a))]




# allocation 가능 여부를 반환하는 함수
# request unit 개수와 남은 resource 개수를 비교하여 모두 할당 가능하면 True, 하나라도 할당 불가하면 False를 반환하는 함수 정의

def alloc_able(request, left):
    request = list(request)
    left = list(left)
    for i in range(rnum):
        if request[i] <= left[i]:
            if i == rnum-1:
                return True
            else:
                continue
        else:
            return False



# 연산을 위해 자원 개수와 프로세스 개수의 자료형을 int로 바꿔줌

rnum = int(rnum)        
pnum = int(pnum)

        
# 할당 가능한 Process를 발견했을 때, 할당 및 반환 후 남은 자원을 다시 계산하는 함수 정의

def calc_leftresource(index, leftresource):
    
    # process에 할당 되어 있던 자원
    alloc = alloclist[index-1]      # index가 실제 index가 아닌 process number로 올 것이기 때문에 -1 연산을 해준다.      
    # 할당 전 남아있던 자원
    leftresource += alloc
    return [leftresource + alloc for leftresource, alloc in zip(leftresource, alloc)]




# 모든 process의 resource 할당 여부를 확인 후 deadlock 식별하는 함수 정의

def detect_deadlock(leftresourcelist, reqlist):
    
    cant_alloc_list = []
    
    for i in reqlist:       # req list 하나씩 확인
        
        if alloc_able(i, leftresourcelist):     # req list가 할당 가능한 경우
            '''cant_alloc_list = []'''
            
            i_index = reqlist.index(i)+1    #현재 보고 있는 req list의 인덱스 저장
            reqlist.remove(i)         # req list에서 할당 및 반환한 list 삭제
            
            if len(reqlist) > 0:            # 아직 남아있는 req list가 있을 때
                leftresourcelist = calc_leftresource(i_index, leftresourcelist)     # 할당 및 반환 이후 남은 자원 다시 계산 (left resource list)      
                detect_deadlock(leftresourcelist, reqlist)         # 업데이트 된 req list와 left resource list로 deadlock 판별 함수 재귀 호출      
            else:           # 남아있는 req list가 없는 상태 
                detect_deadlock(leftresourcelist, reqlist)
                print('Deadlock 상태가 아니다.')

        else:
            cant_alloc_list.append(original_reqlist.index(i)+1)     # cant_alloc_list에 할당 불가능한 process의 인덱스+1을 저장한다. (process number는 인덱스+1 이기 때문)
            
            if len(cant_alloc_list) == len(reqlist):  # 모든 req list가 할당 불가인 경우
                print('Deadlock 상태이다.')
                print('Deadlocked Process List:'+ str(cant_alloc_list))
            else:
                continue


# deadlock 식별

detect_deadlock(leftr, reqlist)





