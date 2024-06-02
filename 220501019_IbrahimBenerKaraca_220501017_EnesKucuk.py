import sys
import itertools
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, \
    QGraphicsEllipseItem, QPushButton, QGraphicsTextItem, QGraphicsLineItem, QVBoxLayout, QWidget, QLineEdit, QInputDialog, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QBrush, QFont, QPixmap

class MantikKapisi:
    def __init__(self, isim):
        self.isim = isim
        self.cikti = None

    def ciktiyi_al(self):
        self.cikti = self.kapi_mantigini_gerceklestir()
        return self.cikti

class TekGirisliKapi(MantikKapisi):
    def __init__(self, isim):
        super().__init__(isim)
        self.giris = None

    def girisi_ayarla(self, giris_degeri):
        self.giris = giris_degeri

class CiftGirisliKapi(MantikKapisi):
    def __init__(self, isim):
        super().__init__(isim)
        self.giris1 = None
        self.giris2 = None

    def girisleri_ayarla(self, giris1_degeri, giris2_degeri):
        self.giris1 = giris1_degeri
        self.giris2 = giris2_degeri

class NotKapisi(TekGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return not self.giris

class AndGate(CiftGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return self.giris1 and self.giris2

class OrGate(CiftGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return self.giris1 or self.giris2

class BufferGate(TekGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return self.giris

class XorGate(CiftGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return self.giris1 != self.giris2

class XnorGate(CiftGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return self.giris1 == self.giris2

class NorGate(CiftGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return not (self.giris1 or self.giris2)

class NandGate(CiftGirisliKapi):
    def kapi_mantigini_gerceklestir(self):
        return not (self.giris1 and self.giris2)

class KapiOgesi(QGraphicsPixmapItem):
    def __init__(self, kapi, x, y, image_path):
        super().__init__()
        self.setPixmap(QPixmap(image_path).scaled(40, 40))
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.kapi = kapi

        self.metin = QGraphicsTextItem(self.kapi.isim, self)
        self.metin.setPos(-10, -10)
        self.metin.setDefaultTextColor(Qt.white)
        self.metin.setFont(QFont("Arial", 10, QFont.Bold))

    def mouseDoubleClickEvent(self, event):
        print(self.kapi.ciktiyi_al())

class BaglantiOgesi(QGraphicsLineItem):
    def __init__(self, baslangic_ogesi, son_ogesi):
        super().__init__()
        self.baslangic_ogesi = baslangic_ogesi
        self.son_ogesi = son_ogesi
        self.guncel_pozisyonu_guncelle()

    def guncel_pozisyonu_guncelle(self):
        cizgi = QLineF(self.baslangic_ogesi.scenePos(), self.son_ogesi.scenePos())
        self.setLine(cizgi)

class MantikKapisiUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.girisler = []
        self.kapilar = []
        self.baglanti_ogeleri = []
        self.led = None
        self.ana_pencere_olustur()
        self.arac_cubugu_olustur()
        self.dogruluk_tablosu = []

    def ana_pencere_olustur(self):
        self.setWindowTitle("Mantık Kapısı Simülatörü")
        self.setGeometry(100, 100, 800, 600)
        self.sahne = QGraphicsScene()
        self.goruntu = QGraphicsView(self.sahne)

        merkezi_widget = QWidget()
        yerlesim = QVBoxLayout()
        yerlesim.addWidget(self.goruntu)
        merkezi_widget.setLayout(yerlesim)
        self.setCentralWidget(merkezi_widget)

    def arac_cubugu_olustur(self):
        arac_cubugu = self.addToolBar("Araçlar")

        and_butonu = QPushButton("AND Kapısı", self)
        and_butonu.clicked.connect(lambda: self.kapi_ekle(AndGate("AND"), "and.png"))
        arac_cubugu.addWidget(and_butonu)

        or_butonu = QPushButton("OR Kapısı", self)
        or_butonu.clicked.connect(lambda: self.kapi_ekle(OrGate("OR"), "or.png"))
        arac_cubugu.addWidget(or_butonu)

        not_butonu = QPushButton("NOT Kapısı", self)
        not_butonu.clicked.connect(lambda: self.kapi_ekle(NotKapisi("NOT"), "not.png"))
        arac_cubugu.addWidget(not_butonu)

        buffer_butonu = QPushButton("BUFFER Kapısı", self)
        buffer_butonu.clicked.connect(lambda: self.kapi_ekle(BufferGate("BUFFER"), "buffer.png"))
        arac_cubugu.addWidget(buffer_butonu)

        xor_butonu = QPushButton("XOR Kapısı", self)
        xor_butonu.clicked.connect(lambda: self.kapi_ekle(XorGate("XOR"), "xor.png"))
        arac_cubugu.addWidget(xor_butonu)
        xnor_butonu = QPushButton("XNOR Kapısı", self)
        xnor_butonu.clicked.connect(lambda: self.kapi_ekle(XnorGate("XNOR"), "xnor.png"))
        arac_cubugu.addWidget(xnor_butonu)

        nor_butonu = QPushButton("NOR Kapısı", self)
        nor_butonu.clicked.connect(lambda: self.kapi_ekle(NorGate("NOR"), "nor.png"))
        arac_cubugu.addWidget(nor_butonu)

        nand_butonu = QPushButton("NAND Kapısı", self)
        nand_butonu.clicked.connect(lambda: self.kapi_ekle(NandGate("NAND"), "nand.png"))
        arac_cubugu.addWidget(nand_butonu)

        giris_sayisi_girisi = QLineEdit(self)
        giris_sayisi_girisi.setPlaceholderText("Giriş sayısını girin")
        arac_cubugu.addWidget(giris_sayisi_girisi)

        giris_ekle_butonu = QPushButton("Giriş Ekle", self)
        giris_ekle_butonu.clicked.connect(lambda: self.giris_ekle(int(giris_sayisi_girisi.text()), "giris.png"))
        arac_cubugu.addWidget(giris_ekle_butonu)

        calistir_butonu = QPushButton("Çalıştır", self)
        calistir_butonu.clicked.connect(self.calistir)
        arac_cubugu.addWidget(calistir_butonu)

    def giris_ekle(self, sayi, image_path):
        for i in range(sayi):
            deger, _ = QInputDialog.getInt(self, "Giriş Değeri", f"Giriş {i + 1} değerini girin (0 veya 1):", min=0,
                                           max=1)
            giris_oge = QGraphicsPixmapItem(QPixmap(image_path).scaled(40, 40))
            giris_oge.setPos(100, 100 + i * 50)
            giris_oge.setFlag(QGraphicsItem.ItemIsMovable)

            metin = QGraphicsTextItem(str(deger), giris_oge)
            metin.setPos(15, 10)
            metin.setDefaultTextColor(Qt.white)
            metin.setFont(QFont("Arial", 10, QFont.Bold))

            self.sahne.addItem(giris_oge)
            self.girisler.append((giris_oge, deger))

    def kapi_ekle(self, kapi, image_path):
        kapi_oge = KapiOgesi(kapi, 300, 200 + len(self.kapilar) * 100, image_path)
        self.sahne.addItem(kapi_oge)
        self.kapilar.append(kapi_oge)
        if len(self.kapilar) > 1:
            self.baglanti_ekle(self.kapilar[-2], kapi_oge)

    def baglanti_ekle(self, baslangic_ogesi, son_ogesi):
        baglanti_ogesi = BaglantiOgesi(baslangic_ogesi, son_ogesi)
        self.sahne.addItem(baglanti_ogesi)
        self.baglanti_ogeleri.append(baglanti_ogesi)

    def calistir(self):
        if not self.kapilar:
            return

        giris_degerleri = [giris[1] for giris in self.girisler]

        for i, kapi_oge in enumerate(self.kapilar):
            kapi_oge.kapi.girisleri_ayarla(*giris_degerleri[i * 2: i * 2 + 2])

        for kapi_oge in self.kapilar:
            print(f"{kapi_oge.kapi.isim} kapısı çıktısı: {kapi_oge.kapi.ciktiyi_al()}")

        if self.led is not None:
            if self.kapilar[-1].kapi.ciktiyi_al():
                self.led.setBrush(QBrush(Qt.red))
            else:
                self.led.setBrush(QBrush(Qt.red))

    def led_ekle(self):
        if self.led is None:
            self.led = QGraphicsEllipseItem(0, 0, 40, 40)
            self.led.setPos(500, 500)
            self.led.setBrush(QBrush(Qt.gray))
            self.sahne.addItem(self.led)

    def calistir(self):
        if not self.kapilar:
            return

        if self.led is None:
            self.led_ekle()

        self.dogruluk_tablosu.clear()

        giris_degerleri = [giris[1] for giris in self.girisler]

        for i, kapi_oge in enumerate(self.kapilar):
            kapi_oge.kapi.girisleri_ayarla(*giris_degerleri[i * 2: i * 2 + 2])


        girdi_kolonlari = [f"Giriş {i + 1}" for i in range(len(self.girisler))]
        girdi_kolonlari.append("Çıkış")

        self.dogruluk_tablosu.append(girdi_kolonlari)

        for kombinasyon in itertools.product([0, 1], repeat=len(self.girisler)):
            satir = list(kombinasyon)
            for kapi_oge in self.kapilar:
                cikti = kapi_oge.kapi.ciktiyi_al()
                satir.append(1 if cikti else 0)
            self.dogruluk_tablosu.append(satir)


        for satir in self.dogruluk_tablosu:
            print("\t".join(map(str, satir)))


        if self.kapilar[-1].kapi.ciktiyi_al():
            self.led.setBrush(QBrush(Qt.red))
        else:
            self.led.setBrush(QBrush(Qt.gray))


        if self.led.scene() is None:
            self.sahne.addItem(self.led)


        self.led.setPos(500, 500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    uygulama = MantikKapisiUygulamasi()
    uygulama.led_ekle()
    uygulama.show()
    sys.exit(app.exec_())

