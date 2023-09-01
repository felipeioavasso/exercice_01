import gurobipy as gp
from colorama import Fore, Style

# Limpar a tela do terminal
def clear_screen():
    print("\033c", end="")

# Dados de entrada
P = [10, 25, 20] # preço de venda do produto
C = [6, 15, 14] # custo do produto
L = [1000, 0, 100] # produção mínima
U = [6000, 500, 1000] # produção máxima
D = [400, 400, 500, 2000] # disponibilidade dos recursos
Q = [[0.03, 0.15, 0.1],
     [0.06, 0.12, 0.1],
     [0.05, 0.1, 0.12],
     [0, 2, 1.2]] # quantidade dos recursos nos produtos

n = len(P) # número de produtos
m = len(D) # número de recursos

utensilios = gp.Model() # cria um modelo do gurobi

# variáveis de decisão
#x = utensilios.addVars(n, vtype=gp.GRB.INTEGER)
x = utensilios.addVars(n, lb = L, ub = U, vtype=gp.GRB.INTEGER)

# função objetiva
utensilios.setObjective(sum((P[i] - C[i]) * x[i] for i in range(n)), sense = gp.GRB.MAXIMIZE)

#restrições
c1 = utensilios.addConstrs(sum(Q[j][i] * x[i] for i in range(n)) <= D[j] for j in range(m))
#c2 = utensilios.addConstrs(x[i] >= L[i] for i in range(n))
#c3 = utensilios.addConstrs(x[i] <= U[i] for i in range(n))


# Suprimindo o console output
utensilios.setParam('OutputFlag', 0)

# Resolvendo o modelo
utensilios.optimize()
clear_screen()

# Apresentando a solução
print()
print("--> Resolução do modelo dos utensílios de metal <--")
print()

Valor_otimo = utensilios.objVal
valor_otimo_colorido = f"{Fore.GREEN}{Valor_otimo:.2f}{Style.RESET_ALL}"
print("Valor ótimo:", valor_otimo_colorido)

# solução ótima
for i in range(n):
  print("x[{}] = {:.3f}".format(i+1, x[i].x))
print()

# utilização das matérias-primas
for j in range(m):
  print("Recurso {} = {}".format(j+1, sum(Q[j][i] * x[i].x for i in range(n))))
print()