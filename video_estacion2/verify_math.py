"""Verificación matemática del caso de estudio con sympy.
h(x) = 1/(x-2) en x=2. Corre esto ANTES de confiar en los numeros del video.
"""
import sympy as sp

x = sp.symbols('x', real=True)
h = 1 / (x - 2)

print("h(x) =", h)

# 1) Valor de la función en x=2
print("\n--- Condición 1: h(2) ---")
try:
    val = h.subs(x, 2)
    print("h(2) =", val)
except Exception as e:
    print("h(2) no evaluable:", e)

# ¿Está x=2 en el dominio?
dominio = sp.calculus.util.continuous_domain(h, x, sp.S.Reals)
print("Dominio de h:", dominio)
print("¿2 pertenece al dominio?", sp.S(2) in dominio)

# 2) Límites laterales
print("\n--- Condición 2: límites laterales ---")
lim_izq = sp.limit(h, x, 2, dir='-')
lim_der = sp.limit(h, x, 2, dir='+')
print("lim x->2- h(x) =", lim_izq)
print("lim x->2+ h(x) =", lim_der)

lim_bilateral = sp.limit(h, x, 2)
print("lim x->2 h(x) (sympy bilateral) =", lim_bilateral)
print("¿Límites laterales iguales?", lim_izq == lim_der)

# 3) Tabla de valores acercándose a 2
print("\n--- Tabla de valores ---")
izq_vals = [sp.Rational(19, 10), sp.Rational(199, 100), sp.Rational(1999, 1000)]
der_vals = [sp.Rational(21, 10), sp.Rational(201, 100), sp.Rational(2001, 1000)]
print("Lado izquierdo (x -> 2-):")
for v in izq_vals:
    print(f"  x = {float(v)}  ->  h(x) = {float(h.subs(x, v)):.1f}")
print("Lado derecho (x -> 2+):")
for v in der_vals:
    print(f"  x = {float(v)}  ->  h(x) = {float(h.subs(x, v)):.1f}")

# Conclusión
print("\n--- Conclusión ---")
print("h(2) existe:", False)
print("lim x->2 h(x) existe (finito):", False, "(límites laterales distintos: -oo != +oo)")
print("Clasificación: discontinuidad inevitable de salto infinito (asíntota vertical en x=2)")
