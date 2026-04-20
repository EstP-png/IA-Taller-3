"""
red_puerto_sombras.py — La Red del Puerto de las Sombras

En el Puerto Industrial se encontró mercancía ilegal oculta en contenedores declarados como carga vacía.
El Capitán Herrera tiene registro digital de salida del puerto verificado durante el fin de semana del delito.x
El Inspector Nova tiene documentación oficial de inspecciones realizadas fuera del puerto ese fin de semana.x
El Oficial Duarte firma todos los manifiestos de carga del puerto; sus manifiestos son fraudulentos.x
El Oficial Duarte no tiene coartada verificada.x
El Marinero Pinto tiene acceso irrestricto a la bodega de contenedores; fue visto introduciendo mercancía ilegal.x
El Marinero Pinto no tiene coartada verificada.x
El Oficial Duarte y el Marinero Pinto pertenecen al mismo cartel portuario.x
Un informante reportó al Oficial Duarte y al Marinero Pinto por nombre.x
El Capitán Herrera acusa al Oficial Duarte.x
El Oficial Duarte declara que el Marinero Pinto no estuvo en el puerto ese fin de semana.x
El Marinero Pinto declara que el Oficial Duarte firmó los documentos por error administrativo.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene registro oficial que lo ubica fuera del puerto durante el delito está descartado.x
Quien firma manifiestos de carga fraudulentos comete fraude documental.x
Quien tiene acceso a la bodega y fue visto introduciendo mercancía ilegal introduce contrabando.x
Quien comete fraude documental sin coartada es culpable.x
Quien introduce contrabando sin coartada es culpable.x
Dos personas comparten red si pertenecen al mismo cartel.x
Si dos culpables comparten red, su actividad constituye una operación conjunta.x
El testimonio de una persona descartada contra alguien es confiable.x
Una red está activa si al menos uno de sus miembros es culpable.x
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    capitan_herrera   = Term("capitan_herrera")
    oficial_duarte    = Term("oficial_duarte")
    marinero_pinto    = Term("marinero_pinto")
    inspector_nova    = Term("inspector_nova")
    cartel_portuario  = Term("cartel_portuario")

    # === YOUR CODE HERE ===
    kb.add_fact(Predicate("coartada_digital", (capitan_herrera,)))
    kb.add_fact(Predicate("coartada_oficial", (inspector_nova,)))
    kb.add_fact(Predicate("sin_coartada", (oficial_duarte,)))
    kb.add_fact(Predicate("firma_manifiestos_fraudulentos", (oficial_duarte,)))
    kb.add_fact(Predicate("acceso_irrestringido_bodega", (marinero_pinto,)))
    kb.add_fact(Predicate("introduce_merc_ilegal", (marinero_pinto,)))
    kb.add_fact(Predicate("sin_coartada", (marinero_pinto,)))
    kb.add_fact(Predicate("pertenece", (cartel_portuario, marinero_pinto,)))
    kb.add_fact(Predicate("pertenece", (cartel_portuario, oficial_duarte,)))
    kb.add_fact(Predicate("reportado_por_informante", (oficial_duarte,)))
    kb.add_fact(Predicate("reportado_por_informante", (marinero_pinto,)))
    kb.add_fact(Predicate("acusa", (capitan_herrera,oficial_duarte)))
    kb.add_fact(Predicate("da_coartada", (oficial_duarte, marinero_pinto)))
    kb.add_fact(Predicate("defiende", (marinero_pinto, oficial_duarte)))


    kb.add_rule(Rule(
        head=Predicate("descartado", (Term("$X"),)),
        body=(Predicate("coartada_oficial", (Term("$X"),)),),
    ))
    
    kb.add_rule(Rule(
        head=Predicate("fraude_documental", (Term("$X"),)),
        body=(Predicate("firma_manifiestos_fraudulentos", (Term("$X"),)),),
    ))
    kb.add_rule(Rule(
        head=Predicate("introduce_contrabando", (Term("$Contrabandista"),)),
        body=(Predicate("acceso_irrestringido_bodega", (Term("$Contrabandista"),)),
              Predicate("introduce_merc_ilegal", (Term("$Contrabandista"),)),
              ),
    ))
    kb.add_rule(Rule(
        head=Predicate("culpable", (Term("$Sospechoso"),)),
        body=(Predicate("fraude_documental", (Term("$Sospechoso"),)),
              Predicate("sin_coartada", (Term("$Sospechoso"),)),
              ),
    ))
    kb.add_rule(Rule(
        head=Predicate("culpable", (Term("$Sospechoso"),)),
        body=(Predicate("introduce_contrabando", (Term("$Sospechoso"),)),
              Predicate("sin_coartada", (Term("$Sospechoso"),)),
              ),
    ))
    kb.add_rule(Rule(
        head=Predicate("comparten_red", (Term("$X"),Term("$Y"),)),
        body=(Predicate("pertenece", (Term("$Cartel"),Term("$X"),)),
              Predicate("pertenece", (Term("$Cartel"),Term("$Y"),)),
              ),
    ))
    kb.add_rule(Rule(
        head=Predicate("operacion_conjunta", (Term("$X"),Term("$X"),)),
        body=(Predicate("comparten_red", (Term("$X"),Term("$X"),)),),
    ))
    kb.add_rule(Rule(
        head=Predicate("testimonio_confiable", (Term("$Acusador"),Term("$Victima"),)),
        body=(Predicate("descartado", (Term("$Acusador"),)),
              Predicate("acusa", (Term("$Acusador"),Term("$Victima"),)),
            ),
    ))
    kb.add_rule(Rule(
        head=Predicate("red_activa", (Term("$Red"),)),
        body=(Predicate("culpable", (Term("$Miembro"),)),
              Predicate("pertenece", (Term("$Red"),Term("$Miembro"),)),
            ),
    ))  

    # === END YOUR CODE ===

    return kb


CASE = CrimeCase(
    id="red_puerto_sombras",
    title="La Red del Puerto de las Sombras",
    suspects=("capitan_herrera", "oficial_duarte", "marinero_pinto", "inspector_nova"),
    narrative=__doc__,
    description=(
        "Contrabando en el Puerto Industrial: manifiestos fraudulentos y mercancía ilegal. "
        "Dos culpables con roles distintos operan como red. Identifica a ambos, verifica "
        "si su operación es conjunta y si hay redes activas."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Oficial Duarte cometió fraude documental?",
            goal=Predicate("fraude_documental", (Term("oficial_duarte"),)),
        ),
        QuerySpec(
            description="¿Marinero Pinto es culpable?",
            goal=Predicate("culpable", (Term("marinero_pinto"),)),
        ),
        QuerySpec(
            description="¿Hay operación conjunta entre Duarte y Pinto?",
            goal=Predicate("operacion_conjunta", (Term("oficial_duarte"), Term("marinero_pinto"))),
        ),
        QuerySpec(
            description="¿El testimonio del Capitán Herrera contra Duarte es confiable?",
            goal=Predicate("testimonio_confiable", (Term("capitan_herrera"), Term("oficial_duarte"))),
        ),
        QuerySpec(
            description="¿Existe alguna red activa?",
            goal=ExistsGoal("$R", Predicate("red_activa", (Term("$R"),))),
        ),
        QuerySpec(
            description="¿Todo reportado por informante es culpable?",
            goal=ForallGoal(
                "$X",
                Predicate("reportado_informante", (Term("$X"),)),
                Predicate("culpable", (Term("$X"),)),
            ),
        ),
    ),
)
