# Apunts

Per tal de realitzar el backend de la nostra aplicació, cal fer una REST API, la qual implementarem mitjançant [Django Rest Framework](https://www.django-rest-framework.org/), una llibreria de django (third party) que ens permet crear una rest api fàcilment, i el qual ja té un mòdul per a generar l'esquema OpenAPI.<br>
> Per si no sabeu que és OpenAPI, simplement es un fitxer on s'explica tots els endpoints de la nostra api, de manera que, si algú vol saber a que pot accedir, només cal que miri aquest fitxer. [Exemple](https://atenea.upc.edu/pluginfile.php/4532654/mod_resource/content/3/wot-api.yaml)

Jo ja us ho he deixat tot configurat, per tal que només us calgui implementar. També els CORS (uns headers que gestionen l'accés a l'API. Ara mateix per a desenvolupar estan desactivats per tal que poguem treballar més fàcilment).
<br><br>
Per tal de fer la REST API, us recomano seguir el següent [enllaç](https://blog.logrocket.com/django-rest-framework-create-api/#restful-structure-get-post-put-delete-methods), el qual està molt bé i us pot servir per aprendre a utilitzar-ho. També us podeu guiar pel que he fet jo, el qual està basat en l'enllaç.
## Models i Migrations
### Models
Els models, son representacions de les taules de la base de dades, i els camps de cada model, son representacions de les columnes de la taula.<br>
Per tal de crear els models, cal implementar el fitxer `models.py`, que estan dins de cada app.<br>
Un exemple de model podria ser el següent:
```python
from django.db import models
class Submission(models.Model):
    title = models.CharField(max_length=100, blank=False)
    type = models.ForeignKey(SubmissionType, on_delete=models.RESTRICT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=1)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='comment.Comment', related_name="comments", through_fields=('submission', 'user'))
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='vote.Vote', related_name="votes", through_fields=('submission', 'user'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
```
Si us hi fixeu, de normal no assignem PK, ja que ho farà automaticament i posara id. En cas que el volguem modificar, ho podem fer.<br>
Tota la documentació de models la podeu trobar [aquí](https://docs.djangoproject.com/en/4.1/topics/db/models/).<br>

### Migrations
Les migrations, son els fitxers que s'encarreguen de crear les taules a la base de dades, i per tant, cal crear-les sempre que es modifiqui algun model.
Una vegada tingueu el model fet o almenys allò que volieu, per a generar la migration (un script que es llença contra la BBDD), cal executar:
```bash
python manage.py makemigrations
```
Això només generarà el fitxer, però no crearà les taules (no s'ha executat). Per a fer-ho, cal que executeu:
```bash
python manage.py migrate
```
Aquesta comanda l'haureu de fer cada cop que algú faci una migration nova, per tal de que tingui efecte sobre el nostre sistema.
### Crear migration de dades inicials per una taula
A vegades necessitarem omplir una taula amb varis valors només crear-la (sobretot quan son taules que provenen de enums).
Per a fer-ho, executarem:
```bash
python manage.py makemigrations --empty appname
```
A appname posarem el nom de la carpeta de l'app que volem crear la migration. Això ens crearà un fitxer de migration buit, que haurà de tenir el següent contingut:
```python
from django.db import migrations

def load_initial_data(apps, schema_editor):
    language_model = apps.get_model('users', 'Languages')
    language_model.objects.create (
        name = "Catala", shortname = "ca"
        )
    language_model.objects.create(
        name="Castellano", shortname="es"
    )
    language_model.objects.create(
        name="English", shortname="en"
    )

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'), # Migration anterior
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
```
### Automatitzar migrations
Per tal de no haver de fer manualment les migrations, cal que configurem el fitxer `settings.py` de la següent manera:
1. Anirem a les configuracions d'execució i li donarem a editar configuració (Està a dalt a la dreta, abans de les opcions de git).
2. Allà, afegirem una nova configuració de tipus python. Li donarem el nom que vulguem, per exemple, `Migrate on run`. A la opció script path, seleccionarem el fitxer de la carpeta root del projecte anomenat pre_run.py.
3. Apliquem els canvis.
4. Anem a la opció de configuració de django i la seleccionem. A sota de tot, ens surt per afegir que s'executi algo abans de l'execució. Pulsarem el + i seleccionarem run another configuration.
5. Seleccioanrem la que hem creat fa uns instants.
6. Apliquem els canvis.

## Estructura RESTful que seguirem
L'estructura restful simplement ens serveix per quedar entre nosaltres com nombrem les coses, per tal que estigui estandaritzat. Si no m'equivoco la openAPI també diu quelcom, però mirant-ho rapid no ho he trobat, si algú ho veu, que ho apunti per aquí.
### Exemple de requests per endpoint:
#### publicacions/
- **GET :** Retorna totes les instàncies que hi hagi de publicacions i codi `HTTP_200_OK`
- **POST :** Crea una nova instància de publicacions i:
  - En cas que s'hagi pogut crear, la retorna juntament amb un codi `HTTP_200_OK`. 
  - En cas que no es pugui crear, es retorna `HTTP_400_BAD_REQUEST` i el misstage d'error.
  - En cas que aquella instància ja existeixi (trenca restriccio unique), es retorna `HTTP_409_CONFLICT` i el misstage d'error.
#### publicacions/\<int:publicacio_id>
- **GET :** Retorna la instància de publicacio que conté la publicacio_id i codi `HTTP_200_OK`. En cas que no existeixi es retorna `HTTP_400_BAD_REQUEST`.
- **PUT :** Actualitza la instància amb la id passada i la retorna, juntament amb codi `HTTP_200_OK`. En cas que no existeixi es retorna `HTTP_400_BAD_REQUEST`. 
- **DELETE :** Elimina la instància amb la id passada i retorna el codi `HTTP_204_NO_CONTENT`. En cas que no existeixi es retorna `error 400`.

> Un endpoint és una url concreta, per exemple *publicacions/*, la qual pot tenir més d'un tipus de request assignat. També hi haurà endpoints que no en tenen cap, i al intentar d'accedir, el matiex framework posa la pàgina d'error 404.

En cas de voler agrupar, podem utilitzar:
#### publicacions/user/\<int:user_id>
- **GET :** Retorna totes les instàncies que hi hagi de publicacions fetes per l'usuari passat per paràmetre
- **DELETE :** Elimina totes les instàncies que tenen al usuari assignat. En cas que no existeixi es retorna `error 400`.

## Tests
Per tal de fer tests, cal implementar el fitxer `tests.py` dins de cada app. Per tal de fer un test, cal crear una classe que hereti de `TestCase` i que tingui el prefix `test_` al nom de la funció. Per exemple:
```python
from django.test import TestCase
class TestSubmission(TestCase):
    def test_get_submissions(self):
        response = self.client.get('/submissions/')
        self.assertEqual(response.status_code, 200)
```
Per tal de fer un test, cal executar el següent codi:
```bash
python manage.py test
```
Tota la documentació relacionada la trobareu a [aquí](https://docs.djangoproject.com/en/4.1/topics/testing/overview/).

## Punts a fer per tal de crear la REST API
Per tal de crear la REST API, haurieu de seguir els següents passos:
1. Crear un fitxer dins el directori anomenat serializers.py. Fer el model Serializer del model del qual heu d'extreure la informació.
2. A views.py, crear una classe per cada endpoint (cada direcció), la qual heredi de APIView.
3. Crear un metode d'aquesta classe per cada request que volem que respongui l'endpoint. Dins d'aquest, fer les operacions que calguin i, un cop acabat, fer la Response amb la data necessària i l'status.
4. Afegir els endpoints al fitxer urls.py tot indicant la APIView que volem relacionar-hi.
5. Comprovar que l'endpoint que hem posat funciona accedint des del navegador.
6. Fer test en el fitxer test.py per tal de comprovar que funciona correctament.

## Exemple de com crear un endpoint
```python
# serializers.py
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "title", "type", "author", "url", "text", "comments", "votes", "created_at"]
# views.py
class NewsApiView(APIView, PaginationHandlerMixin):
    def get(self, request):
        news = Submission.objects.annotate(num_submissions=Count('votes')).order_by('-num_submissions')

        page = self.paginate_queryset(news)
        if page is not None:
            serializer = self.get_paginated_response(SubmissionReadSerializer(page, many=True).data)
        else:
            serializer = SubmissionReadSerializer(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        url = request.data.get('url')
        text = request.data.get('text')
        user = request.user

        if url != "":
            url_exists = Submission.objects.filter(url=url)
            if url_exists.count() > 0:
                return Response(
                    {"res": "Url already exists", "id": url_exists[0].id},
                    status=status.HTTP_409_CONFLICT
                )
            submision_type = SubmissionType.objects.get(name="url")
            data = {
                'title': title,
                'type': submision_type.id,
                'author': user.id,
                'url': url,
                'points': 1,
            }
            serializer = SubmissionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"res": "Los parametros pasados no son correctos"}, status=status.HTTP_400_BAD_REQUEST)

class NewsDetailApiView(APIView):
    def get_object(self, submission_id):
        try:
            return Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return None

    def get(self, request, news_id):
        submission_instance = self.get_object(news_id)
        if not submission_instance:
            return Response(
                {"res": "Object with news id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubmissionDetailedSerializer(submission_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, news_id):
        submission_instance = self.get_object(news_id)
        if not submission_instance:
            return Response(
                {"res": "Object with news id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title')
        }
        serializer = SubmissionSerializer(instance=submission_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news_id):
        submission_instance = self.get_object(news_id)
        if not submission_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        submission_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )
# urls.py
urlpatterns = [
    path('news/', NewsApiView.as_view(), name='news'),
    path('news/<int:news_id>/', NewsDetailApiView.as_view(), name='news_detail'),
]
```
## Convencions a l'hora d'escriure codi
### Variables
- **Noms de variables**: sempre en minúscules i separades per guions baixos. `Exemple: comptador_de_paraules`
- Cal que siguin descriptives
- Si son constants, cal que siguin en majúscules i separades per guions baixos. `Exemple: MAXIM_DE_PARAULES`
- Si son variables que contenen un booleà, cal que siguin en minúscules i que comencin per is o has. `Exemple: is_valid`
- Si son variables que contenen un array, cal que siguin en minúscules i que acabin en s. `Exemple: paraules`
- Si son variables que contenen un objecte, cal que siguin en minúscules i que acabin en o. `Exemple: paraula`
- Els noms de les variables han de ser en anglès, utilitzant un llenguatge entenedor i un vocublari senzill.
### Funcions / mètodes
- **Noms de funcions**: Menys la primera paraula, les altres començen en majúscules i la resta en minúscules, sense res que les separi. `Exemple: getCarByUserId(param1, param2)`
- El nom no pot ser massa llarg, ha de ser descriptiu i entenedor.
- El nom ha de ser en anglès, utilitzant un llenguatge entenedor i un vocublari senzill.
- Els paràmetres han de ser descriptius i entenedors.
- **Comentaris**: Cal que cada funció tingui un comentari que expliqui el que fa i els paràmetres que rep, seguint el format de comentaris de javadoc. Estan escrits en català.
Exemple: 
  ``` python
      /**
       * Retorna un cotxe a partir del seu id
       * @param id
       * @return Car
       */
  ```
- **Obrir i tancar claus**: sempre s'ha d'obrir en la mateixa línia i tancar-la en una línia nova.

### Classes
- **Noms de classes**: Totes les paraules començen en majúscules, sense res que les separi. `Exemple: UserCar`
- El nom no pot ser massa llarg, ha de ser descriptiu i entenedor.
- El nom ha de ser en anglès, utilitzant un llenguatge entenedor i un vocublari senzill.
- **Comentaris**: Cal que cada classe tingui un comentari que expliqui el que fa, seguint el format de comentaris de javadoc. Estan escrits en català.
- ** Ordre dels mètodes** Els mètodes de l'api REST s'ordenaran de la següent manera:
  1. get
  2. post
  3. put
  4. delete
 
Qualsevol altre element que no s'hagi mencionat, s'escriurà seguint el conveni de [PEP8](https://www.python.org/dev/peps/pep-0008/)


