Seimo rinkimų rezultatai.

**TODO**

   * 2012 daugiamandatės - DONE
   * bendra suvestinė 2012,2008,2004  
   * 2012, 2008 II turas - DONE
   * 2000 - DONE
   * 1996 - DONE
   * pataisyti failų pavadinimus - DONE
   * kandidatu deklaracijos - DONE
      + 1996 - DONE      
      + 2000 - DONE
      + 2004 - DONE
      + 2008 - DONE
      + 2012 - DONE
   * kandidatu anketos - DONE
      + vienmandates _ DONE
      + daugiamandates - DONE
   * išrinkti Seimo nariai

**Failų aprašymas**

   + vienmandate20XX__apylinkeitem.csv - apylinkių aktyvumo suvestinė. Pvz. ["Balsavimo rezultatai rinkimų apylinkėse"][1]
   + vienmandate20XX_kandidatorezultaiapygardojeitem.csv - pvz. ["Balsavimo rezultatai apygardoje"][1] 
   + vienmandate20XX_kandidatorezultaiapylinkejeitem.csv - pvz. ["Balsavimo rezultatai rinkimų apylinkėje"][2]
   + kandidatasXXXX_kandidatasitem.csv - aprašymas ["Kandidato biografija"][3]
   + kandidatas DaugiamantatejeXXXX - kandidatasitem.csv - visi kandidatai 
   + kandidatoDeklaracija2004_kandidatodeklaracija.csv - turto deklaracija - pvz. [gyventojų turto ir pajamų deklaracijos pagrindinių duomenų išrašas][6]
   + daugiamandate20XX_daugiamandatesrezultataiapylinkejeitem - [daugiamandatės rez. apylinkėse][4]
   + daugiamandate20XX_daugiamandatesrezultataiapygardojeitem - [daugiamandatės rez. apygardose][5]
   
    

[1]: http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_vienmand_apygardose/rezultatai_vienmanate_apygarda7215aktyvumasdesc1turas.html
[2]: http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_vienmand_apygardose/rezultatai_apylinke219704visodesc1turas.html
[3]: http://www.vrk.lt/rinkimai/416_lt/Kandidatai/Kandidatas67066/Kandidato67066Anketa.html
[4]: http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_daugiamand_apygardose/apygardos_rezultatai7213.html
[5]: http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_daugiamand_apygardose/rezultatai_daugiamand_apygardose1turas.html
[6]: http://www3.lrs.lt/n/rinkimai/20001008/kandvl.htm-143962.htm
**Pastabos**

   + 2000 m. antro turo nebuvo.
   + Apibendrinti atstovybių ir kiekvienos atstovybės rezultai saugomi kaip apylinkės - duomenis dubliuojasi


**Žinomos klaidos**
kandidatas2000_kandidatasitem.csv

   + sunkus_nusikaltimas stulpelyje viena bloga reiksme

vienmandate2004_2_kandidatorezultaiapygardojeitem.csv

   + **FIXED** http://www3.lrs.lt/rinkimai/2004/seimas/rezultatai/rezv_apg_l_1603_2.htm - tik po vien kandidata apygardoje yra? Fix: td/a/text

2004
   + **FIXED** Kaip del diplomatiniu atstovybiu duomenu? Rinkeju skaicius nemazas iseina. Dabar atrodo nepateikiami sitie duomenys? http://www3.lrs.lt/rinkimai/2004/seimas/rezultatai/rezv_apg_l_1603_1.htm

1996 daugiamandate 
   + **FIXED** blogas encodingas

2004_2_apylinkeitem:
    + 513, 621 eilutes vietoje rinkeju skaiciaus atsiranda procentai. Problema velgi su tom eilutemis, kur rezultatus skaiciavo apygardoje.

2012_apylinkeitem:
   + 698, 743 tas pats.

2004_apylineitem:
   + 1062, 589 - rinkeju skaiciaus langelyje procentas.
   + 499 - negaliojanciu_biuleteniu NA reiksme. Cia ir svetaineje taip raso. Jei nera negaliojanciu biuleteniu, tai nuli reiktu rasyt, o cia tuscia palieka. 
