


A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R, S, T, U, V = "ABCDEFGHIJKLMNOPRSTUV"

zemljevid = {
    (A, B): "gravel trava",
    (A, V): "pešci lonci",
    (B, C): "bolt lonci",
    (B, V): "",
    (C, R): "stopnice pešci lonci",
    (D, F): "stopnice pešci",
    (D, R): "pešci",
    (E, I): "trava lonci",
    (F, G): "trava črepinje",
    (G, H): "črepinje pešci",
    (G, I): "avtocesta",
    (H, J): "robnik bolt",
    (I, M): "avtocesta",
    (I, P): "gravel",
    (I, R): "stopnice robnik",
    (J, K): "",
    (J, L): "gravel bolt",
    (K, M): "stopnice bolt",
    (L, M): "robnik pešci",
    (M, N): "rodeo",
    (N, P): "gravel",
    (O, P): "gravel",
    (P, S): "",
    (R, U): "trava pešci",
    (R, V): "pešci lonci",
    (S, T): "robnik trava",
    (T, U): "gravel trava",
    (U, V): "robnik lonci trava"
}

vrednosti_vescin = {
    "črepinje": 1,
    "robnik": 1,
    "lonci": 1,
    "gravel": 2,
    "bolt": 2,
    "rodeo": 2,
    "trava": 3,
    "pešci": 4,
    "stopnice": 6,
    "avtocesta": 10
}
zemljevid = {k: set(v.split()) for k, v in zemljevid.items()} | {k[::-1]: set(v.split()) for k, v in zemljevid.items()}

mali_zemljevid = {(A, B): "robnik bolt",  # 3
                  (A, C): "bolt rodeo pešci",  # 8
                  (C, D): ""}  # 0

mali_zemljevid = {k: set(v.split()) for k, v in mali_zemljevid.items()} | {k[::-1]: set(v.split()) for k, v in mali_zemljevid.items()}


import string
import unittest
import ast
from collections import defaultdict

def vrednost_povezave(povezava,  zemljevid):
    return sum([vrednosti_vescin[v] for v in zemljevid[povezava]])

def najboljsa_povezava(zemljevid):
    return max(zemljevid, key=lambda povezava: vrednost_povezave(povezava, zemljevid))

def vrednost_poti(pot, zemljevid):
    return sum([vrednost_povezave((pot[i], pot[i+1]), zemljevid) for i in range(len(pot)-1)])

def najbolj_uporabna(pot, zemljevid):
    stevec_uporab = defaultdict(int)
    for i in range(len(pot)-1):
        key = (pot[i], pot[i+1])
        for vescina in zemljevid[key]:
            stevec_uporab[key] += 1          
    return max(stevec_uporab, key=stevec_uporab.get, default=None)

def naslednje_tocke(tocke, zemljevid, vescine):
    return tocke | {k2 for (k1, k2), v in zemljevid.items() if k1 in tocke and v.issubset(vescine)}

def dosegljive(tocka, zemljevid, vescine):
    prvotne = set()
    dosegljive_temp = {tocka}
    while dosegljive_temp > prvotne:
        prvotne = dosegljive_temp
        dosegljive_temp = naslednje_tocke(dosegljive_temp, zemljevid , vescine)
    return dosegljive_temp

class Ocena_06(unittest.TestCase):
    def test01_vrednost_povezave(self):
        self.assertEqual(5, vrednost_povezave((V, R), zemljevid))
        self.assertEqual(10, vrednost_povezave((G, I), zemljevid))
        self.assertEqual(4, vrednost_povezave((R, D), zemljevid))
        self.assertEqual(0, vrednost_povezave((S, P), zemljevid))
        self.assertEqual(11, vrednost_povezave((C, R), zemljevid))

        self.assertEqual(3, vrednost_povezave((A, B), mali_zemljevid))

    def test_02_najboljsa_povezava(self):
        self.assertIn(
            najboljsa_povezava({
                (A, C): {"avtocesta"}, (C, A): {"avtocesta"},  # 10
                (A, B): set("stopnice pešci trava".split()), (B, A): set("stopnice pešci trava".split()), # 12
                (A, D): set("črepinje robnik lonci gravel".split()), (D, A): set("črepinje robnik lonci gravel".split()) # 5
            }),
            {(A, B), (B, A)})

        self.assertIn(najboljsa_povezava(zemljevid), {(C, R), (R, C)})
        self.assertIn(najboljsa_povezava(mali_zemljevid), {(A, C), (C, A)})

    def test_03_vrednost_poti(self):
        self.assertEqual(8, vrednost_poti("ABC", zemljevid))
        self.assertEqual(33, vrednost_poti("ABCRDF", zemljevid))
        self.assertEqual(0, vrednost_poti("SPSPSP", zemljevid))
        self.assertEqual(0, vrednost_poti("M", zemljevid))

        self.assertEqual(8, vrednost_poti("ACDC", mali_zemljevid))



class Ocena_09(unittest.TestCase):
    def test_00_enovrsticne(self):
        functions = {
            elm.name: elm
            for elm in ast.parse(open(__file__, "r", encoding="utf-8").read()).body
            if isinstance(elm, ast.FunctionDef)}

        dovoljene_funkcije = set("vrednost_povezave najboljsa_povezava vrednost_poti najbolj_uporabna "
                                 "mozna_pot koncna_tocka do_nagrade naslednje_tocke dosegljive dosegljive_n naj_vescine".split())
        for func in functions:
            self.assertIn(func, dovoljene_funkcije, f"\nFunkcija {func} ni dovoljena.")

        for func in (vrednost_povezave, najboljsa_povezava, vrednost_poti, naslednje_tocke):
            body = functions[func.__code__.co_name].body
            self.assertEqual(len(body), 1, "\nFunkcija ni dolga le eno vrstico")
            self.assertIsInstance(body[0], ast.Return, "\nFunkcija naj bi vsebovala le return")

    def test_01_naslednje_tocke(self):
        self.assertEqual({S, P, O, N, I}, naslednje_tocke({P}, zemljevid, {"gravel"}))
        self.assertEqual({S, P, O, N, I}, naslednje_tocke({P}, zemljevid, {"gravel", "rodeo"}))
        self.assertEqual({N, M, P}, naslednje_tocke({N}, zemljevid, {"gravel", "rodeo"}))
        self.assertEqual({N, M}, naslednje_tocke({N}, zemljevid, {"rodeo"}))

        self.assertEqual({V, A, B, R, F, D}, naslednje_tocke({V, F}, zemljevid, set("pešci stopnice lonci rodeo".split())))
        self.assertEqual({V, A, B, R, F, D, P, S}, naslednje_tocke({V, F, P}, zemljevid, set("pešci stopnice lonci rodeo".split())))
        self.assertEqual({V, A, B, R, F, D, P, S}, naslednje_tocke({V, F, P}, zemljevid, set("pešci stopnice lonci rodeo".split())))
        self.assertEqual({V, A, B, R, F, D, P, S, O, N, I}, naslednje_tocke({V, F, P}, zemljevid, set("pešci stopnice lonci rodeo gravel".split())))


class Ocena_10(unittest.TestCase):
    def test_01_dosegljivo(self):
        self.assertEqual({N, S, P, O, I}, dosegljive(N, zemljevid, {"gravel"}))
        self.assertEqual({N, S, P, O, I, G, M}, dosegljive(N, zemljevid, {"gravel", "avtocesta"}))
        self.assertEqual({N, S, P, O, I, G, M}, dosegljive(N, zemljevid, {"gravel", "avtocesta", "rodeo"}))
        self.assertEqual({N, S, P, O, I, M}, dosegljive(N, zemljevid, {"gravel", "rodeo"}))

        self.assertEqual({H, J, L, K, M, N}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci trava".split())))
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci trava črepinje".split())))
        # zdaj je dosegljivo vse
        self.assertEqual({H, J, L, K, M, N, I, G, R, D, F, V, A, B, C, U, E, S, T, P, O}, dosegljive(M, zemljevid, set("robnik pešci rodeo stopnice bolt avtocesta lonci trava črepinje gravel".split())))

if "__main__" == __name__:
    unittest.main()