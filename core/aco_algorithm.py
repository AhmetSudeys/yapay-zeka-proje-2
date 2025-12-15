import numpy as np
from core.matrix_utils import rota_mesafesi_hesapla

def aco_coz(mesafe_matrisi, karinca_sayisi=30, iterasyon_sayisi=80, alfa=1.0, beta=5.0, buharlas=0.5, baslangic_index=0):
    n = len(mesafe_matrisi)

    feromon = np.ones((n, n), dtype=float)

    sezgisel = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                sezgisel[i, j] = 1.0 / max(mesafe_matrisi[i][j], 1)

    en_iyi_rota = None
    en_iyi_mesafe = float("inf")
    en_iyi_tarihce = []

    for _ in range(iterasyon_sayisi):
        tum_karinca_rotalari = []

        for _ in range(karinca_sayisi):
            rota = rota_uret(n, feromon, sezgisel, alfa, beta, baslangic_index)
            rota.append(baslangic_index)

            mesafe = rota_mesafesi_hesapla(rota, mesafe_matrisi)
            tum_karinca_rotalari.append((rota, mesafe))

            if mesafe < en_iyi_mesafe:
                en_iyi_mesafe = mesafe
                en_iyi_rota = rota

        en_iyi_tarihce.append(en_iyi_mesafe)

        feromon *= (1.0 - buharlas)

        for rota, mesafe in tum_karinca_rotalari:
            feromon_miktari = 1.0 / max(mesafe, 1)
            for i in range(len(rota) - 1):
                a = rota[i]
                b = rota[i+1]
                feromon[a, b] += feromon_miktari
                feromon[b, a] += feromon_miktari

    return en_iyi_rota, en_iyi_mesafe, en_iyi_tarihce

def rota_uret(n, feromon, sezgisel, alfa, beta, baslangic_index):
    ziyaret_edildi = set([baslangic_index])
    rota = [baslangic_index]

    while len(ziyaret_edildi) < n:
        mevcut = rota[-1]
        olasiliklar = olasilik_hesapla(mevcut, ziyaret_edildi, n, feromon, sezgisel, alfa, beta)
        secilen = np.random.choice(range(n), p=olasiliklar)
        rota.append(secilen)
        ziyaret_edildi.add(secilen)

    return rota

def olasilik_hesapla(mevcut, ziyaret_edildi, n, feromon, sezgisel, alfa, beta):
    agirliklar = np.zeros(n, dtype=float)

    for j in range(n):
        if j in ziyaret_edildi:
            agirliklar[j] = 0.0
        else:
            agirliklar[j] = (feromon[mevcut, j] ** alfa) * (sezgisel[mevcut, j] ** beta)

    toplam = agirliklar.sum()
    if toplam == 0:
        secilebilir = [j for j in range(n) if j not in ziyaret_edildi]
        olasiliklar = np.zeros(n, dtype=float)
        pay = 1.0 / len(secilebilir)
        for j in secilebilir:
            olasiliklar[j] = pay
        return olasiliklar

    return agirliklar / toplam
