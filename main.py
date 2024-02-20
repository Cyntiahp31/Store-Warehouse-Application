from tabulate import tabulate
from datetime import datetime


current_date = datetime.now().date()
date_format = '%Y-%m-%d'

# Dummy Data
data = [
    {"No" : None, "ID": 'P0001', "Product": "Richeese Nabati", "Quantity": 25, "Weight (gr)": 150.0, "Expired Date": '2026-08-06', "Manufacturer": 'PT Pangan Sehat'},
    {"No" : None, "ID": 'P0002', "Product": "Pantene Anti Dandruff", "Quantity": 30, "Weight (gr)": 350.0, "Expired Date": '2027-10-17', "Manufacturer": 'PT Unilever Indonesia'},
    {"No" : None, "ID": 'P0003', "Product": "Walen's Choco Soes", "Quantity": 22, "Weight (gr)": 100.6, "Expired Date": '2027-09-04', "Manufacturer": 'PT Makan Sejahtera'},
    {"No" : None, "ID": 'P0004', "Product": "Walen's Cheese Soes", "Quantity": 9, "Weight (gr)": 100.9, "Expired Date": '2027-10-04', "Manufacturer": 'PT Makan Sejahtera'},
    {"No" : None, "ID": 'P0005', "Product": "Roma Kelapa", "Quantity": 10, "Weight (gr)": 320.0, "Expired Date": '2025-12-11', "Manufacturer": 'PT Indofood Indonesia'}
]

# Iterasi untuk penomoran index dummy data setiap ada data yang dihapus
def update_no(data):
    for index, item in enumerate(data):
        item["No"] = index + 1

# Tambahkan penomoran agar user dapat melihat index data tersebut
update_no(data)

# Fungsi ini akan mengembalikan value True jika nama produk yang dimasukkan oleh user sudah ada dalam dummy data. Fungsi ini khusus untuk menu create.
def product_existence_create(name, data):
    for index, item in enumerate(data):
        if item['Product'].lower() == name.lower():
            prod_exist = True
            break
        else:
            prod_exist = False
    return prod_exist

# Fungsi ini akan mengembalikan value True jika nama produk yang dimasukkan oleh user sudah ada dalam dummy data. 
# Namun ada pengecualian: jika nama yang sama ada pada index yang ingin di-update user, maka fungsi akan me-return nilai False.
# Fungsi ini khusus untuk menu update.
def product_existence_update(name, data, idx):

    for index, item in enumerate(data):
        if item['Product'].lower() == name.lower():
            if idx-1 == index:
                prod_exist = False
            else:
                prod_exist = True
                break
        else:
            prod_exist = False
    return prod_exist

# Fungsi untuk menampilkan semua data
def read_data(data):
    # Jika datanya kosong, maka program akan memberi tahu bahwa data kosong
    if len(data) == 0: 
        print("Data is empty!")

    # Kalau datanya tidak kosong, maka program akan mencetak seluruh dummy data
    else: 
        print(tabulate(data, headers='keys', tablefmt='pretty'))
    
# Fungsi untuk mengonfirmasi bahwa input user adalah sebuah tanggal dengan format YYYY-MM-DD
def is_date(input_string, date_format = '%Y-%m-%d'):

    # Jika input dapat dikonversi ke datetime, maka akan fungsi akan mengembalikan nilai True
    try:
        datetime.strptime(input_string, date_format)
        return True
    
    # Namun, jika ValueError fungsi akan mengembalikan nilai False
    except ValueError:
        return False

# Fungsi untuk generate unique ID
def generate_new_id(data):

    # Mengambil ID terakhir pada dummy data
    last_id = data[-1]['ID']

    # last_id mengambil ID terakhir pada dummy data yang memiliki format 'PXXX', di mana X adalah angka.
    # Maka untuk mengambil angkanya saja, kita lakukan slicing dari index 1 sampai terakhir. Sehingga, new_id_number
    # adalah last_id[1:] + 1.
    new_id_number = int(last_id[1:]) + 1

    # Tambahkan P dan angka 0 di depan angka tersebut sampai ada empat digit angka
    new_id = f"P{new_id_number:04d}"

    # Kembalikan new_id
    return new_id

# Fungsi untuk meng-insert detail produk untuk fungsi create_data dan update_data
def insert_data():   

    # Untuk menyimpan input kuantitas 
    # Jika ValueError (karena input bukan numeric), maka user akan diberi tahu bahwa inputnya harus numerik.
    # Kemudian, user akan diminta untuk meng-input ulang kuantitas produk.
    while True:
        try:
            qty = int(input("Insert product's quantity: "))
            break
        except ValueError:
            print("Quantity has to be numeric!")

    # Untuk menyimpan input berat
    # Jika ValueError (karena input bukan numeric), maka user akan diberi tahu bahwa inputnya harus numerik.
    # Kemudian, user akan diminta untuk meng-input ulang berat produk.
    while True:
        try:
            weigh = float(input("Insert product's weight in gram: "))
            break
        except ValueError:
            print("Weight has to be numeric!")

    # Untuk menyimpan input tanggal kadaluarsa
    # Untuk mengecek apakah input berupa datetime, kita gunakan fungsi is_date() dengan input user sebagai parameternya.
    # Jika fungsi mengembalikan nilai False, maka user akan diminta untuk meng-input ulang sampai input mengikuti format tanggal yang diminta.
    while True:
        exp = input("Insert product's expired date (YYYY-MM-DD): ")
        if is_date(exp) == True:
            exp = datetime.strptime(exp, date_format).date()

            # Jika tanggal kadaluarsa yang diinput user belum lewat dari current date (belum kadaluarsa), maka looping akan berhenti. 
            if exp > current_date:
                break
            # Jika tanggal kadaluarsa yang diinput user sudah lewat dari current date, user akan diminta untuk menginput ulang tanggal kadaluarsa
            else:
                print("Product is expired! Please input a valid date!")
        else:
            print("Please follow the date's format (YYYY-MM-DD)!")
    
    
    # Untuk menyimpan input manufacturer
    # Jika input user tidak berawalan 'PT' maka user akan diminta untuk menginput ulang sampai inputnya berawalan 'PT'.
    while True:
        manu = input("Insert product's manufacturer: ")
        if manu.startswith('PT') == False:
            print("The manufacturer has to starts with \'PT\'")
        else:
            break

    # Kembalikan nilai-nilainya
    return qty, weigh, exp, manu

# Fungsi untuk memasukkan data baru ke dalam daftar dummy data
def create_data(data):
    
    print("Please provide the details of the data!")

    # Name untuk menyimpan nama produk yang diinput
    # Selama panjang karakter dari nama produk kurang dari 5 dan nama produk bersifat tidak unique, looping akan terus berjalan.
    while True:
        name = input("Insert product name (>= 5 characters): ")
        if len(name) >= 5:
            prod_exist = product_existence_create(name, data)
            if prod_exist:
                print("Product already exists. Please input a distinct product!")
            else:
                break
        else:
            print("Product name has to be 5 characters or longer!")

    # Buat variabel untuk menyimpan value yang di-return oleh fungsi insert_data()
    qty, weigh, exp, manu = insert_data() 

    # Buat sebuah dictionary untuk menyimpan semua nilai yang dikembalikan oleh fungsi insert_data
    # Index adalah len(data) + 1
    # Value dari ID adalah value yang dikembalikan oleh fungsi generate_new_id()
    myDict = {"No": len(data) + 1, 
              "ID":generate_new_id(data), 
              "Product":name, 
              "Quantity": qty, 
              "Weight (gr)": weigh, 
              "Expired Date": exp,
              "Manufacturer": manu}
    
    # Gunakan fungsi append untuk menambahkan myDict ke dalam list data
    data.append(myDict)
    print("")
    print("Data has been added. Thank you!\n")

    # Tampilkan semua data untuk mengonfirmasi bahwa data baru sudah diinput
    read_data(data)

# Fungsi untuk memperbaharui data yang sudah ada dalam dummy data
def update_data(data):
    
    # Jika datanya kosong, maka program akan mencetak "Data is empty!"
    if len(data) == 0:
        print("Data is empty!")

    # Jika datanya tidak kosong, maka program akan berlanjut
    else:

        # Tampilkan data dalam tabel
        read_data(data) 
        print("")

        # Jika index yang diinput oleh user bukan angka, maka program akan terus meminta user memasukkan kembali index dari data yang ingin dihapus.
        # Looping akan berhenti jika index yang dimasukkan user adalah angka dan berada di antara 1-jumlah data.
        while True:
            try:
                idx = int(input(f"Please insert the index of the data that you wish to update (1-{len(data)}): "))
                if idx <= 0 or idx > len(data):
                    print("Invalid index!")
                else:
                    break
            except ValueError:
                print("Index has to be numeric!")
        print("\nPlease provide the details of the data!")

        # Menerima input nama
        # Jika panjang karakter dari nama produk kurang dari lima atau nama produk sudah ada dalam data (kecuali data pada index yang ingin di-update), 
        # looping akan terus berjalan.
        while True:
            name = input("Insert product name (>= 5 characters): ")
            if len(name) >= 5:
                if product_existence_update(name, data, idx):
                    print("Product already exists. Please input a distinct product!")
                else:
                    break
            else:
                print("Product name has to be 5 characters or longer!")

        # Buat variabel untuk menyimpan value yang di-return oleh fungsi insert_data()
        qty, weigh, exp, manu = insert_data() 

        # Buat sebuah dictionary untuk menyimpan semua nilai yang dikembalikan oleh fungsi insert_data
        # Index dan ID tetap bernilai sama seperti index dari data yang ingin di-update
        myDict = {"No": data[idx-1]['No'], 
                  "ID":data[idx-1]['ID'], 
                  "Product":name, 
                  "Quantity": qty, 
                  "Weight (gr)": weigh, 
                  "Expired Date": exp, 
                  "Manufacturer": manu}
        
        # Ganti value dari data pada index yang ingin di-update sebagai myDict
        data[idx-1] = myDict

        print("\nData has been successfully updated!\n")

        # Tampilkan tabel data
        read_data(data)
    
# Fungsi untuk menghapus data yang ada dalam dummy data berdasarkan dummy data
def del_data(data):

    # Jika datanya kosong, maka program akan mencetak "Data is empty!"
    if len(data) == 0:
        print("Data is empty!")

    # Jika tidak, maka fungsi akan berlanjut
    else: 

        # Tampilkan tabel data
        read_data(data)
        print("")

        # Jika index yang diinput oleh user bukan angka, maka program akan terus meminta user memasukkan kembali index dari data yang ingin dihapus.
        # Looping akan berhenti jika index yang dimasukkan user adalah angka dan berada di antara 1-jumlah data.
        while True:
            try:
                idx = int(input(f"Please insert the index of the data that you wish to remove (1-{len(data)}): "))
                if idx <= 0 or idx > len(data):
                    print("Invalid index")
                
                # Jika input user adalah angka dan bernilai antara 1-jumlah data, maka data di index tersebut akan dihapus.
                else:
                    del data[idx - 1]
                    # Update value dari No agar tetap urut
                    update_no(data)
                    print("")
                    
                    print("\nData has been successfully removed!\n")

                    # Tampilkan tabel
                    read_data(data)
                    break
            except ValueError:
                print("Index has to be numeric!")
            
            
def print_jarak():
    for i in range(8):
        print("")

# Fungsi untuk menjahit semua function yang telah dibuat dalam bentuk menu aplikasi
def main_program():

    print('''
 __        __   _                            _          ____  _                 _      __        __             _                          
 \ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___   / ___|| |_ ___  _ __ ___( )___  \ \      / /_ _ _ __ ___| |__   ___  _   _ ___  ___ 
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  \___ \| __/ _ \| '__/ _ \// __|  \ \ /\ / / _` | '__/ _ \ '_ \ / _ \| | | / __|/ _ \\
   \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |  ___) | || (_) | | |  __/ \__ \   \ V  V / (_| | | |  __/ | | | (_) | |_| \__ \  __/
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |____/ \__\___/|_|  \___| |___/    \_/\_/ \__,_|_|  \___|_| |_|\___/ \__,_|___/\___|
                                                                                                                                           ''')    

    # Variabel untuk menyimpan menu yang dipilih user
    inp = 0

    # Jika user belum menginput angka 5, program akan terus berjalan
    while inp != '5':
        print("+===========================+")
        print("|Menu                       |")
        print("|1. View Data               |")
        print("|2. Add New Data            |")
        print("|3. Update Existing Data    |")
        print("|4. Delete Existing Data    |")
        print("|5. Exit                    |")
        print("+===========================+")
        inp = input('Choose a menu: ')
        print("")


        # Jika inp = '1', panggil fungsi read_data
        if inp == '1':
            read_data(data)
            print_jarak()
        
        # Jika inp = '2', panggil fungsi create_data
        elif inp == '2':
            create_data(data)
            print_jarak()
        
        # Jika inp = '3', panggil fungsi update_data
        elif inp == '3':
            update_data(data)
            print_jarak()

        # Jika inp = '4', panggil fungsi del_data
        elif inp == '4':
            del_data(data)
            print_jarak()
        elif inp == '5':
            print('''  _____ _                 _     __   __          
 |_   _| |__   __ _ _ __ | | __ \ \ / /__  _   _ 
   | | | '_ \ / _` | '_ \| |/ /  \ V / _ \| | | |
   | | | | | | (_| | | | |   <    | | (_) | |_| |
   |_| |_| |_|\__,_|_| |_|_|\_\   |_|\___/ \__,_|
                                                 ''')
            print_jarak()
            break

# Panggil fungsi main_program()
main_program()

    


