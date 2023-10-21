import stadata as stat

def test_view_statictable(token):
    client = stat.Client(token)
    result = client.view_statictable("0000","2215",lang='ind')
    assert result[0][0] == "Angka Kelahiran Hasil Long Form SP2020 Menurut Kelompok Umur Ibu  (Age Spesific Fertility Rate/ASFR) dan Provinsi/Kabupaten/Kota, 2020"
    result = client.view_statictable("0000","2215",lang='eng')
    assert result[0][0] == "Birth Rate Long Form SP2020 Result by Mother's Age Group (Age  Spesific Fertility Rate/ASFR) and Province/Regency/City, 2020"
    
def test_view_dynamictable(token):
    client = stat.Client(token)
    result = client.view_dynamictable("0000","70")
    assert result.iloc[2,7] == 28.77
    
def test_view_pressrelease(token):
    client = stat.Client(token)
    result = client.view_pressrelease("0000","2035")
    assert result.desc()['title'] == 'Gini Ratio Maret 2023 tercatat sebesar 0,388.'
    
def test_view_publication(token):
    client = stat.Client(token)
    result = client.view_publication("0000","fafd73df0c782f4c2302fd1a")
    assert result.desc()['title'] == 'Buletin Statistik Perdagangan Luar Negeri Impor Mei 2023'