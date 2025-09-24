# oppgave a
saldo = 20000  
spare = 2000
rente = 0.3    # Rente i prosent (0,3%)
mål = 70000    
n = 24 
vf = 1 + rente / 100

# Beregn saldo etter 12 måneder (oppgave a)
for i in range(1, 13):  # range (1,13) gir 12 måneder
    saldo = (saldo+spare)*vf # Oppdater saldo med rente
print(f"Saldo etter 12 måneder: {saldo:.2f}")

# oppgave b
spare = (mål - saldo * vf**n) / ((vf**n - 1) / (vf - 1))
print(f"For å oppnå {mål} på 2 år, må du spare {spare:.2f} hver måned.")
