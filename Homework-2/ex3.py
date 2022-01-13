from qiskit import *
from qiskit.visualization import *
from qiskit.circuit.library import *
from qiskit.circuit import *
import matplotlib.pyplot as plt
import numpy as np
import cmath
import math
from fractions import Fraction

def algebric(a,x,n):
    raspuns=1
    while x>0:
        raspuns=(raspuns*a)%n
        x=x-1
    return raspuns


#for i in range(100):
#    print("Pas: ",i+1,"=>",algebric(9,i+1,55))




def algebric_optim(a,x,n):
    contor=1
    first_value=a

    rest=n*[None]#maxim n resturi
    rest[contor]=first_value
    contor=contor+1

    #elementele distincte dintr-o perioada:
    curr_val=first_value*a%n
    while curr_val!=first_value:
        rest[contor]=curr_val
        contor=contor+1
        curr_val=curr_val*a%n
    nr_rests=contor

    #umplem resturile in functie de perioada gasita:
    coord=(x+10)*[None]

    contor=1
    coord[0]=1
    for i in range(1,x+1):
        if contor==nr_rests:
            contor=1
        print("Pasul: ",i,"=>",rest[contor])
        coord[i]=rest[contor]
        contor=contor+1

    xvals=range(0,x+1)
    yvals=coord[0:x+1]
    fig, ax = plt.subplots()
    ax.plot(xvals,yvals,linewidth=1,linestyle='dotted',marker='x')
    ax.set(xlabel='$x$', ylabel='$%i^x$ mod $%i$' % (a, n),title="Periodic Function")
    try:    # plot r on the graph
        r = yvals[1:].index(1) + 1      # indexul urmatorului '1' imediat dupa a^0 (+1 => perioada)
        plt.annotate('', xy=(0,1), xytext=(r,1), arrowprops=dict(arrowstyle='<->'))
        plt.annotate('$r=%i$' % r, xy=(r/3,1.5))
        plt.show()
    except ValueError:
        print('Could not find period, check a < N and have no common factors.')

algebric_optim(9,100,55)



def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,7,8,11,13]:  #cum le-a luat aici?
        raise ValueError("'a' must be 2,7,8,11 or 13")
    U = QuantumCircuit(4)        
    for iteration in range(power):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a == 11:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U


def perioada(a, nr_mod):
    m=math.ceil(math.log(nr_mod,2))
    n=2*m

    circuit=QuantumCircuit(n+m,n)

    for i in range(n):
        circuit.h(i)

    circuit.x(n+m-1)

    #poarta pentru functie: c_amod15(a,power)
    for i in range(n):
        circuit.append(c_amod15(a, 2**i),[i] + [j+n for j in range(m)])

    circuit=circuit.compose(QFT(n,0,True,True,False,None))

    circuit.measure(range(n),range(n))

    print(circuit.draw(fold=-1))

    simulator=Aer.get_backend('qasm_simulator')
    result=execute(circuit,simulator,shots=10000).result()
    counts=result.get_counts()
    plot_histogram(counts).savefig('ex3.b.png')
    print("Rezultat :")
    print(counts)

    phases=[]
    for string in counts:
        decimal = int(string,base=2)
        phase = decimal/(2**n)
        phases.append(phase)
    for phase in phases:
        print("Faza pentru rezultat: ",phase)

    guess=[]
    for phase in phases:
        frac = Fraction(phase).limit_denominator(nr_mod)
        guess.append(frac.denominator)
    for i in guess:
        print("Perioada pentru rezultat: ",i)

    print("Rezultat gresit pentru valoarea 0, fie rezulta un factor al perioadei")

perioada(11,15)


