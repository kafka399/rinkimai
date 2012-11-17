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

class KandidatoRezultaiApygardojeItem(Item):
	apygarda = Field()
	kandidatas = Field()
	apylinkese = Field()
	pastu = Field()
	nuo_galiojanciu_biuleteniu = Field()
	nuo_rinkeju = Field()
	pass

class KandidatoRezultaiApylinkejeItem(Item):
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
	pass
