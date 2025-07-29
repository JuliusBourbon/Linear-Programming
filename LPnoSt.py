def input_data():
    print("\n=== INPUT DATA MASALAH PEMROGRAMAN LINEAR ===")
    n = int(input("Jumlah variabel keputusan: "))
    m = int(input("Jumlah kendala: "))

    decision_labels = []
    print("\nMasukkan nama/label untuk setiap variabel keputusan:")
    for i in range(n):
        label = input(f"Label variabel x{i+1}: ")
        decision_labels.append(label)

    print("\nMasukkan koefisien fungsi tujuan (dipisah spasi):")
    c_input = input("Z = ").split()
    c = []
    for val in c_input:
        c.append(float(val))

    A = []
    b = []
    constraint_labels = []

    print("\nMasukkan nama/label untuk setiap kendala:")
    for i in range(m):
        label = input(f"Label kendala {i+1}: ")
        constraint_labels.append(label)

    print("\nMasukkan koefisien fungsi kendala dan sisi kanan:")
    for i in range(m):
        print(f"{constraint_labels[i]} (format: a1 a2 ... an b):")
        row_input = input().split()
        row = []
        for val in row_input[:-1]:
            row.append(float(val))
        A.append(row)
        b.append(float(row_input[-1]))

    return n, m, c, A, b, constraint_labels, decision_labels

def print_tableau(tableau, n, m, step, decision_labels):
    print(f"\n== ITERASI {step} ==")
    headers = decision_labels + [f"S{i+1}" for i in range(m)] + ["Solusi"]
    print("Basis\t" + "\t".join(headers))
    for i, row in enumerate(tableau):
        if i < len(tableau) - 1:
            basis_var = f"S{i+1}"
        else:
            basis_var = "Z"
        print(f"{basis_var}\t" + "\t".join(f"{val:7.2f}" for val in row))

def build_tableau(n, m, c, A, b):
    tableau = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(A[i][j])
        for j in range(m):
            row.append(1.0 if j == i else 0.0)
        row.append(b[i])
        tableau.append(row)

    obj_row = []
    for ci in c:
        obj_row.append(-ci)
    for j in range(m):
        obj_row.append(0.0)
    obj_row.append(0.0)
    tableau.append(obj_row)
    return tableau

def pivot(tableau, pivot_row, pivot_col):
    pivot_val = tableau[pivot_row][pivot_col]
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot_val

    for i in range(len(tableau)):
        if i != pivot_row:
            ratio = tableau[i][pivot_col]
            for j in range(len(tableau[0])):
                tableau[i][j] -= ratio * tableau[pivot_row][j]

def find_pivot_column(tableau):
    last_row = tableau[-1][:-1]
    min_val = last_row[0]
    min_idx = 0
    for i in range(1, len(last_row)):
        if last_row[i] < min_val:
            min_val = last_row[i]
            min_idx = i
    return min_idx if min_val < 0 else -1

def find_pivot_row(tableau, pivot_col):
    min_ratio = float('inf')
    pivot_row = -1
    for i in range(len(tableau) - 1):
        rhs = tableau[i][-1]
        elt = tableau[i][pivot_col]
        if elt > 0:
            ratio = rhs / elt
            if ratio < min_ratio:
                min_ratio = ratio
                pivot_row = i
    return pivot_row

def simplex(n, m, c, A, b, decision_labels):
    tableau = build_tableau(n, m, c, A, b)
    step = 1
    while True:
        print_tableau(tableau, n, m, step, decision_labels)
        pivot_col = find_pivot_column(tableau)
        if pivot_col == -1:
            print("\n>> Tidak ada nilai negatif di baris Z, solusi optimal ditemukan.")
            break
        pivot_row = find_pivot_row(tableau, pivot_col)
        if pivot_row == -1:
            print("\n>> Masalah tidak terbatas (unbounded). Tidak ada baris yang memenuhi syarat pivot.")
            break
        print(f"Pivot pada baris {pivot_row+1}, kolom {pivot_col+1}")
        pivot(tableau, pivot_row, pivot_col)
        step += 1
    return tableau

def extract_solution(tableau, n, m):
    sol = []
    for i in range(n):
        value = 0
        col = []
        for row in tableau[:-1]:
            col.append(row[i])
        if col.count(1) == 1 and col.count(0) == len(col) - 1:
            row_index = col.index(1)
            value = tableau[row_index][-1]
        sol.append(value)
    z = tableau[-1][-1]
    return sol, z

def main():
    n, m, c, A, b, constraint_labels, decision_labels = input_data()
    final_tableau = simplex(n, m, c, A, b, decision_labels)
    solution, zmax = extract_solution(final_tableau, n, m)
    print("\n>> HASIL AKHIR <<")
    for i in range(n):
        print(f"{decision_labels[i]} (x{i+1}) = {solution[i]:.2f}")
    print(f"\nUntuk mencapai maksimasi,", end=" ")
    for i in range(n):
        if solution[i] > 0:
            print(f"{decision_labels[i]} harus diproduksi sejumlah ± {solution[i]:.0f},", end=" ")
    print(f"\ndengan pendapatan maksimum sebesar Rp{zmax:,.0f}")

if __name__ == "__main__":
    main()
