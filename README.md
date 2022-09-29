# GreenWheel Backend API

Projecte per a l'assignatura PES de la Facultat d'Informàtica de Barcelona (FIB) de la Universitat Politècnica de Catalunya (UPC).
<br/>**Quatrimestre:** Tardor curs 2022/2023.
<br/>**Temàtica:** MOBILITAT SOSTENIBLE: fomentar l'ús de vehicles elèctrics (punts de recàrrega,...) i bicing.
## Introducció
El nostre projecte consisteix en el desenvolupament d’una aplicació mòbil la qual està principalment enfocada per tota aquella gent que disposi d’un cotxe elèctric i/o vulgui disposar de bicicletes durant uns dies.
<br>L’aplicació constarà d’un mapa en el qual es podran veure els punts de càrrega elèctrics de tot Catalunya i tots aquells punts on hi hagi bicis disponibles per a ser llogades. La nostra principal innovació és que un usuari podrà posar a disposició d’altres usuaris tant punts de càrrega com bicicletes, d’aquesta manera li proporcionen una utilitat als seus carregadors i bicicletes quan els propis usuaris no en facin ús.

### Membres del grup

| Nom              | GitHub username | Taiga username | Responsabilitat |
|------------------|-----------------| --- | --- |
| **Isslam Benali**    | Isslam1         | IsslamBenali | Service |
| **Arnau Giménez**    | arnau147        | arnau147 | Sprint 1 |
| **Cristina Migó**    | crismigo        | crismigo | Sprint 2 |
| **Miguel Gutiérrez** | MikierXXV         | mikierxxv | Demo tècnica |
| **Daniel Oliveras**  | daniou         | daniou | Inception |
| **Andreu Orensanz**  | andyfratello         | andreuorensanz | Inception |
| **Àlex Ollé**        | aolle99         | aolle99 | Sprint 3 |

### Professor responsable
Jordi Piguillem Poch ( [jpiguillem@essi.upc.edu](mailto:jpiguillem@essi.upc.edu) )

### Enllaços
- [Enllaç al entorn de PRE (NO DISPONIBLE)]()
- [Enllaç al entorn de PRODUCCIÓ (NO DISPONIBLE)]()
- [Enllaç al projecte Taiga](https://tree.taiga.io/project/arnau147-pes-green-whee/)
- [Repositori GitHub](https://github.com/orgs/Green-Wheel/repositories)


## Requeriments per a poder començar a treballar
### Introducció
A continuació trobareu un tutorial guiat per tal d'instalar-vos el projecte en local i poder començar a treballar-hi. Aquest tutorial està pensat per a que sigui seguit en ordre, però si voleu podeu saltar-vos algun pas si ja teniu instal·lat alguna de les eines que es demanen.
<br>El tutorial està pensat per a windows. En qualsevol altre sistema operatiu, serà semblant, però no puc assegurar que funcioni.

### Instalar Python
1. Per a comprovar si el teniu instal·lat, proveu a escriure `python` al terminal de windows. En cas de que no el tingueu (i estigueu a windows 11) us portarà a la microsoft Store, on us dirà si voleu instalar python.
2. Allà, li doneu a _obtener_ i us instal·larà la ultima versió de python. Si esteu en una altra versió de windows, podeu descarregar-lo des de la web oficial de python: [https://www.python.org/downloads/](https://www.python.org/downloads/release/python-3107/).
3. Torneu a provar a utilitzar la comanda `python` al terminal i veureu com us surt la versió i unes fletxetes.
4. En un altre terminal, proveu a posar `pip` i us sortirà les diferents opcions. Si us surten aquestes coses, es que ho teniu ben instal·lat i podeu passar al següent pas.

### Instalar PyCharmProfessional
Si voleu podeu usar el Community, però ja que sou estudiants, jo de vosaltres aprofitaria per demanar llicencia i utilitzar la versió pro, que ofereix moltes més eines.
1. Demanar compte estudiant a [Jetbrains](https://www.jetbrains.com/shop/eform/students) (no cal si ja l'heu demanat abans)
2. Descarregar-se el Pycharm Professional
3. Un cop instalat, obriu-lo i us apareixerà una finestra com aquesta:
![Imagen Pantalla inicial PyCharm](https://i.imgur.com/Z2vlOHc.png)
4. Un cop en aquesta finestra, li donarem clic a Get from VCS
5. Ens sortirà una altra finestra, i li donarem a GitHub, on linkejarem amb el nostre compte que té el projecte compartit.
6. Un cop loguejats, ens sortirà una llista dels projectes que tenim, i allà seleccionarem el `Green-Wheel/Backend`.
7. A directory posarem el directori on volem que se'ns guardi i li donarem a clone.
8. Se'ns obrirà el projecte, on tot hauria d'estar configurat. si us diu que instaleu quelcom, feu-ho.

### Instalar llibreries necessaries de python
1. Us recomano crear-vos un [virtual environment](https://www.programaenpython.com/miscelanea/crear-entornos-virtuales-en-python/), aixi no se us fa malbé el python local.
2. Anar al fitxers settings.py i ja ens dirà si volem instalar les llibreries, allà, li donarem que si (les agafa del fitxer requirements.txt).
3. (Per si no funciona la 2) Si no ens ho diu, anar al terminal i posar `pip install -r requirements.txt` i ens instal·larà totes les llibreries necessàries.

### Executar projecte
1. Anar al terminal i posar `python manage.py runserver` i ens obrirà un servidor local.
2. Anar al navegador i posar [localhost:8000](http://localhost:8000/) i ens hauria de sortir la pàgina principal del projecte.

### Executar projecte des de PyCharm (Opcional)
1. Anar a Run -> Edit Configurations
2. A la barra esquerra, pulsarem el més i seleccionarem Django Server
3. Configurarem la configuració com a la imatge:
![Imagen Configuracion PyCharm](https://i.imgur.com/5iZ0eN4.png)
4. Al apartat python interpreter podeu posar el vostre virtual environment, si no, posar el de sistema.
5. Li doneu a ok i ja us hauria de funcionar. Es possible que us faci configurar Django, i simplement especifiqueu on estan els directoris i fitxers del projecte.

### Instalar Docker (per a la base de dades)
1. Descarregar-se docker des de [aquí](https://www.docker.com/products/docker-desktop).
2. Instal·lar-lo.
3. Un cop instal·lat, obrir el docker i comprovar que funciona.
4. Si no funciona, podeu provar a obrir el terminal i posar `docker run hello-world` i veureu si us surt un missatge de que tot ha anat bé.
5. Si us surt aquest missatge, ja podeu passar al següent pas.

### Desplegar la base de dades
1. Anar al terminal i posar `docker-compose up -d` i ens hauria de crear la base de dades (ja configurada).
2. Executar la comanda python `python manage.py migrate` per a crear les taules de la base de dades.
3. Executar la comanda python `python manage.py createsuperuser` per a crear un usuari administrador de la base de dades. Seguiu les instruccions del terminal

## Connectar Base de Dades a PyCharm (opcional)
PyCharm permet crear una connexio a la base de dades, la qual nomes serveix per a poder veure la base de dades des del programa. Això pot anar bé si voleu veure com va quedant la base de dades o el que necessiteu. És opcional, ja que la connexió amb Django ve donada per els arxius de configuració d'aquests i no per el IDE.
1. A la barra lateral dreta veureu un apartat anomenat Database. Allà, veureu que hi ha un simbol de suma -> Data source -> PostgreSQL
2. Configurarem els diferents inputs amb la configuració que trobarem al fitxer settings.py de l'aplicació.
3. Li doneu a apply i a ok, i ja ho tindreu configurat.

### Ja està! Ara us recomano que aneu al fitxer apunts.md i llegiu els apunts que hi ha per a començar a fer el projecte.

## Enllaços d'interès
- [Documentació Django](https://docs.djangoproject.com/en/4.0/)
- [Curs de Django a Youtube](https://www.youtube.com/playlist?list=PLU8oAlHdN5BmfvwxFO7HdPciOCmmYneAB)
- [Llibreria de rest](https://www.django-rest-framework.org/)
- [Exemple de com utilitzar REST API](https://blog.logrocket.com/django-rest-framework-create-api/#restful-structure-get-post-put-delete-methods)
- [Projecte ASW fet amb Django](https://github.com/crismigo/Hacker-News-HN22D)
- [Tutorial generar OpenApi amb swaggerUI utilitzant Django](https://hackernoon.com/openapi-30-schema-with-swagger-ui-for-django-restful-app-4w293zje)


<br>Fins aquí l'explicació de com instal·lar-se les coses. Si teniu qualsevol problema, dubte o necessitat, digueu-m'ho. També sentiu-vos lliures de completar aquesta petita guia.