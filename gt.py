

# 3 stanze A, B, C
# Na, Nb, Nc
# Ma, Mb, Mc


# TO DO Va, Vb, Vc
# Valore di un furto V

# Cattura C

# malposizionamento m
# stanza scoperta s

### generare combinazioni dei poliz
# tot poliz = N

n_stanze = 3

N = 2
v = 1
c_param = 1
malposiz = 1
st_scoperte = 1

poliz = []

for Na in range(N+1):
	for Nb in range(0, N-Na+1):
		Nc = N-Na-Nb
		poliz.append((Na, Nb, Nc))

crimin = []
C = 3
for Na in range(C+1):
	for Nb in range(0, C-Na+1):
		Nc = C-Na-Nb
		crimin.append((Na, Nb, Nc))


sp = "           "

pre_sp = "   "
post_sp = "    "

print(sp, end="")
for c in crimin:
	print(c, end="  ")
print()

for p in poliz:
	print(p, end=" ");
	for c in crimin:
		n_furti = 0
		n_catture = 0
		n_malposiz = 0
		n_stanze_scoperte = 0

		for i in range(n_stanze):
			diff = c[i]-p[i]
			if (diff>0):
				n_furti += diff
			else:
				n_catture += diff
			if (p[i]>0 and c[i]==0):
				n_malposiz += p[i]
			if (p[i]==0):
				n_stanze_scoperte += 1

		u_s = n_furti*(-v) + n_catture*c_param - n_malposiz*malposiz - n_stanze_scoperte*st_scoperte

		u_c = n_furti*(v) + n_catture*(-c_param)

		print(pre_sp + str(u_s)+ "," + str(u_c) + post_sp, end="")
	print()