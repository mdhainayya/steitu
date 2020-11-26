
from flask import Flask, jsonify, request
from fpdf import FPDF
from datetime import date
import os
from flask_mysqldb import MySQL
import requests
import ast

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "ka_stei"

mysql = MySQL(app)

@app.route('/')
def root():
    return "Tubes LaSTI"

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def generate_document(path, id, nama, nim, jurusan, instansi):
    COMPANY = 'SURAT PENGANTAR BEASISWA'
    COMPANY_INFO = 'Jl. Ganesha No.10, Lb. Siliwangi, Kecamatan Coblong, Kota Bandung, Jawa Barat 40132'
    LOGO_IMAGE = 'logoitb.png'
    
    p = FPDF()
    p.add_page()
    p.set_font('Arial', 'B', 20)
    p.image(LOGO_IMAGE, 10, 10, 20)
    p.cell(22, 10)
    p.cell(40, 10, COMPANY)
    p.ln()
    p.line(10, 30, 200, 30)
    p.set_font('Arial', '', 12)
    p.cell(22, 7)
    p.cell(0, 7, COMPANY_INFO)
    p.ln(15)
    p.ln()
    p.ln(5)
    p.set_font('Arial', '', 12)
    p.cell(40, 7, "Surat ini adalah sebagai pengantar beasiswa.")
    p.ln()
    p.set_font('Arial', '', 12)
    p.cell(40, 7, "ID")
    p.cell(10, 7, ":", 0, 0, 'L')
    p.cell(0, 7, str(id), 0, 0, 'L')
    p.ln(6)
    p.cell(40, 7, "Nama")
    p.cell(10, 7, ":", 0, 0, 'L')
    p.cell(0, 7, str(nama), 0, 0, 'L')
    p.ln(6)
    p.cell(40, 7, "NIM")
    p.cell(10, 7, ":", 0, 0, 'L')
    p.cell(0, 7, str(nim), 0, 0, 'L')
    p.ln(6)
    p.cell(40, 7, "Jurusan")
    p.cell(10, 7, ":", 0, 0, 'L')
    p.cell(0, 7, str(jurusan), 0, 0, 'L')
    p.ln(6)
    p.cell(40, 7, "Instansi Tujuan")
    p.cell(10, 7, ":", 0, 0, 'L')
    p.cell(0, 7, str(instansi), 0, 0, 'L')
    p.ln(15)
    p.ln(10)
    p.set_font('Arial', '', 12)
    p.cell(0, 7, "Bandung, " + date.today().strftime("%d %B %Y"), 0, 0, "R")
    p.ln(30)
    p.set_font('Arial', '', 12)
    p.cell(0, 7, "Kaprodi STI", 0, 0, "R")
    p.output(path, 'F')

@app.route('/download_kaprodi/<id>', methods=['GET'])
#mendownload file dari database dengan id_dokumen = id dan format penamaan file = doc (doc diisi dg tipe format juga cth nana.pdf)
def download_kaprodi(id):

    info = ''
    cur = mysql.connection.cursor()
    check = cur.execute("SELECT * from permintaan WHERE ID_Permintaan = %s", (id))
    
    #id yang diminta ada di database
    if check > 0:
        info = cur.fetchone()
        info_id = info[0]
        info_nama = info[1]
        info_nim = info[2]
        info_jurusan = info[3]

        check = cur.execute("SELECT * from permintaan_surat_rekomendasi WHERE ID_Permintaan = %s", (id))
        infonext = cur.fetchone()
        info_instansi = infonext[1]

        generate_document("doc.pdf", info_id, info_nama, info_nim, info_jurusan, info_instansi)

        #update status dokumen
        cur.execute("UPDATE status_permintaan SET Status = 'sedang diproses Kaprodi' WHERE ID_Permintaan = %s", (id))

        mysql.connection.commit()

        cur.close()

        return jsonify({'message':'download berhasil'})

    #id yang diminta tidak ada di database
    else:
        mysql.connection.commit()

        cur.close()

        return jsonify({'message':'id yang diminta tidak ada'})

@app.route('/download_mahasiswa/<id>', methods=['GET'])
#mendownload file dari database dengan id_dokumen = id dan format penamaan file = doc (doc diisi dg tipe format juga cth nana.pdf)
def download_mahasiswa(id):

    cur = mysql.connection.cursor()
    pdf = cur.execute("SELECT dokumen_ttd from dokumen WHERE ID_Permintaan = %s", (id))
    
    #id yang diminta ada di database
    if pdf > 0:
        pdf_file = cur.fetchone()
        doc = "doc.pdf"

        #update status dokumen

        file =  pdf_file[0]
        write_file(file, doc)

        mysql.connection.commit()

        cur.close()

        return jsonify({'message':'download berhasil'})
    #id yang diminta tidak ada di database
    else:
        mysql.connection.commit()

        cur.close()

        return jsonify({'message':'id yang diminta tidak ada'})

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

@app.route('/upload/<id>/<filename>', methods=['POST'])
def insert(id, filename):
    if request.method == 'POST':

        binaryData = convertToBinaryData(filename)

        cur = mysql.connection.cursor()

        cur.execute("UPDATE dokumen SET dokumen_ttd = %s WHERE ID_Permintaan = %s", (binaryData, id))
        cur.execute("UPDATE status_permintaan SET Status = 'Selesai' WHERE ID_Permintaan = %s", (id))

        mysql.connection.commit()

        cur.close()

        return jsonify({'message':'upload berhasil'})

@app.route('/form/<nim>/<nama>/<jurusan>/<instansi_tujuan>', methods=['POST'])
def form(nim, nama, jurusan, instansi_tujuan):

    cur = mysql.connection.cursor()

    #validasi nama dan NIM mahasiswa
    check = cur.execute("SELECT Nama from mahasiswa WHERE NIM = %s", [nim])
    check1 = cur.fetchone()
    check2 = check1[0]

    if request.method == 'POST' and check2 == nama:
        cur.execute("INSERT into permintaan (Nama, NIM, Jurusan) VALUES (%s, %s, %s)", [nama, nim, jurusan])
        cur.execute("INSERT into permintaan_surat_rekomendasi (Instansi_Tujuan) VALUES (%s)", [instansi_tujuan])
        cur.execute("INSERT into status_permintaan (Status) VALUES ('sedang divalidasi')")
        cur.execute("INSERT into dokumen (dokumen_tanpa_ttd, dokumen_ttd) VALUES ('','')")

        mysql.connection.commit()

        cur.close()
        
        return jsonify({'message':'permintaan berhasil diterima oleh sistem'})
    else:
        return jsonify({'message':'nama dan nim tidak sesuai'})

@app.route('/get-status/<id>', methods=['GET'])
def get_status(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Status from status_permintaan WHERE ID_Permintaan = %s", (id))
    status = cur.fetchone()
    result = status[0]
    mysql.connection.commit()

    cur.close()
    return jsonify(result)

if __name__ == '__main__':
    app.debug = True
    app.run()
