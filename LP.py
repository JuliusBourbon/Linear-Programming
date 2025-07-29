import streamlit as st

def input_data(default=False):
    if default:
        n = 6
        m = 4
        label_tujuan = ["Ori", "Cheese", "Matcha", "Chocomelt", "Red Velvet", "Blueberry"]
        c = [50000, 60000, 65000, 70000, 75000, 80000]
        label_pembatas = ["Telur", "Tepung", "Gula", "Mentega"]
        A = [
            [3, 4, 4, 2, 2, 3],
            [350, 360, 355, 320, 350, 325],
            [60, 80, 70, 55, 50, 45],
            [80, 100, 90, 75, 70, 65]
        ]
        b = [80, 8500, 800, 2000]
    else:
        st.subheader("Masukkan Jumlah Variabel dan Kendala")
        n = st.number_input("Jumlah variabel keputusan", min_value=1, step=1)
        m = st.number_input("Jumlah kendala", min_value=1, step=1)

        label_tujuan = []
        st.subheader("Label Variabel Keputusan")
        for i in range(n):
            label = st.text_input(f"Label variabel x{i+1}")
            label_tujuan.append(label if label else f"x{i+1}")

        st.subheader("Fungsi Tujuan (Z)")
        c = []
        for i in range(n):
            coef = st.number_input(f"Koefisien {label_tujuan[i]}", min_value=0, step=1)
            c.append(float(coef))

        A = []
        b = []
        label_pembatas = []

        st.subheader("Fungsi Pembatas")
        for i in range(m):
            label = st.text_input(f"Label kendala {i+1}")
            label_pembatas.append(label if label else f"K{i+1}")
            row = []
            cols = st.columns(n + 1)
            for j in range(n):
                val = cols[j].number_input(f"{label_pembatas[i]} - {label_tujuan[j]}", min_value=0, step=1)
                row.append(float(val))
            rhs = cols[-1].number_input(f"Sisi kanan {label_pembatas[i]}", min_value=0, step=1)
            A.append(row)
            b.append(float(rhs))

    return n, m, c, A, b, label_pembatas, label_tujuan

def print_tableau(tableau, n, m, step, decision_labels, basis_labels):
    headers = ["Basis", "Z"] + [f"X{j+1}"for j in range(n)] + [f"S{i+1}" for i in range(m)] + ["Solusi"]
    data = []
    for i, row in enumerate(tableau):
        if i < len(tableau) - 1:
            basis_var = basis_labels[i]
            z_val = "0"
        else:
            basis_var = "Z"
            z_val = "1"
        data.append([basis_var, z_val] + [f"{val:.2f}" for val in row])
    st.subheader(f"Iterasi {step-1}")
    st.table([headers] + data)

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

def simplex(n, m, c, A, b, label_tujuan):
    tableau = build_tableau(n, m, c, A, b)
    step = 1
    basis_labels = [f"S{i+1}" for i in range(m)]
    while True:
        print_tableau(tableau, n, m, step, label_tujuan, basis_labels)
        pivot_col = find_pivot_column(tableau)
        if pivot_col == -1:
            st.success("Solusi optimal ditemukan.")
            break
        pivot_row = find_pivot_row(tableau, pivot_col)
        if pivot_row == -1:
            st.error("Masalah tidak terbatas (unbounded). Tidak ada baris yang memenuhi syarat pivot.")
            break
        entering_var = f"X{pivot_col + 1}"
        basis_labels[pivot_row] = entering_var
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
    st.set_page_config(page_title="Simpleks LP", layout="wide")
    tab1, tab2 = st.tabs(["Contoh Kasus", "User Input"])

    with tab1:
        st.header("Contoh Kasus Bolu Amanda")
        n, m, c, A, b, label_pembatas, label_tujuan = input_data(default=True)
        # Keterangan fungsi tujuan dan pembatas
        st.subheader("Keterangan")
        for i in range(n):
            st.write(f"X{i+1} = {label_tujuan[i]}")
            
        st.subheader("")
        st.subheader("Fungsi Tujuan")
        st.write("Maksimasi Z = " + " - ".join([f"{c[i]}x{i+1}" for i in range(n)]))
        st.subheader("")
        st.subheader("Fungsi Pembatas")
        for i in range(m):
            st.write(f"{label_pembatas[i]}: " + " + ".join([f"{A[i][j]}X{j+1}" for j in range(n)]) + f" <= {b[i]}")
            st.write()

        st.write(", ".join([f"X{i+1}" for i in range(n)] + [f"S{i+1}" for i in range(m)] + [">= 0"]))
        
        if st.button("Hitung Simpleks", key="default_btn"):
            final_tableau = simplex(n, m, c, A, b, label_tujuan)
            solution, zmax = extract_solution(final_tableau, n, m)

            st.subheader("Hasil Akhir")
            for i in range(n):
                st.write(f"{label_tujuan[i]} (x{i+1}) = {solution[i]:.2f}")

            hasil = "Untuk mencapai maksimasi, "
            hasil += ", ".join([f"{label_tujuan[i]} harus diproduksi sejumlah ± {solution[i]:.0f}" for i in range(n) if solution[i] > 0])
            hasil += f", dengan pendapatan maksimum sebesar Rp{zmax:,.0f}"
            st.success(hasil)

    with tab2:
        st.header("Masukkan Data Sendiri")
        n, m, c, A, b, label_pembatas, label_tujuan = input_data(default=False)
        if st.button("Hitung Simpleks", key="manual_btn"):
            final_tableau = simplex(n, m, c, A, b, label_tujuan)
            solution, zmax = extract_solution(final_tableau, n, m)

            st.subheader("Hasil Akhir")
            for i in range(n):
                st.write(f"{label_tujuan[i]} (x{i+1}) = {solution[i]:.2f}")

            hasil = "Untuk mencapai maksimasi, "
            hasil += ", ".join([f"{label_tujuan[i]} harus diproduksi sejumlah ± {solution[i]:.0f}" for i in range(n) if solution[i] > 0])
            hasil += f", dengan pendapatan maksimum sebesar Rp{zmax:,.0f}"
            st.success(hasil)

main()