# ============================================================
# CELDA 1 — Jorge: Definición del problema y estructura de datos
# ============================================================

def knapsack_01(W, items):
    """
    Resuelve el problema 0/1 Knapsack con programación dinámica bottom-up.

    Parámetros:
        W     : int — capacidad máxima de memoria del servidor
        items : list[tuple[str, int, int]] — lista de (nombre, peso, valor) de cada VM

    Retorna:
        max_value      : int — valor máximo alcanzable
        selected_items : list[str] — nombres de las VMs seleccionadas
        dp_table       : list[list[int]] — tabla DP completa (para visualización)
    """
    n = len(items)

    # Tabla DP: (n+1) filas x (W+1) columnas, inicializada en 0
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Llenado bottom-up
    for i in range(1, n + 1):
        name_i, w_i, v_i = items[i - 1]
        for c in range(W + 1):
            # Caso 1: no incluir VM i
            dp[i][c] = dp[i - 1][c]
            # Caso 2: incluir VM i (si cabe)
            if w_i <= c:
                dp[i][c] = max(dp[i][c], v_i + dp[i - 1][c - w_i])

    # Backtracking para recuperar las VMs seleccionadas
    selected = []
    c = W
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(items[i - 1][0])  # nombre de la VM
            c -= items[i - 1][1]              # restar su peso

    selected.reverse()

    return dp[n][W], selected, dp


# ============================================================
# CELDA 2 — Wilson: Visualización de la tabla DP
# ============================================================

def print_dp_table(dp, items, W):
    """
    Imprime la tabla DP de forma legible.

    Parámetros:
        dp    : list[list[int]] — tabla DP generada por knapsack_01
        items : list[tuple[str, int, int]] — lista de (nombre, peso, valor)
        W     : int — capacidad máxima
    """
    n = len(items)
    header = "".join(f"{c:>6}" for c in range(W + 1))
    print(f"{'VM':>10} | c = {header}")
    print("-" * (16 + 6 * (W + 1)))

    # Fila base (i=0)
    row = "".join(f"{dp[0][c]:>6}" for c in range(W + 1))
    print(f"{'(ninguna)':>10} | {row}")

    # Filas de cada VM
    for i in range(1, n + 1):
        name = items[i - 1][0]
        row = "".join(f"{dp[i][c]:>6}" for c in range(W + 1))
        print(f"{name:>10} | {row}")


# ============================================================
# CELDA 3 — Jorge: Caso de prueba principal
# ============================================================

# Definición de la instancia
W = 10  # capacidad del servidor en GB

vms = [
    # (nombre,   memoria_GB, valor)
    ("DB-Main",       6,       30),
    ("Web-Server",    3,       14),
    ("Cache-Redis",   4,       16),
    ("ML-Worker",     2,        9),
]

max_val, selected, dp = knapsack_01(W, vms)

print("=" * 50)
print("CRISIS 2 — Asignación de Memoria para VMs")
print("=" * 50)
print(f"Capacidad del servidor: {W} GB")
print(f"VMs disponibles:")
for name, w, v in vms:
    print(f"  {name:15s}  memoria={w} GB  valor={v}")
print("-" * 50)
print(f"Valor máximo alcanzable: {max_val}")
print(f"VMs seleccionadas: {', '.join(selected)}")
mem_used = sum(w for name, w, v in vms if name in selected)
print(f"Memoria utilizada: {mem_used}/{W} GB")


# ============================================================
# CELDA 4 — Wilson: Mostrar tabla DP completa
# ============================================================

print("\nTabla DP completa:\n")
print_dp_table(dp, vms, W)


# ============================================================
# CELDA 5 — Jorge: Verificación con el contraejemplo del documento
# ============================================================

print("\n" + "=" * 50)
print("VERIFICACIÓN — Contraejemplo del greedy")
print("=" * 50)

W_test = 5
vms_test = [
    ("VM_1", 3, 4),  # ratio 1.33
    ("VM_2", 5, 6),  # ratio 1.20
]

val, sel, dp_test = knapsack_01(W_test, vms_test)
print(f"W = {W_test}")
for name, w, v in vms_test:
    print(f"  {name}: memoria={w}, valor={v}, ratio={v/w:.2f}")
print(f"\nGreedy por ratio tomaría VM_1 → valor = 4")
print(f"DP encuentra → valor = {val}, selección: {', '.join(sel)}")
print(f"DP supera al greedy: {val > 4}")


# ============================================================
# CELDA 6 — Wilson: Caso borde y estrés
# ============================================================

print("\n" + "=" * 50)
print("CASOS BORDE")
print("=" * 50)

# Caso 1: ninguna VM cabe
print("\n--- Caso: ninguna VM cabe ---")
val, sel, _ = knapsack_01(1, [("Big-VM", 5, 100)])
print(f"W=1, VM con memoria=5 → valor={val}, selección={sel}")

# Caso 2: todas caben
print("\n--- Caso: todas las VMs caben ---")
vms_small = [("A", 1, 5), ("B", 2, 3), ("C", 1, 4)]
val, sel, _ = knapsack_01(10, vms_small)
print(f"W=10, VMs pequeñas → valor={val}, selección={', '.join(sel)}")

# Caso 3: instancia más grande
print("\n--- Caso: 8 VMs ---")
vms_large = [
    ("API-Gateway",   3, 12),
    ("Auth-Service",  2,  8),
    ("DB-Primary",    7, 35),
    ("DB-Replica",    7, 30),
    ("Cache-Layer",   4, 18),
    ("ML-Pipeline",   5, 22),
    ("Log-Collector", 1,  4),
    ("Monitor",       1,  3),
]
val, sel, _ = knapsack_01(15, vms_large)
print(f"W=15 GB")
for name, w, v in vms_large:
    marker = " ✓" if name in sel else ""
    print(f"  {name:15s}  mem={w} GB  val={v}{marker}")
print(f"Valor máximo: {val}")
print(f"Selección: {', '.join(sel)}")
mem = sum(w for name, w, v in vms_large if name in sel)
print(f"Memoria usada: {mem}/15 GB")
