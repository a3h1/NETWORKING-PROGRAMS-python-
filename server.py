import socket
import pickle

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def check_win(B):
	if B[0][0]==B[0][1] and B[0][0]==B[0][2]:
		if B[0][0]==1:
			return True
	elif B[0][0]==B[1][1] and B[0][0]==B[2][2]:
		if B[0][0]==1:
			return True
	elif B[0][0]==B[1][0] and B[0][0]==B[1][2]:
		if B[0][0]==1:
			return True
	elif B[1][0]==B[1][1] and B[1][0]==B[1][2]:
		if B[1][0]==1:
			return True
	elif B[2][0]==B[2][1] and B[2][0]==B[2][2]:
		if B[2][0]==1:
			return True
	elif B[0][1]==B[1][1] and B[0][1]==B[2][1]:
		if B[0][1]==1:
			return True
	elif B[0][2]==B[1][2] and B[0][2]==B[2][2]:
		if B[0][2]==1:
			return True
	elif B[0][2]==B[1][1] and B[0][2]==B[2][0]:
		if B[0][2]==1:
			return True
	else:
		return False

def chk_tie(A):
    for i in range(3):
        for j in range(3):
            if(A[i][j]==-1):
                return False
    return True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Waiting for any player to connect')
    conn, addr = s.accept()
    with conn:
        print('Player2 Accepted and Game starts')
        a=[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
        while True:
            print("Enter Index as i,j")
            inp=[]
            inp=input().split(',')
            i=int(inp[0])
            j=int(inp[1])
            if(i<3 and j<3 and i>=0 and j>=0 and a[i][j]==-1):
                a[i][j]=0
                conn.send(pickle.dumps([i,j]))
            else:
                print('position not accepted and is not stored')
                continue
            data = conn.recv(1024)
            try:
                data=pickle.loads(data)
            except EOFError:
                break
            if(data[0]<3 and data[1]<3 and data[0]>=0 and data[1]>=0 and a[data[0]][data[1]]==-1):
                a[data[0]][data[1]]=1
                print('position accepted and stored')
                print('move : symbol \'X\' in position ('+str(data[0])+','+str(data[1])+')')
            else:
                print('position not accepted and is not stored')
                continue
            if(check_win(a)):
                print("Player2 won.")
                break
            if(chk_tie(a)):
                print("tie")
                break
        conn.close()
   
            