# teaching-application-project
Sovelluksen nykytila:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
Opiskelija näkee listan kursseista ja voi liittyä kurssille.
Opiskelija voi lukea kurssin tekstimateriaalia sekä ratkoa kurssin tehtäviä.
Opiskelija pystyy näkemään tilaston, montako kurssin tehtävää on ratkonut.
Tehtävä katsotaan ratkotuksi vasta, kun tehtävään on vastattu täysin virheettömästi.
Opiskelija näkee tehtävään vastattuaan, tiedon siitä, mitkä vastauksista olivat väärin ja mitkä taas oikein.
Opettaja pystyy luomaan uuden kurssin, muuttamaan olemassa olevaa kurssia ja poistamaan kurssin.
Opettaja pystyy lisäämään kurssille tekstimateriaalia ja opetettavia merkkejä ja sanoja. Tehtävä on tekstikenttä, johon tulee kirjoittaa oikea vastaus.
Opettaja pystyy näkemään kurssistaan tilaston, keitä opiskelijoita on kurssilla ja montako kurssin tehtävää jokainen on ratkonut.

Sovellus ei ole testattavissa Fly.iossa, joten alla on ohjeet sovelluksen käynnistämiseksi paikallisesti:

Kloonaa repositorio koneellesi ja siirry sen juurikansioon. Luo .env-tiedosto ja määritä sen sisältö seuraavalla tavalla:

DATABASE_URL=tietokantasi-paikallinen-osoite

SECRET_KEY=salainen-avain

Seuraavaksi aktivoi virtuaaliympäristö komennoilla
python3 -m venv venv
source venv/bin/activate

asenna sovelluksen riippuvuudet komennolla
pip install -r ./requirements.txt

ja määritä tietokannan skeema komennolla
psql < schema.sql

Tämän jälkeen voit käynnistää sovelluksen komennolla
flask run


Sovelluksen kuvaus:

Opetussovellus vieraiden kielten kirjoitusjärjestelmän ja sanaston opiskelun tueksi.
Sovelluksen avulla voidaan järjestää verkkokursseja eri kielten kirjoitusjärjestelmien ja sanojen opiskeluun. Kursseilla on tekstimateriaalia ja automaattisesti tarkastettavia tehtäviä. Jokainen käyttäjä on opettaja tai opiskelija. Kursseilla voidaan opettaa sellaisia kieliä, jotka eivät käytä latinalaista aakkostoa (esim. kreikka, heprea, akkadi, sumeri), ja kielen opiskelu koostuu tällöin kurssilla esimerkiksi kahdesta tasosta, joista jokaisen tarkoituksena on tutustua paremmin kielen kirjoitusjärjestelmään ja sanastoon: 
1. kirjoitusjärjestelmään kuuluvien merkkien harjoittelu (mikäli merkkejä on kielessä paljon, voi olla tarpeen ja hyödyllistä järjestää useampi kurssi)
2. ja opituilla merkeillä kirjoitettujen ja/tai translitteroitujen sanojen opettelu.

Näiden sovelluksen tasojen läpäisemisen jälkeen siirtyminen kielen varsinaiseen opiskeluun pitäisi olla helpompaa, kun kielen merkistö on osin tai kokonaan tuttu.

