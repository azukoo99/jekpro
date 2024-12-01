import csv
import pandas as pd
from tabulate import tabulate
import os


def login():
    os.system('cls')
    teks = """
    ██████╗░░█████╗░███╗░░██╗███████╗███╗░░██╗██████╗░░█████╗░██████╗░
    ██╔══██╗██╔══██╗████╗░██║██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗██║█████╗░░██╔██╗██║██║░░██║██║░░██║██████╔╝
    ██╔═══╝░██╔══██║██║╚████║██╔══╝░░██║╚████║██║░░██║██║░░██║██╔══██╗
    ██║░░░░░██║░░██║██║░╚███║███████╗██║░╚███║██████╔╝╚█████╔╝██║░░██║
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝
    """

    print(teks)
    print ("=================================[LOGIN]=================================")


    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    user = []
    with open('user.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            user.append({'username': row[0], 'password': row[1], 'role': row[2]})

    for i in user:
        if i['username'] == username and i['password'] == password:
            if i['role'] == 'owner': 
                print("Selamat datang, owner!")
                input("Klik Enter untuk melanjutkan...")
                menu_owner(username)
            else:
                print(f"Selamat datang, {i['username']}!")
                input("Klik Enter untuk melanjutkan...")
                menu_kasir(username)
            return username

    print("Username atau password salah!")    
    input("Klik Enter untuk melanjutkan...")
    return login()

def kelola_produk(role, username):
    os.system('cls')
    data_produk = pd.read_csv('produk.csv')
    data_produk.index += 1
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    print("Kelola Produk")
    print("1. Tambah Produk")
    print("2. Hapus Produk")
    print("3. Update Produk")
    print("4. Keluar")

    pilihan = input("Masukan jawaban Anda: ")
    if pilihan == "1":
        tambah_produk(data_produk)
    elif pilihan == "2":
        hapus_produk(data_produk)
    elif pilihan == "3":
        update_produk(data_produk)
    elif pilihan == "4":
        if role == "owner":
            menu_owner(username)
        else:
            menu_kasir(username)
    else:
        input("Masukan input yang benar, tekan Enter untuk lanjut")
        kelola_produk(role, username)

def tambah_produk(data_produk):
    os.system('cls')
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    nama_produk = input("Masukan nama produk: ")
    stok_produk = input("Masukan stok produk: ")
    harga_produk = input("Masukan harga produk: ")
    menambahkan_produk = pd.DataFrame({"produk": [nama_produk], "stok(kg)": [stok_produk], "harga": [harga_produk]})
    data_produk = data_produk._append(menambahkan_produk)
    data_produk.to_csv('produk.csv', index=False)
    print("Produk berhasil ditambahkan")
    input("Klik Enter untuk melanjutkan...")

def hapus_produk(data_produk):
    os.system('cls')
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    index_produk = int(input("Masukan index produk: ")) 
    if 0 <= index_produk < len(data_produk)+1:
        data_produk = data_produk.drop(index=index_produk)
        data_produk.to_csv('produk.csv', index=False)
        print("Produk berhasil dihapus")
    else:
        print("Index tidak valid!")
    input("Klik Enter untuk melanjutkan...")

def update_produk(data_produk):
    os.system('cls')
    print(tabulate(data_produk, headers='keys', tablefmt='fancy_grid'))
    index_produk = int(input("Masukan index produk: ")) 
    if 0 <= index_produk < len(data_produk)+1:
        nama_produk = input("Masukan nama produk: ")
        stok_produk = input("Masukan stok produk: ")
        harga_produk = input("Masukan harga produk: ")
        data_produk.at[index_produk, "produk"] = nama_produk
        data_produk.at[index_produk, "stok(kg)"] = float(stok_produk)
        data_produk.at[index_produk, "harga"] = float(harga_produk)

        data_produk.to_csv('produk.csv', index=False)
        print("Produk berhasil diubah")
    else:
        print("Index tidak valid!")
    input("Klik Enter untuk melanjutkan...")

def catatan_penjualan(username):
    os.system('cls')
    produk = pd.read_csv('produk.csv')
    penjualan = pd.read_csv('penjualan.csv')

    tampilkan_produk = produk.copy()
    tampilkan_produk.index += 1
    print("\nDaftar Produk Tersedia:")
    print(tabulate(tampilkan_produk, headers='keys', tablefmt='fancy_grid'))

    while True:
        try:
            jumlah_jenis = int(input("\nBerapa jenis produk yang ingin dibeli: "))
            if jumlah_jenis <= 0:
                print("Masukkan angka lebih besar dari 0!")
                continue
            break
        except ValueError:
            print("Input tidak valid! Masukkan angka.")
    
    keranjang = []
    total_belanja = 0
    
    for i in range(jumlah_jenis):
        print(f"\nPembelian ke-{i+1}")

        while True:
            try:
                nomor_produk = int(input("Masukkan nomor produk: ")) - 1
                if nomor_produk < 0 or nomor_produk >= len(produk):
                    print("Nomor produk tidak valid!")
                    continue
                
                jumlah = float(input("Masukkan jumlah (kg): "))
                if jumlah <= 0:
                    print("Jumlah harus lebih besar dari 0!")
                    continue
                
                stok = float(produk.iloc[nomor_produk]['stok(kg)'])
                if jumlah > stok:
                    print(f"Stok tidak cukup! Stok tersedia: {stok} kg")
                    continue
                
                nama = produk.iloc[nomor_produk]['produk']
                harga = float(produk.iloc[nomor_produk]['harga'])
                subtotal = jumlah * harga

                keranjang.append({'produk': nama, 'jumlah': jumlah, 'harga': harga, 'subtotal': subtotal})
                total_belanja += subtotal

                produk.at[nomor_produk, 'stok(kg)'] = stok - jumlah
                break
            except ValueError:
                print("Input tidak valid! Masukkan angka.")
    
    print("\n=== STRUK PEMBELIAN ===")
    print(f"Kasir: {username}")  
    for i in keranjang:
        print(f"\nProduk: {i['produk']}")
        print(f"Jumlah: {i['jumlah']} kg")
        print(f"Harga: Rp {i['harga']:,.0f}/kg")
        print(f"Subtotal: Rp {i['subtotal']:,.0f}")
    print(f"\nTotal Pembelian: Rp {total_belanja:,.0f}")
    
    for i in keranjang:
        new_row = pd.DataFrame({
            'tanggal': [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")],
            'produk': [i['produk']],
            'jumlah': [i['jumlah']],
            'harga': [i['harga']], 
            'total': [i['subtotal']]
        })
        penjualan = pd.concat([penjualan, new_row], ignore_index=True)

    penjualan.to_csv('penjualan.csv', index=False)
    produk.to_csv('produk.csv', index=False)
    
    input("\nTekan Enter untuk kembali ke menu utama...")

def laporan_keuntungan():
    # Implementasi fungsi laporan keuntungan
    pass

def kelola_akun_kasir():
    # Implementasi fungsi kelola akun kasir
    pass

def logout():
    print("Anda telah logout. Sampai jumpa!")
    os.system('cls')
    exit()

def menu_kasir(username):
    while True:
        os.system('cls')
        teks = """
    ██████╗░░█████╗░███╗░░██╗███████╗███╗░░██╗██████╗░░█████╗░██████╗░
    ██╔══██╗██╔══██╗████╗░██║██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗██║█████╗░░██╔██╗██║██║░░██║██║░░██║██████╔╝
    ██╔═══╝░██╔══██║██║╚████║██╔══╝░░██║╚████║██║░░██║██║░░██║██╔══██╗
    ██║░░░░░██║░░██║██║░╚███║███████╗██║░╚███║██████╔╝╚█████╔╝██║░░██║
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝
    """

        print(teks)

        print(f"===================== MENU UTAMA (Kasir: {username}) =====================")
        print("1. Kelola Produk")
        print("2. Catat Penjualan")
        print("3. Logout")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            kelola_produk("kasir", username)
        elif pilihan == '2':
            catatan_penjualan(username)
        elif pilihan == '3':
            logout()
        else:
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")

def menu_owner(username):
    while True:
        os.system('cls')
        teks = """
    ██████╗░░█████╗░███╗░░██╗███████╗███╗░░██╗██████╗░░█████╗░██████╗░
    ██╔══██╗██╔══██╗████╗░██║██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗██║█████╗░░██╔██╗██║██║░░██║██║░░██║██████╔╝
    ██╔═══╝░██╔══██║██║╚████║██╔══╝░░██║╚████║██║░░██║██║░░██║██╔══██╗
    ██║░░░░░██║░░██║██║░╚███║███████╗██║░╚███║██████╔╝╚█████╔╝██║░░██║
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚══╝╚═════╝░░╚════╝░╚═╝░░╚═╝
    """

        print(teks)

        print(f"===================== MENU UTAMA (Owner: {username}) =====================")
        print("1. Kelola Produk")
        print("2. Catat Penjualan")
        print("3. Laporan Keuntungan")
        print("4. Kelola Akun Kasir")
        print("5. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5): ")

        if pilihan == '1':
            kelola_produk("owner", username)
        elif pilihan == '2':
            catatan_penjualan(username)
        elif pilihan == '3':
            laporan_keuntungan()
        elif pilihan == '4':
            kelola_akun_kasir()
        elif pilihan == '5':
            logout()
        else:
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")

# Panggil fungsi login
username = login()
