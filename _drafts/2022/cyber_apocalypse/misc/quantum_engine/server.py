import socketserver
from secrets import flag
import signal
from qiskit import *
import itertools

class CircuitException(Exception):
    pass


class Circuit:

    def __init__(self, inputGates) -> None:
        self.a = 0
        self.b = 0
        self.c = 0
        self.inputGates = inputGates
    
    def append_HGate(self, qbit):
        qbit = int(qbit)
        if qbit in range(4):
            self.circuit.h(qbit)
        else:
            raise CircuitException('Non-valid qbit position given...')
    
    def append_TGate(self, qbit):
        qbit = int(qbit)
        if qbit in range(4):
            self.circuit.t(qbit)
        else:
            raise CircuitException('Non-valid qbit position given...')

    def append_TdgGate(self, qbit):
        qbit = int(qbit)
        if qbit in range(4):
            self.circuit.tdg(qbit)
        else:
            raise CircuitException('Non-valid qbit position given...')

    def append_CZGate(self, qbits):
        qbits = qbits.split(',')
        c_qubit = int(qbits[0])
        t_qubit = int(qbits[1])

        if c_qubit in range(4) and t_qubit in range(4):
            self.circuit.cz(c_qubit, t_qubit)
        else:
            raise CircuitException('Non-valid qbit position given...')


    def generate_Circuit(self):

        self.circuit = QuantumCircuit(4,3)

        if self.a == 1:
            self.circuit.x(0)
        if self.b == 1:
            self.circuit.x(1)
        if self.c == 1:
            self.circuit.x(2)
        
        for gate in self.inputGates:
            gate = gate.split(':')
            if gate[0] == 'H':
                self.append_HGate(gate[1])
            elif gate[0] == 'T':
                self.append_TGate(gate[1])
            elif gate[0] == 'TDG':
                self.append_TdgGate(gate[1])
            elif gate[0] == 'CZ':
                self.append_CZGate(gate[1])
            else:
                raise CircuitException('Non-valid gate given...')

        self.circuit.measure([0,2,3],[0,1,2])
        if self.circuit.depth() > 43:
            raise CircuitException('Circuit is too big...')
        
    def check_Circuit(self):
        inputs = list(itertools.product([0, 1], repeat=3))

        for input in inputs:
            self.a = input[0]
            self.b = input[1]
            self.c = input[2]

            self.generate_Circuit()

            simulator = Aer.get_backend('qasm_simulator')
            counts = execute(self.circuit,backend=simulator, shots = 1).result().get_counts()
            counts = next(iter(counts))[::-1]
            if (int(counts[0]) == self.a) and int(counts[1]) == self.c ^self.a ^ self.b and (int(counts[2]) == self.a&self.b|self.b&self.c|self.c&self.a):
                pass
            else:
                return False
        return True

        

def challenge(req):
    try:
        req.sendall(b'|--------------------------------|\n'+
                    b'| Phalcon\'s Accelaration System |\n'+
                    b'|--------------------------------|\n'+
                    b'| > Send quantum circuit for the |\n'+
                    b'| system to analyze...           |\n'+
                    b'|--------------------------------|\n'+
                    b'\n> '
                    )
        input = req.recv(4096).decode().strip().split(';')

        if len(input) < 0 or len(input) > 100:
            raise CircuitException('Non-valid circuit length...')
        
        quantumCircuit = Circuit(input)
        
        if quantumCircuit.check_Circuit():
            req.sendall(flag.encode()+b"\n")
            req.close()
            exit()
        else:
            req.sendall(b'The circuit failed to pass the test...\n')
            req.close()
            exit()


    except CircuitException as ce:
        try:
            req.sendall(ce.encode()+b'\n')
            req.close()
        except:
            pass
        exit()

    except Exception as e:
        try:
            req.sendall(b'Unexpected error.\n')
            req.close()
        except:
            pass
        exit()

class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(300)
        req = self.request
        print("starting server")
        while True:
            challenge(req)

class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

socketserver.TCPServer.allow_reuse_address = False
server = ReusableTCPServer(("0.0.0.0", 1337), incoming)
server.serve_forever()