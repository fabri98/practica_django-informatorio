from .utils import obtener_id_disponible, sacar_id_de_lista
from .models import Pregunta, ProgresoSesion, Respuesta
from django.shortcuts import redirect, render
import random


# Create your views here.

#view de registrar, logear. copiar documentación


#view index

#La view que muestra la pregunta
def pregunta_view(request, pregunta_id):
    if request.method == 'GET':
        preguntas = Pregunta.objects.all()

        respuestas = Respuesta.objects.all()

        #quitamos pregunta de las preguntas disponibles
        print(f"llamando a la funcion {pregunta_id}")
        sacar_id_de_lista(request.user.id, pregunta_id)
        print(f"llamé a la funcion {pregunta_id}")

        #id_random = random.randint(1, preguntas.count())
        id_random = pregunta_id

        pregunta = preguntas.get(id=id_random)

        respuestas_pregunta = respuestas.filter(pregunta=pregunta)

        return render(request, 'quiz/pregunta.html', {
            'pregunta': pregunta,
            'respuestas': respuestas_pregunta
        })

    if request.method == 'POST':
    # si es correcta => redireccionar a view pregunta_view
        id_respuesta = request.POST["respuesta"]

        respuesta = Respuesta.objects.get(id=id_respuesta)

        if respuesta.es_correcta:
            #obtener el nuevo id, random, que no está repetido
            id_pregunta_disponible = obtener_id_disponible(request.user.id)

            #llevar cuenta de puntos de 10 en 10
            sesion = ProgresoSesion.objects.get(usuario=request.user)
            sesion.puntaje += 10
            sesion.save()

            #redireccionar
            return redirect('pregunta_view', pregunta_id=id_pregunta_disponible)
        else:
        # si es incorrecta => redireccionar a view fin de partida
            sesion = ProgresoSesion.objects.get(usuario=request.user)
            return redirect('resultado_view', sesion_id=sesion.id)




def resultado_view(request, sesion_id):
    sesion = ProgresoSesion.objects.get(id=sesion_id)

    return render(request, 'quiz/resultado.html', {
        'puntaje': sesion.puntaje
    })


#   metodo get => mostrar pregunta
#   metodo post => elegir la proxima pregunta.
#       funcion auxiliar, logica para llevar la cuenta de preguntas usando el modelo progresosesion.

#view fin de partida y compartir resultados.


#view estadisticas