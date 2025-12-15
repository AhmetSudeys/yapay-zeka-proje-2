import pandas as pd
import pydeck as pdk

def rota_haritasi_olustur(rota, koordinatlar, isimler=None):
    noktalar = []
    for idx in rota:
        lat, lng = koordinatlar[idx]
        isim = isimler[idx] if isimler else str(idx)
        noktalar.append({"lat": lat, "lon": lng, "isim": isim})

    df_nokta = pd.DataFrame(noktalar)

    line_coords = [[row["lon"], row["lat"]] for _, row in df_nokta.iterrows()]
    df_line = pd.DataFrame([{"path": line_coords}])

    layer_points = pdk.Layer(
        "ScatterplotLayer",
        data=df_nokta,
        get_position="[lon, lat]",
        get_radius=60,
        pickable=True
    )

    layer_line = pdk.Layer(
        "PathLayer",
        data=df_line,
        get_path="path",
	get_color=[255, 0, 0],
        width_scale=10,
        width_min_pixels=4
    )

    view_state = pdk.ViewState(
        latitude=df_nokta["lat"].mean(),
        longitude=df_nokta["lon"].mean(),
        zoom=12
    )

    return pdk.Deck(
        layers=[layer_line, layer_points],
        initial_view_state=view_state,
        tooltip={"text": "{isim}"}
    )
