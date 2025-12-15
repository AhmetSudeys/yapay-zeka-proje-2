def rota_mesafesi_hesapla(rota, mesafe_matrisi):
    toplam = 0
    for i in range(len(rota) - 1):
        toplam += mesafe_matrisi[rota[i]][rota[i+1]]
    return toplam
