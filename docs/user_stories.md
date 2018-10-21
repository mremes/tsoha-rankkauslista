# User storyt

User storyt on kategorisoitu pääasiallisesti entiteettityyppien mukaan. Projektin entiteetit löydät [READMEsta](README.md#entiteetit).

## Käyttäjäryhmät
* Ylläpitäjä
    - toimii lajiliittona: pystyy tekemään kaikkea järjestelmässä
    - erityisesti, luo ranking-listat ja lisää ranking-pisteet turnauksiin
* Pelaaja-agentti
    - pystyy lisäämään pelaajia järjestelmään
    - pystyy lisäämään lisäämiään pelaajia ranking-listoilla, muokkaamaan ja poistamaan heidän tietojaan
* Turnausjärjestäjä:
    - luo turnaukset
    - lisää turnaustulokset
    - lopettaa turnaukset

## Lajiliitto (ylläpitäjä)
Lajiliittona, haluan luoda ranking-listan, jolle rekisteröidyn pelaajan voi lisätä pelaaja-agentin toimesta.
```
INSERT INTO Player (name, gender, dateofbirth, placeofbirth, registered_dt, created_by) VALUES ("Pekka Pelaaja", "mies", "17.07.1994", "Helsinki", CURRENT_TIMESTAMP, 1);
```
Lajiliittona, haluan tarjota turnauksen järjestäjälle listan käytettävissä olevista pelaajista turnauskaavion luomisen tueksi.
```
SELECT * 
FROM Player 
WHERE dateofbirth BETWEEN 16 and 25
AND gender = "nainen";
```

Lajiliittona, haluan tarkastella turnauksen järjestäjän syöttämiä turnaustuloksia ja antaa turnauksen sijoituksille ranking-pisteitä.

Lajiliittona, haluan päättää turnauksen.

```
UPDATE Tournament 
SET is_completed = 1
WHERE id = 1;
```

## Pelaaja
Pelaaja-agenttina, haluan lisätä pelaajan järjestelmään.
```
INSERT INTO Player (name, gender, dateofbirth, placeofbirth, registered_dt, created_by) VALUES ("Pekka Pelaaja", "mies", "17.07.1994", "Helsinki", CURRENT_TIMESTAMP, 1);
```

Pelaajana, haluan tarkastella profiilitietojani. Ranking-listoilta haluan nähdä reaaliaikaisen ranking-pistetilanteeni. Voin kuulua moneen ranking-listaan.
```
SELECT * FROM Player WHERE id = 1;
```

```
SELECT a.*
FROM RankingRecord a
INNER JOIN 
(
SELECT ranking_id, max(timestamp) maxts
FROM RankingRecord
GROUP BY ranking_id
) b
ON a.ranking_id = b.ranking_id AND a.timestamp = a.maxtws
INNER JOIN
(
SELECT id
FROM Ranking 
WHERE player_id = 1
) c
ON a.ranking_id = c.id;
```

Pelaaja-agenttina, voin poistaa pelaajan. 
```
DELETE FROM Player WHERE id = 1;
DELETE FROM RankingRecord WHERE ranking_id in (SELECT id FROM Ranking WHERE player_id = 1);
DELETE FROM Ranking WHERE player_id = 1;
```

## Turnaus
Turnausjärjestäjänä, haluan syöttää turnaustiedot järjestelmään. Turnaustiedot sisältävät tietoja kuten:

* järjestämisaika,
* osallistuvat pelaajat sekä
* jaettavat palkinnot sijoituksen mukaan.

Haluan, että voin asetella pelaajat turnauskaavioon ranking-listalla olevista pelaajista.

Turnausjärjestäjänä, haluan syöttää sijoitustiedot ja julistaa turnauksen lopetetuksi. Turnauksen loputtua, ranking-tilanteen on päivityttävä reaaliaikaisesti, jos lajiliitto on määritellyt pistejakauman.

Turnausjärjestäjänä, voin poistaa turnauksen.

## Julkiset user storiet
Turnauksesta kiinnostuneena henkilönä, haluan nähdä turnauksen sijoitukset sekä sijoituksista jaetut mahdolliset ranking-pisteet.

Ranking-listan selaajana, haluan nähdä vähintään top 10 ranking-listalla olevaa pelaajaa sekä heidän pistemääränsä pistejärjestyksessä.

```
SELECT name, score
FROM
(
SELECT ranking_id, a.score score
FROM RankingRecord a
INNER JOIN
(
SELECT ranking_id, MAX(timestamp) maxts
FROM RankingRecord
GROUP BY ranking_id
) b
ON a.ranking_id = b.ranking_id AND a.timestamp = b.maxts
) a
LEFT JOIN
(
SELECT a.id ranking_id, b.name name
FROM Ranking
LEFT JOIN
(
SELECT name, id player_id
FROM Player
) b
ON a.player_id = b.player_id
) b
ON a.ranking_id = b.ranking_id
ORDER BY score DESC
```

Pelaajasta kiinnostuneena, haluan avata pelaajan profiilisivun, josta näen perustiedot sekä mille ranking-listoille hän kuuluu.

## Indeksit
```
CREATE INDEX PlayerMain
ON Player (registered_at, name);

CREATE INDEX RankingRecordByTime
ON RankingRecord (timestamp);
```
