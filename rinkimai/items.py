# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ApygardaItem(Item):
    # define the fields for your item here like:
    apygarda = Field()
    apylinkiu_skaicius  = Field()
    rinkeju_skaicius = Field()
    dalyvavo = Field()
    negaliojantys_iuleteniai = Field()

    pass

class ApylinkeItem(Item):
    # define the fields for your item here like:
    apygarda = Field()
    apylinke = Field()
    rinkeju_skaicius = Field()
    dalyvavo = Field()
    negaliojantys_biuleteniai = Field()

    pass

class DaugiamandatesRezultataiApygardojeItem(Item):
	apygarda = Field()
	partija = Field()
	apylinkese = Field()
	pastu = Field()
	nuo_galiojanciu_biuleteniu = Field()
	pass

class DaugiamandatesRezultataiApylinkejeItem(Item):
        apygarda = Field()
	apylinke = Field()
        partija = Field()
        apylinkese = Field()
        pastu = Field()
        nuo_galiojanciu_biuleteniu = Field()
        pass

class KandidatoRezultaiApygardojeItem(Item):
	apygarda = Field()
	kandidatas = Field()
	apylinkese = Field()
	pastu = Field()
	nuo_galiojanciu_biuleteniu = Field()
	nuo_rinkeju = Field()
	pass

class KandidatoRezultaiApylinkejeItem(Item):
    apygarda = Field()
    apylinke = Field()
    kandidatas = Field()
    balsadezeje = Field()
    pastu = Field()
    nuo_galiojanciu_biuleteniu = Field()
    nuo_rinkeju = Field()
    pass

class KandidatasItem(Item):
	kandidatas = Field()
	apygarda  = Field()
	iskele = Field()
	saraso_numeris = Field()
	gimimo_data  = Field()
	gyvena = Field()
	tautybe = Field()
	gimimo_vieta = Field()
	uzsienio_kalbos = Field()
	darboviete = Field()
	pomegiai  = Field()
	seimynine_padetis = Field()
	issilavinimas = Field()	
	neatlikta_bausme = Field()
	pripazintas_kaltu = Field()
	sunkus_nusikaltimas = Field()
	pass
class KandidatoDeklaracija(Item):
	kandidatas = Field()
	turtas = Field()
	vertybiniai_popieriai = Field()
	gryni_pinigai = Field()
	suteiktos_paskolos=Field()
	gautos_paskolos = Field()
	gautos_pajamos = Field()
	mokesciai = Field()
	pass
