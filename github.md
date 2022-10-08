# Com gestionar el github

A continuació un resum de com gestionar el github i fer les coses per tal de que tots anem a una.

## Creació d'una issue

Per cada història d'usuari que hagueu de fer, cal crear una issue a github. Si teniu front i back, haureu de fer-ho als
dos repositoris. Si només necessiteu un dels dos, doncs només ho fareu en el que necessiteu.

1. Anar a la pàgina principal del repositori a la que voleu crear la issue.
2. Anar a la pestanya `Issues`.
3. Clicar a `New issue`.
4. Afegir el títol de la issue. Cal que estigui en el seguent format: #<num-HU>-<nom-historia>. Per
   exemple: `#1-Seleccionar idioma`.
5. Afegir la descripció de la issue. La gràcia seria que posessiu la descripció del taiga i després en format de llista
   amb checkboxes les tasques que hi te assignades.
6. On posa Assigness, us afegiu a vosaltres pulsant a assign yourself.
7. En labels, afegiu la label `feature`.
8. En milestone, selecciones `Sprint 1` (o el que correspongui).
9. Clicar a `Submit new issue`.
   ![](https://i.imgur.com/Hpz5T6o.png)

## Gestió de la issue

- Si hi ha qualsevol canvi, estaria bé que ho deixessiu com a comentari de la issue, per a que quedi escrit en algun
  lloc, aixi com si hi ha qualsevol problema, no es pot fer o quelcom.
- La issue es tacarà automàticament al fer merge de la branca. Per tant, no cal que la tancaríeu.
- Si la issue no es pot fer o quelcom, cal que la tanqueu a mà pulsant close issue.
- Si la issue es fa en dos o més commits, cal que la deixeu oberta fins que es faci tot.

## Creació d'una branca

Per cada issue que hagueu de fer, cal crear una branca dedicada exclusivament a aquesta issue. Per a crear la branca,
farem el següent:

1. Anirem a la issue que acabem de crear.
2. A la barra dreta, al apartat development, pulsarem a create a branch.
3. Al nom de la branca, posarem si es tracta d'una issue tipus feature o una tipus bug i despres el titol de la issue
   sense #. Per exemple: `feature- 37-seleccionar-idioma`.
4. No tocarem res i li donarem a `Create branch`.
   ![](https://i.imgur.com/hxjCPWu.png)

## Utilitzar branca al IDE

Per utilitzar la branca al IDE, farem el següent:

1. Anirem a la barra d'eines inferior i pulsarem l'apartat `Git`.
2. Anirem a la pestanya `Log`.
3. Pulsarem la fletxa amb el borde blau de la barra esquerra. Això ens actualitzarà les branques existents.
4. Pulsarem click dret sobre la branca que volem utilitzar i li donarem checkout.
5. Es molt important que no tinguem canvis en la branca en que estavem, sino ens dirà de fer rebase o quelcom. Si teniu
   canvis, pujeu-los a la branca o anuleu-los.
6. Estareu a la vostra branca i ja podeu començar a fer els canvis.
7. Sempre us podeu anar movent de branca, però sempre pujeu els canvis a la branca que esteu utilitzant.
8. Si necessiteu qualsevol cosa d'una altra branca, podeu fer click dret sobre la branca que voleu i li donar
   a `Merge into current`.

## Ajuntar amb la branca dev (la branca principal)

Per a fer merge amb la branca dev, farem el següent:

1. Anirem a github i anirem a la branca que volem ajuntar.
2. Mínim cal que tingui un commit, sino no te sentit fer merge.
3. Pulsarem a `Compare & pull request`.
   ![](https://i.imgur.com/D0LmZmz.png)
4. Pulsarem a create pull request.
5. A la barra dreta configurarem el assigness, labels i milestone.
6. Quan estiguem segurs de que tot esta bé, haguem debugat el codi, fet els tests, etc, li donarem
   a `Merge pull request`.
7. Si tot esta bé, li donarem a `Confirm merge`.