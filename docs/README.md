# Tennis Grand Ranking
Tämä repositorio on tarkoitettu [Aineopintojen harjoitustyö: Tietokantasovellus -kurssin](https://courses.helsinki.fi/fi/tkt20011/124960890) suorittamiseksi. Tavoitteena on luoda Python-backendia – erityisesti Flask-kirjastoa – käyttävä verkkosovellus.

## Demosovellus
[Herokussa pyörivä demosovellus](https://tsoha-rankkauslista.herokuapp.com/) löytyy painamalla linkkiä. Järjestelmän testitunnukset eri käyttäjäryhmille ovat:

- ylläpitäjän/lajiliiton testitunnukset:
    - käyttäjätunnus: testaaja
    - salasana: testaaja
- turnausjärjestäjän testitunnukset:
    - käyttäjätunnus: turnausj
    - salasana: turnausj
- pelaaja-agentin testitunnukset:
    - käyttäjätunnus: pagentti
    - salasana: pagentti

## Dokumentaatio
* [Tietokantakaavio](/docs/images/ermodel.png)
* [Asennusohje](https://github.com/mremes/tsoha-rankkauslista#asennusohje)
* [Käyttöohje](https://github.com/mremes/tsoha-rankkauslista#k%C3%A4ytt%C3%B6ohje)
* [User storiet](/docs/user_stories.md)
* [Käyttäjäryhmät](https://github.com/mremes/tsoha-rankkauslista/blob/master/docs/user_stories.md#k%C3%A4ytt%C3%A4j%C3%A4ryhm%C3%A4t)
* [CREATE TABLE-lauseet](https://github.com/mremes/tsoha-rankkauslista/blob/master/docs/create_statements.sql)

## Asennusohje - oma ympäristö
Voit asentaa tämän sovelluksen omalle koneellesi. Oletetaan, että sinulla on käytössäsi Pythonista versio 3.6.6 tai uudempi.

Aja seuraavat komennot hakemiston juuresta.

1. Asenna riippuudet
```
pip install -r requirements.txt
```

## Käynnistysohje - oma ympäristö

1. Aja sovellus (hakemiston juuresta)
```
python run.py
```

## Asennus ja käynnistys Docker-konttina
Vaihtoehtoisesti voit käynnistää sovelluksen Docker-konttina käyttäen juuressa olevaa `Dockerfile`-tiedostoa. Jos sinulla on `docker`-komentorivityökalut asennettuna niin aja seuraavat komennot projektin juuressa:

```
docker build . -t tsoha
docker run -p 127.0.0.1:5000:5000 --name tsoha tsoha
```

## Docker-imagen lataus ja käynnistys

```
docker run -d -p 127.0.0.1:5000:5000 --name tsoha mrremes/tsoha-rankkauslista:latest
```

## Käyttöohjeet
Kun olet käynnistänyt lokaalin instanssin sovelluksesta, pääset siihen käsiksi seuraavasti:

1. Käytä sovellusta Internet-selaimella osoitteessa [http://localhost:5000](http://localhost:5000).

2. Rekisteröi itsesi järjestelmään "Rekisteröidy" -painikkeesta.

Jos haluat käyttää [Herokussa toimivaa versiota](https://tsoha-rankkauslista.herokuapp.com/), niin toimi näin:

1. Valitse jotkin käyttäjätunnukset tämän tiedoston yllä olevasta käyttäjätunnuslistasta.

2. Kirjaudu tunnuksilla sisään.

3. Käytä niitä toiminnallisuuksia, jotka valitsemasi käyttäjän roolille ovat sallittu.

#### Tyypillinen "käyttöpolku" ylläpitäjälle
1. Luo tunnus ylläpitäjä-roolilla
2. Kirjaudu sisään tunnuksilla
3. Lisää pelaaja
4. Lisää toinen pelaaja
5. Luo ranking-lista (johon luodut pelaajat sopivat)
6. Lisää pelaajat ranking-listalle (nyt ranking-listalla on kaksi pelaajaa)
7. Luo turnaus 2 pelaajan välille
8. Syötä saatavat ranking-pisteet turnauksessa
9. Syötä turnauksen tulos
10. Lopeta turnaus
11. Tarkastele uutta ranking-listan tilannetta

## Aiheen kuvaus
Toteutettava verkkosovellus on rekisteröityjen tenniksen harrastajien rankkaukseen sekä tennisturnauksen järjestämisen tueksi tarkoitettu verkkojärjestelmä. Ajatuksena on toteuttaa turnauksille soveltuva rankkausmenetelmä sekä tarvittavat web-pohjaiset tietojensyöttö- ja esitystoiminnot.

Sovellus koostuu pelaajarekisteristä, rankkauslistarekisteristä, sekä turnausluontiportaalista ja turnausrekisteristä. Pelaajarekisteriin lisätään pelaajia pelaaja-agenttien toimesta, ja turnausjärjestäjät laativat turnauksia. Ylläpitäjät tekevät kaikkea, ja erityisesti hyväksyvät turnausjärjestäjien syöttämät turnaustulokset.

Aihe- ja vaatimusmäärittelyn pohjana tulen käyttämään [ohjeissa esitetettyä aihe-esitystä](http://advancedkittenry.github.io/suunnittelu_ja_tyoymparisto/aiheet/Rankkauslista.html) vastaavasta sovelluksesta.

### Entiteetit
* Pelaaja
* Ranking
* Ranking-lista
* Ranking-kirjaus
* Ottelu
* Turnaus
* Turnauspelaaja
* Turnausottelu
* Turnauspalkinto

#### Lajiliitto
Lajiliitto on yhtä tai useampaa ranking-listaa operoiva elin, joka määrittää turnausten arvon ja tarjoaa turnauskaaviopohjan. Esimerkiksi eri pelaajaryhmille on oma lajiliittonsa. Lajiliittona voi toimia joko luonnollinen henkilö (operaattori) tai lajiliiton operaattoria esittävä tekoäly.

Lajiliitto on käytännössä järjestelmän ylläpitäjä.

#### Pelaajat
Jotta pelaaja olisi mukana ranking-listalla, hänet täytyy ensin rekisteröidä järjestelmään. Pelaajan rekisteröinnissä määritetään pelaajan nimi, sukupuoli ja syntymäaika.

Pelaajan voi rekisteröidä sopivalle ranking-listalle. Kun pelaaja on rekisteröity lajilistalle, hänet voi asetella turnauksiin. Pelaaja saa turnauksen peleistä ranking-pisteitä, jotka kertyvät ranking-listan turnauksista.

Pelaajaprofiileista on olemassa näkymä, joista selviää perustietojen lisäksi mm. pelaajan turnaushistoria sekä ranking-arvon kehitys aikajanalla.

#### Ranking-lista
Ranking-lista on kokoelma sille sopivia pelaajia. Sopivia pelaajia voi rajata syntymäajan ja sukupuolen perusteella.

Turnauksia järjestetään tietyille ranking-listoille, jolloin turnausmenestys vaikuttaa pelaajan sen listan ranking-pisteisiin.


#### Ranking ja ranking-kirjaus
Ranking on entiteetti, joka määrittää mille listalle kukakin pelaaja kuuluu.

Ranking-kirjaus on jonkin ajan ranking-tilanne. Ranking-kirjauksia tulee lisää kun pelaajan ranking-pisteet muuttuvat.

#### Ranking-pisteytys
Ranking-pisteiden laskentamenetelma tulee olemaan variaatio [ATP-järjestön käyttämästä menetelmästä](https://en.wikipedia.org/wiki/ATP_Rankings#Ranking_method). Järjestelmä tulee mahdollistamaan rinnakkaisten listojen ylläpidon (esim. erillinen lista eri sukupuolille, ikäluokille tai pelimuodoille [esim. kaksin- ja nelinpelit]). Ranking-pisteiden laskennan syötteenä toimivat turnausten tuloskaaviot, jotka pohjautuvat manuaalisesti laadittuihin turnauskaavioihin.

Ranking-pisteytetyt pelaajat kuuluvat ranking-listalle. Lista päivittyy reaaliaikaisesti, ja sillä on olemassa operaattorin ja yleisön näkymä.

#### Turnaukset ja turnausvaiheet
Tennisturnaukset järjestetään [cup-menetelmällä](https://en.wikipedia.org/wiki/Single-elimination_tournament). Turnauksille luodaan järjestelmän puolesta turnauskaaviopohja, joka täytetään – manuaalisesti tai tekoälyn generoimana tulevissa versioissa – siten, että ranking-listassa korkeimmalla olevat kohtaisivat turnauksen loppupäässä.

Turnausvaiheet ovat cup-järjestelmän vaiheita, joihin pelaajat etenevät edeltävien turnausvaiheiden ottelulopputuloksien mukaan. Turnaussijoitukset määrittävät pelaajien palkinnot sekä ranking-pistekertoimet.

Järjestelmä tarjoaa turnauskaavion laadintaan työkalun, joka mm. validoi turnaukseen osallistuvien pelaajien olevan rekisteröity järjestelmään ja muuten laadittu oikein. Täytetyt turnauskaaviot syötetään järjestelmään turnausjärjestäjien toimesta. Liitto (ylläpitäjä) kirjaa turnauksen sijoituksille ranking-pisteet ja lopettaa turnauksen, jonka jälkeen pisteet päivittyvät välittömästi.

#### Ottelut
Ottelut ovat kahden pelaajaentiteetin (kaksinpelitenniksessä kahden pelaajan ja nelinpelitenniksessä neljän pelaajan) välisiä kamppailuja, joissa toinen otteluparin pelaajista etenee seuraavaan vaiheeseen.

Ottelutoiminnallisuus ei ole toteutettu projektin nykyisessä versiossa vaan on laajennettavissa seuraaviin versioihin.

## Arkkitehtuuri
Projekti toteutetaan MVC-mallin pohjalta. Model- ja Controller-toiminnallisuus toteutetaan kurssin vaatimusten mukaisesti käyttäen Flask- ja muita relevantteja Python-kirjastoja käyttäen.

Viewin toteuttamiseen ajatuksena on käyttää Flaskin URL-prosesoreita, renderöityä Jinja2-HTML-templaatteja sekä Bootstrapin HTML/CSS/JS-kirjastoja. Mahdollisesti kokeilen myös implementoia joitakin frontin osa-alueita oppimismielessä ReactJS:llä aikaresurssien mahdollistamissa rajoissa.
