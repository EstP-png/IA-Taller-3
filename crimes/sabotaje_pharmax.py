"""
sabotaje_pharmax.py — El Sabotaje en Laboratorio Pharmax

Los cultivos del Proyecto Ámbar fueron destruidos en el Laboratorio Pharmax durante el fin de semana.
La Dra. Santos asistió a un congreso internacional ese fin de semana con documentación oficial de viaje al exterior.
El Director Vega participó en una conferencia en Bruselas con registro verificado de asistencia.
El Técnico Ríos fue despedido recientemente por filtrar información confidencial; no tiene coartada para el fin de semana.
El Asistente Mora fue amenazado con despido; tampoco tiene coartada para el fin de semana.
El registro de acceso muestra que el Técnico Ríos entró a la sala de cultivos el sábado.
El mismo registro muestra que el Asistente Mora también entró a la sala de cultivos el sábado.
Registros bancarios muestran que el Técnico Ríos recibió pagos de Syntek Corp. durante los últimos meses.
Syntek Corp. es la empresa rival que competía por la misma patente farmacéutica.
El Asistente Mora acusa directamente al Técnico Ríos.
El Técnico Ríos declara que el Asistente Mora estuvo con él durante todo el fin de semana.

Como detective, he llegado a las siguientes conclusiones:
Documentación oficial de ausencia del país constituye coartada verificada.
Un registro oficial de conferencia también constituye coartada verificada.
Quien tiene coartada verificada queda descartado como autor del sabotaje.
Quien recibió pagos de una empresa que se beneficia del sabotaje tiene conflicto de intereses con ella.
El conflicto de intereses con la empresa beneficiada constituye motivo económico para el sabotaje.
Quien tuvo acceso registrado al lugar saboteado estuvo en el momento del crimen.
Quien sin coartada tiene motivo económico y estuvo en el lugar del sabotaje es culpable.
La denuncia de alguien que también estuvo en el lugar del sabotaje es una denuncia informada.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    tec_rios       = Term("tec_rios")
    asistente_mora = Term("asistente_mora")
    dra_santos     = Term("dra_santos")
    director_vega  = Term("director_vega")
    syntek_corp    = Term("syntek_corp")
    sala_cultivos  = Term("sala_cultivos")

    # === YOUR CODE HERE ===

    # --- Hechos ---
    # Dra. Santos tiene documentación oficial de viaje al exterior (coartada verificada)
    kb.add_fact(Predicate("documentacion_oficial_ausencia", (dra_santos,)))

    # Director Vega tiene registro verificado de conferencia en Bruselas (coartada verificada)
    kb.add_fact(Predicate("registro_oficial_conferencia", (director_vega,)))

    # Técnico Ríos fue despedido recientemente por filtrar información (sin coartada)
    kb.add_fact(Predicate("sin_coartada", (tec_rios,)))

    # Asistente Mora fue amenazado con despido (sin coartada)
    kb.add_fact(Predicate("sin_coartada", (asistente_mora,)))

    # Registro de acceso: Técnico Ríos entró a la sala de cultivos el sábado
    kb.add_fact(Predicate("acceso_registrado", (tec_rios, sala_cultivos)))

    # Registro de acceso: Asistente Mora entró a la sala de cultivos el sábado
    kb.add_fact(Predicate("acceso_registrado", (asistente_mora, sala_cultivos)))

    # Técnico Ríos recibió pagos de Syntek Corp.
    kb.add_fact(Predicate("recibio_pagos_de", (tec_rios, syntek_corp)))

    # Syntek Corp. es empresa rival beneficiada por el sabotaje
    kb.add_fact(Predicate("empresa_beneficiada", (syntek_corp,)))

    # Asistente Mora acusa directamente al Técnico Ríos
    kb.add_fact(Predicate("acusa", (asistente_mora, tec_rios)))

    # --- Reglas ---
    # Documentación oficial de ausencia del país constituye coartada verificada
    kb.add_rule(Rule(
        head=Predicate("coartada_verificada", (Term("$X"),)),
        body=(Predicate("documentacion_oficial_ausencia", (Term("$X"),)),),
    ))

    # Registro oficial de conferencia también constituye coartada verificada
    kb.add_rule(Rule(
        head=Predicate("coartada_verificada", (Term("$X"),)),
        body=(Predicate("registro_oficial_conferencia", (Term("$X"),)),),
    ))

    # Quien tiene coartada verificada queda descartado como autor del sabotaje
    kb.add_rule(Rule(
        head=Predicate("descartado", (Term("$X"),)),
        body=(Predicate("coartada_verificada", (Term("$X"),)),),
    ))

    # Quien recibió pagos de una empresa beneficiada tiene conflicto de intereses con ella
    kb.add_rule(Rule(
        head=Predicate("conflicto_intereses", (Term("$X"), Term("$E"))),
        body=(
            Predicate("recibio_pagos_de", (Term("$X"), Term("$E"))),
            Predicate("empresa_beneficiada", (Term("$E"),)),
        ),
    ))

    # El conflicto de intereses con la empresa beneficiada constituye motivo económico
    kb.add_rule(Rule(
        head=Predicate("motivo_economico", (Term("$X"),)),
        body=(Predicate("conflicto_intereses", (Term("$X"), Term("$E"))),),
    ))

    # Quien tuvo acceso registrado al lugar saboteado estuvo en el momento del crimen
    kb.add_rule(Rule(
        head=Predicate("acceso_en_momento", (Term("$X"),)),
        body=(Predicate("acceso_registrado", (Term("$X"), Term("$Lugar"))),),
    ))

    # Quien sin coartada tiene motivo económico y estuvo en el lugar del sabotaje es culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (Term("$X"),)),
        body=(
            Predicate("sin_coartada", (Term("$X"),)),
            Predicate("motivo_economico", (Term("$X"),)),
            Predicate("acceso_en_momento", (Term("$X"),)),
        ),
    ))

    # La denuncia de alguien que también estuvo en el lugar del sabotaje es una denuncia informada
    kb.add_rule(Rule(
        head=Predicate("denuncia_informada", (Term("$X"), Term("$Y"))),
        body=(
            Predicate("acceso_en_momento", (Term("$X"),)),
            Predicate("acusa", (Term("$X"), Term("$Y"))),
        ),
    ))

    # === END YOUR CODE ===

    return kb


CASE = CrimeCase(
    id="sabotaje_pharmax",
    title="El Sabotaje en Laboratorio Pharmax",
    suspects=("tec_rios", "asistente_mora", "dra_santos", "director_vega"),
    narrative=__doc__,
    description=(
        "Cuatro años de investigación farmacéutica destruida en una noche. "
        "Un caso donde motivo económico, ausencia de coartada y registro de acceso "
        "convergen para identificar al saboteador."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿La Dra. Santos está descartada?",
            goal=Predicate("descartado", (Term("dra_santos"),)),
        ),
        QuerySpec(
            description="¿Técnico Ríos tiene conflicto de intereses con Syntek Corp.?",
            goal=Predicate("conflicto_intereses", (Term("tec_rios"), Term("syntek_corp"))),
        ),
        QuerySpec(
            description="¿Técnico Ríos es culpable?",
            goal=Predicate("culpable", (Term("tec_rios"),)),
        ),
        QuerySpec(
            description="¿La denuncia de Asistente Mora es una denuncia informada?",
            goal=Predicate("denuncia_informada", (Term("asistente_mora"), Term("tec_rios"))),
        ),
        QuerySpec(
            description="¿Todo culpable tuvo acceso en el momento del sabotaje?",
            goal=ForallGoal(
                "$X",
                Predicate("culpable", (Term("$X"),)),
                Predicate("acceso_en_momento", (Term("$X"),)),
            ),
        ),
    ),
)
