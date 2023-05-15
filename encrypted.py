import socket
import threading
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
# Generate some parameters. These can be reused.
parameters = dh.generate_parameters(generator=2, key_size=2048)
# Generate a private key for use in the exchange.
server_private_key = parameters.generate_private_key()
# In a real handshake the peer is a remote client. For this
import rsa as diffieHellman
# example we'll generate another local private key though. Note that in
# a DH handshake both peers must agree on a common set of parameters.
peer_private_key = parameters.generate_private_key()
shared_key = server_private_key.exchange(peer_private_key.public_key())
# Perform key derivation.

derived_key = HKDF(

    algorithm=hashes.SHA256(),

    length=32,

    salt=None,

    info=b'handshake data',

).derive(shared_key)

# And now we can demonstrate that the handshake performed in the

# opposite direction gives the same final value

same_shared_key = peer_private_key.exchange(

    server_private_key.public_key()

)

same_derived_key = HKDF(

    algorithm=hashes.SHA256(),

    length=32,

    salt=None,

    info=b'handshake data',

).derive(same_shared_key)

derived_key == same_derived_key


# Diffie-Hellman Code


def prime_checker(p):
	# Checks If the number entered is a Prime Number or not
	if p < 1:
		return -1
	elif p > 1:
		if p == 2:
			return 1
		for i in range(2, p):
			if p % i == 0:
				return -1
			return 1


def primitive_check(g, p, L):
	# Checks If The Entered Number Is A Primitive Root Or Not
	for i in range(1, p):
		L.append(pow(g, i) % p)
	for i in range(1, p):
		if L.count(i) > 1:
			L.clear()
			return -1
		return 1


l = []
while 1:
	P = int(input("Enter P : "))
	if prime_checker(P) == -1:
		print("Number Is Not Prime, Please Enter Again!")
		continue
	break

while 1:
	G = int(input(f"Enter The Primitive Root Of {P} : "))
	if primitive_check(G, P, l) == -1:
		print(f"Number Is Not A Primitive Root Of {P}, Please Try Again!")
		continue
	break

# Private Keys
x1, x2 = int(input("Enter The Private Key Of User 1 : ")), int(
	input("Enter The Private Key Of User 2 : "))
while 1:
	if x1 >= P or x2 >= P:
		print(f"Private Key Of Both The Users Should Be Less Than {P}!")
		continue
	break

# Calculate Public Keys
y1, y2 = pow(G, x1) % P, pow(G, x2) % P

# Generate Secret Keys
k1, k2 = pow(y2, x1) % P, pow(y1, x2) % P

print(f"\nSecret Key For User 1 Is {k1}\nSecret Key For User 2 Is {k2}\n")

if k1 == k2:
	print("Keys Have Been Exchanged Successfully")
else:
	print("Keys Have Not Been Exchanged Successfully")



public_key, private_key =diffieHellman.newkeys(1024)

os.system('color 90')
os.system('cls')
public_partner =None

choice = input("Do you Want to host(1) or to connect (2)?\t")

if choice == "1":
    server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.56.1", 9999))
    server.listen ()
    
    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner =diffieHellman.PublicKey.load_pkcs1(client.recv(1024))


elif choice == "2":
    client = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.56.1", 9999))
     
    public_partner =diffieHellman.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

else:
    exit()


def sending_message(c):
    print("Write Your Message:")
    while True:
        message =input("")
        c.send(diffieHellman.encrypt(message.encode(), public_partner))
        print("You: "+ message )

        
def reciving_message(c):
    while True:
        print("Partner : "+ diffieHellman.decrypt(c.recv(1024), private_key).decode())

        
threading.Thread(target=sending_message, args=(client,)).start()
threading.Thread(target=reciving_message, args=(client,)).start()