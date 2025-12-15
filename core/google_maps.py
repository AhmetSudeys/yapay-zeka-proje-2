import googlemaps

def gmaps_client_olustur(api_key: str):
    return googlemaps.Client(key=api_key)

def mesafe_matrisi_olustur(gmaps, koordinatlar, mode="driving"):
    noktalar = [f"{lat},{lng}" for lat, lng in koordinatlar]

    yanit = gmaps.distance_matrix(
        origins=noktalar,
        destinations=noktalar,
        mode=mode
    )

    n = len(noktalar)
    matris = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            eleman = yanit["rows"][i]["elements"][j]
            if eleman["status"] != "OK":
                raise ValueError(f"Mesafe alinamadi: {i}->{j} status={eleman['status']}")
            matris[i][j] = eleman["distance"]["value"]

    return matris
