import csv
import glob
import re

provinsi_lookup = {
    'ACEH': '11',
    'BALI': '51',
    'BANGKA BELITUNG': '19',
    'BANTEN': '36',
    'BENGKULU': '17',
    'DI YOGYAKARTA': '34',
    'DKI JAKARTA': '31',
    'GORONTALO': '75',
    'JAMBI': '15',
    'JAWA BARAT': '32',
    'JAWA TENGAH': '33',
    'JAWA TIMUR': '35',
    'KALIMANTAN BARAT': '61',
    'KALIMANTAN SELATAN': '63',
    'KALIMANTAN TENGAH': '62',
    'KALIMANTAN TIMUR': '64',
    'KEPULAUAN RIAU': '21',
    'LAMPUNG': '18',
    'MALUKU': '81',
    'MALUKU UTARA': '82',
    'NUSA TENGGARA BARAT': '52',
    'NUSA TENGGARA TIMUR': '53',
    'PAPUA': '91',
    'PAPUA BARAT': '92',
    'RIAU': '14',
    'SULAWESI BARAT': '76',
    'SULAWESI SELATAN': '73',
    'SULAWESI TENGAH': '72',
    'SULAWESI TENGGARA': '74',
    'SULAWESI UTARA': '71',
    'SUMATERA BARAT': '13',
    'SUMATERA SELATAN': '16',
    'SUMATERA UTARA': '12'
}

dapil_lookup = {
    'DI YOGYAKARTA 1': '3400-01-0000',    
    'DI YOGYAKARTA 2': '3400-02-0000',    
    'DI YOGYAKARTA 3': '3400-03-0000',    
    'DI YOGYAKARTA 4': '3400-04-0000',    
    'DI YOGYAKARTA 5': '3400-05-0000',    
    'DI YOGYAKARTA 6': '3400-06-0000',    
    'DI YOGYAKARTA 7': '3400-07-0000'    
}

partai_lookup = {
    'PARTAI AMANAT NASIONAL': '8',
    'PARTAI BULAN BINTANG': '14',
    'PARTAI DEMOKRASI INDONESIA PERJUANGAN': '4',
    'PARTAI DEMOKRAT': '7',
    'PARTAI GERAKAN INDONESIA RAYA': '6',
    'PARTAI GOLONGAN KARYA': '5',
    'PARTAI HATI NURANI RAKYAT': '10',
    'PARTAI KEADILAN DAN PERSATUAN INDONESIA': '15',
    'PARTAI KEADILAN SEJAHTERA': '3',
    'PARTAI KEBANGKITAN BANGSA': '2',
    'PARTAI NASDEM': '1',
    'PARTAI PERSATUAN PEMBANGUNAN': '9'
}

# write IDs and names for partai, dapil, provinsi
write_ids = True
write_names = True
# flag for checking whether CSV headers have been written
headers_written = False
# flag for printing out feedback
be_verbose = True

# header names and order
csv_headers = ['lembaga', 'tahun', 'id_provinsi', 'nama_provinsi', 'id_dapil', 'nama_dapil', 'id_partai', 'nama_partai', 'urutan', 'id', 'nama', 'jenis_kelamin', 'agama', 'tempat_lahir', 'tanggal_lahir', 'status_perkawinan', 'nama_pasangan', 'jumlah_anak', 'kelurahan_tinggal', 'kecamatan_tinggal', 'kab_kota_tinggal', 'provinsi_tinggal', 'foto_url']

for filename in glob.glob("./input/*.csv"):
    if be_verbose:
        print('opening file ' + filename)
    with open(filename, 'rU') as f:
        if be_verbose:
            print('opened file!')
        csv_file = open("out.csv", 'a')
        writer = csv.DictWriter(csv_file, csv_headers)

        provinsi = ""
        dapil = ""
        partai = ""
        stage = 0

        for line in f:
            if be_verbose:
                print('parsing line! stage is '+str(stage))
            # strip leading & trailing whitespace
            line = line.strip()
            
            # if stage = 0 then we're looking for province
            if stage == 0:
                if "PROVINSI" in line:
                    provinsi = re.search('^PROVINSI : (.+?)$', re.split(',', line)[0].strip()).group(1)
                    provinsi = re.sub('D\.I\.', 'DI', provinsi)
                    if be_verbose:
                        print('found province '+provinsi)
                    stage = 1

            # if stage = 1 then we're looking for dapil
            elif stage == 1:
                if "DAERAH PEMILIHAN" in line:
                    dapil = re.search('^DAERAH PEMILIHAN : (.+?)$', re.split(',', line)[0].strip()).group(1)
                    dapil = re.sub('D\.I\.', 'DI', dapil)
                    if be_verbose:
                        print('found dapil '+dapil)
                    stage = 2

            # if stage = 2 then we're looking for party
            elif stage == 2:
                if "PARTAI" in line:
                    partai = re.search('^\d+? (PARTAI .+?)$', re.split(',', line)[0].strip()).group(1)
                    if be_verbose:
                        print('found party '+partai)
                    stage = 3

                elif "DAFTAR CALON TETAP" in line:
                    # we've reached the end of a dapil; start looking for the next one
                    stage = 1

            # if stage = 3 then we're looking for the beginning of a chunk of candidate data
            elif stage == 3:
                if "LENGKAP" in line:
                    candidate_chunk = []
                    candidate_chunk.append(line)
                    if be_verbose:
                        print('found beginning of candidate data chunk')
                    stage = 4

            # if stage = 4 then we're appending lines of candidate data
            elif stage == 4:
                if "JUMLAH LAKI-LAKI" not in line:
                    if be_verbose:
                        print('found line of candidate data chunk')
                    candidate_chunk.append(line)

                # the chunk is finished
                else:
                    if be_verbose:
                        print('chunk done')
                    values = csv.DictReader(candidate_chunk, delimiter=',', quotechar='"')
                    for row in values:
                        # make sure it's not a blank record
                        if row['NAMA LENGKAP'].strip() != '':
                            writeme = {}
                            if write_names:
                                writeme['nama_provinsi'] = provinsi
                                writeme['nama_dapil'] = dapil
                                writeme['nama_partai'] = partai

                            dapil_id = dapil_lookup[dapil]

                            if write_ids:
                                writeme['id_provinsi'] = provinsi_lookup[provinsi]
                                writeme['id_dapil'] = dapil_id
                                writeme['id_partai'] = partai_lookup[partai]

                            writeme['lembaga'] = "DPRDI"
                            writeme['tahun'] = "2014"
                            writeme['urutan'] = row['NOMOR URUT'].strip()

                            # candidate ID wrangling
                            partai_id_padded = partai_lookup[partai]
                            urutan_padded = row['NOMOR URUT'].strip()
                            if int(partai_id_padded) < 10:
                                partai_id_padded = "0" + partai_id_padded

                            if int(urutan_padded) < 10:
                                urutan_padded = "0" + urutan_padded

                            candidate_id = dapil_id + '-' + partai_id_padded + urutan_padded
                            writeme['id'] = candidate_id
                            
                            writeme['nama'] = row['NAMA LENGKAP'].strip()

                            '''periods = re.findall('(\w*\.\w+|\w+\.\w*)', row['NAMA LENGKAP'].strip())
                            for periodmatch in periods:
                                print(periodmatch)'''

                            # make sure gender letter is uppercased
                            writeme['jenis_kelamin'] = row['JENIS KELAMIN (L/P)'].strip().upper()
                            writeme['kab_kota_tinggal'] = row['KABUPATEN/KOTA (TEMPAT TINGGAL BAKAL CALON)'].strip().upper()
                            
                            if not headers_written:
                                if be_verbose:
                                    print('writing header:')
                                    print(csv_headers)
                                header_row = dict((h, h) for h in csv_headers)
                                writer.writerow(header_row)
                                headers_written = True

                            if be_verbose:
                                print('writing row:')
                                print(list(writeme.viewvalues()))

                            # write the row
                            writer.writerow(writeme)

                    # go back to looking for the first party
                    stage = 2

        # done writing, close the file
        if be_verbose:
            print('closing file')
        csv_file.close()
