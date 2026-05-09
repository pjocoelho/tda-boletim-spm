import gudhi
import numpy as np

# Exemplo: Nuvem de pontos aleatória
points = np.random.rand(50, 3)

# Criação do complexo de Rips
rips_complex = gudhi.RipsComplex(points=points, max_edge_length=0.5)
simplex_tree = rips_complex.create_simplex_tree(max_dimension=3)

# Cálculo da persistência
persistence = simplex_tree.persistence()

# Visualização do barcode
gudhi.plot_persistence_barcode(persistence)