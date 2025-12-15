import matplotlib.pyplot as plt

def yakin_sama_grafigi(en_iyi_tarihce):
    fig = plt.figure()
    plt.plot(en_iyi_tarihce)
    plt.xlabel("Iterasyon")
    plt.ylabel("En iyi mesafe (metre)")
    plt.title("ACO Yakinsama Grafigi")
    return fig
