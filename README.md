# tsoha-rankkauslista

Tämä repositorio on tarkoitettu [Aineopintojen harjoitustyö: Tietokantasovellus -kurssin](https://courses.helsinki.fi/fi/tkt20011/124960890) suorittamiseksi. Tavoitteena on luoda Python-backendia – erityisesti Flask-kirjastoa – käyttävä verkkosovellus.

## Aiheen kuvaus
Toteutettava verkkosovellus on rekisteröityjen tenniksen harrastajien rankkaukseen tarkoitettu verkkojärjestelmä. Ajatuksena on turnauksille soveltuva rankkausmenetelmä sekä tarvittavat web-pohjaiset tietojensyöttö- ja esitystoiminnot.

Aihe- ja vaatimusmäärittelyn pohjana tulen käyttämään [ohjeissa esitetettyä aihe-esitystä](http://advancedkittenry.github.io/suunnittelu_ja_tyoymparisto/aiheet/Rankkauslista.html) vastaavasta sovelluksesta.

### Entiteetit
* Lajiliitto
* Pelaaja
* Turnaus
* Turnausvaihe
* Ottelu
* Ranking-pisteytys

#### Lajiliitto
Lajiliitto on yksittäistä ranking-listaa operoiva elin, joka määrittää turnausten arvon ja -kaaviot. Esimerkiksi eri pelaajaryhmille on oma lajiliittonsa. Lajiliittona voi toimia joko luonnollinen henkilö (operaattori) tai lajiliiton operaattoria esittävä tekoäly.

#### Pelaajat
Jotta pelaaja olisi mukana ranking-listalla, hänet täytyy rekisteröidä järjestelmään. Pelaajan rekisteröinnissä määritetään minkä lajiliiton alle pelaaja kuuluu. Kun pelaaja on rekisteröity lajilistalle, hänet voi asettaa turnauslistoille ja hänellä on jokin ranking-arvo. Pelaajaprofiileista on olemassa liitto-operaattorin näkymä sekä yleisön näkymä, joista selviää mm. pelaajan turnaushistoria ja ranking-arvon kehitys aikajanalla.

#### Turnaukset ja turnausvaiheet
Tennisturnaukset järjestetään [cup-menetelmällä](https://en.wikipedia.org/wiki/Single-elimination_tournament). Turnauksille luodaan turnauskaaviopohja, jotka laaditaan – manuaalisesti – siten, että ranking-listassa korkeimmalla olevat kohtaavat turnauksen loppupäässä.

Lajiliitto päättää turnauksen arvoista, joilla luodaan yksittäisten turnausten sijoituskohtainen pisteytys. Turnauksen arvoon vaikuttaa mm. palkintosumma ja turnaukseen osallistuvien pelaajien ranking-sijoitukset ja turnauksen historia.

Turnausvaiheet ovat cup-järjestelmän vaiheita, joihin pelaajat etenevät edeltävien turnausvaiheiden ottelulopputuloksien mukaan. Turnausvaiheet määrittävät pelaajien palkinnot sekä ranking-pistekertoimet.

Järjestelmä tarjoaa turnauskaavion laadintaan työkalun, joka mm. validoi turnaukseen osallistuvien pelaajien olevan rekisteröity järjestelmään. Täytetyt turnauskaaviot syötetään järjestelmään kertakäyttöisellä avaimella kirjautumalla lomakkeentäyttösivulle.

#### Ottelut
Ottelut ovat kahden pelaajaentiteetin (kaksinpelitenniksessä kahden pelaajan ja nelinpelitenniksessä neljän pelaajan) välisiä kamppailuja, joissa toinen otteluparin pelaajista etenee seuraavaan vaiheeseen.

#### Ranking-pisteytys
Ranking-pisteiden laskentamenetelma tulee olemaan variaatio [ATP-järjestön käyttämästä menetelmästä](https://en.wikipedia.org/wiki/ATP_Rankings#Ranking_method). Järjestelmä tulee mahdollistamaan rinnakkaisten listojen ylläpidon (esim. erillinen lista eri sukupuolille, ikäluokille tai pelimuodoille [esim. kaksin- ja nelinpelit]). Ranking-pisteiden laskennan syötteenä toimivat turnausten tuloskaaviot, jotka pohjautuvat manuaalisesti laadittuihin turnauskaavioihin.

Ranking-pisteytetyt pelaajat kuuluvat ranking-listalle. Lista päivittyy reaaliaikaisesti, ja sillä on olemassa operaattorin ja yleisön näkymä.

## Arkkitehtuuri
Projekti toteutetaan MVC-mallin pohjalle. Model- ja Controller-toiminnallisuus toteutetaan kurssin vaatimusten mukaisesti käyttäen Flask- ja muita relevantteja Python-kirjastoja käyttäen.

Viewin toteuttamiseen ajatuksena on käyttää renderöityä Jinja2-HTML-templaatteja sekä Bootstrapin HTML/CSS/JS-kirjastoja. Mahdollisesti kokeilen myös implementoia joitakin frontin osa-alueita oppimismielessä ReactJS:llä aikaresurssien mahdollistamissa rajoissa.
