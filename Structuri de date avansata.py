# Reguli prinicpale RedBlackTree:
#  - Toate nodurile sunt fie rosii, fie negre
#  - Radacina arborelui este neagra
#  - Daca un nod este rosu, toti copiii acestuia vor fi negrii
#  - Pentru orice nod din arbore, toate drumurile simple de la acest nod la nodurile frunză conțin același număr de noduri negre
#  - Nodurile nil(nodurile frunza) sunt considerate negre


# Definim o clasa pentru un nod din arbore
class Node:
    # Constructorul clasei
    def __init__(self, key):
        self.key = key          # Cheia nodului - valoarea asociata acestuia
        self.left = None        # Subarborele stang al nodului (initial gol)
        self.right = None       # Subarborele drept al nodului (initial gol)
        self.parent = None      # Parintele nodului (initial gol)
        self.color = 1          # Culoarea nodului (0 = negru, 1 = roșu)

# Definim clasa pentru RedBlackTree
class RedBlackTree:
    # Constructorul clasei. Initializam arborele cu un nod nil (un nod fictiv, negru)
    def __init__(self):
        self.nil = Node(None)
        self.nil.color = 0      # Nodul nil este negru
        self.root = self.nil    # Initial, arborele nu are niciun nod, deci rădăcina este nil

    # Functia de inserare a unui nod în arbore
    def insert(self, key):
        # Cream un nou nod
        new_node = Node(key)

        # Initial, noul nod este adaugat la sfarsitul arborelui (ca frunza)
        new_node.left = self.nil
        new_node.right = self.nil

        # Incercam să gasim locul unde sa inseram noul nod
        current = self.root      # Pornim de la radacina arborelui
        parent = None            # Parintele curent initial este nul
        while current != self.nil:
            parent = current     # Nodul curent devine parintele pentru urmatorul pas
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right
        # Am găsit locul unde să inserăm noul nod, deci îl adăugăm ca fiu al părintelui găsit
        new_node.parent = parent
        if parent == None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        # Setăm culoarea noului nod la roșu
        new_node.color = 1
        # Aplicăm regulile de red-black tree pentru a menține proprietățile acestuia

        #self.insert_fixup(new_node)

    # Functia pentru mentinerea proprietatilor RBT, dupa inserarea unui nod
    def insert_fixup(self, node):
        # Cat timp parintele si bunicul nodului nou inserat sunt rosii, trebuie sa aplicam rotatii si schimbari de culori
        if node.parent is not None:
            while node.parent.color == 1 and node.parent != self.root:
                # Daca parintele este fiul stang al bunicului
                if node.parent == node.parent.parent.left:
                    uncle = node.parent.parent.right
                    # Daca unchiul este rosu, schimbam culorile pentru parinte, unchi si bunic, apoi ne mutam in sus in arbore
                    if uncle.color == 1:
                        node.parent.color = 0
                        uncle.color = 0
                        node.parent.parent.color = 1
                        node = node.parent.parent
                    else:
                        # Daca nodul este fiul drept al parintelui, trebuie sa aplicam o rotatie la stanga, astfel incat
                        # parintele sa devina noul nod radacina pentru aceasta subarbore
                        if node == node.parent.right:
                            node = node.parent
                            self.left_rotate(node)
                        # Schimbam culorile pentru parinte si bunic, apoi aplicam o rotatie la dreapta pentru a creste subarborele
                        # spre varful arborelui si pentru a pastra proprietatile Red-Black
                        node.parent.color = 0
                        node.parent.parent.color = 1
                        self.right_rotate(node.parent.parent)
                # Daca parintele este fiul drept al bunicului, procedam simetric
                else:
                    uncle = node.parent.parent.left
                    if uncle.color == 1:
                        node.parent.color = 0
                        uncle.color = 0
                        node.parent.parent.color = 1
                        node = node.parent.parent
                    else:
                        if node == node.parent.left:
                            node = node.parent
                            self.right_rotate(node)
                        node.parent.color = 0
                        node.parent.parent.color = 1
                        self.left_rotate(node.parent.parent)

        # Setam radacina arborelui la negru, pentru a indeplini regula ca radacina trebuie sa fie neagra
        self.root.color = 0

    # Functia de rotire la dreapta a unui subarbore cu rădăcina în nodul x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x  # setăm x ca fiu drept al lui y
        x.parent = y  # setăm y ca părinte al lui x

    # Functia de rotire la stânga a unui subarbore cu radacina în nodul x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Functia de cautare a unui nod x
    def search(self, key):
        current_node = self.root

        while current_node != self.nil:
            if current_node.key == key:
                return current_node

            elif key < current_node.key:
                current_node = current_node.left

            else:
                current_node = current_node.right

        return None

    # Functia de transplant
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Functia de stergere a unui nod x
    def delete(self, key):
        # Cautam nodul cu cheia specificata si il stocam în variabila 'node'
        node = self.search(key)

        # Daca nu am gasit nodul, iesim din functie
        if node == self.nil:
            return

        # Salvam culoarea nodului inainte de a-l șterge
        original_color = node.color

        # Daca nodul are doar un subarbore, il eliminam si ii legam parintelui subarborele corespunzator
        if node.left == self.nil:
            child = node.right
            self.transplant(node, node.right)
        elif node.right == self.nil:
            child = node.left
            self.transplant(node, node.left)

        # Daca nodul are doi subarbori, gasim succesorul sau și il eliminam in locul sau
        else:
            successor = self.minimum(node.right)  # Determinam succesorul nodului dat
            original_color = successor.color
            child = successor.right  # Verificam daca succesorul are un fiu drept, pentru a il putea transplanta ulterior

            # Verificam daca succesorul este fiul direct al nodului de sters
            if successor.parent == node:
                child.parent = successor
            else:
                self.transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

            self.transplant(node, successor)  # Inlocuim nodul cu succesorul
            successor.left = node.left  # Succesorul primeste subarborele stang al nodului de sters
            successor.left.parent = successor
            successor.color = node.color  # Succesorul primeste culoarea originala a nodului de sters

        # Daca nodul sters era negru, trebuie sa ne asiguram ca regulile de RedBlackTree sunt respectate
        if original_color == 0:
            self.delete_fixup(child)

    # Functia pentru mentinerea proprietatilor RBT, dupa stergerea unui nod
    def delete_fixup(self, node):
        # Executam fixup pana cand nodul devine radacina sau culoarea lui este rosie
        while node != self.root and node.color == 0:
            if node == node.parent.left:
                # Nodul este copil stanga al parintelui sau
                sibling = node.parent.right
                # Cazul 1: Fratele nodului este rosu
                if sibling.color == 1:
                    sibling.color = 0
                    node.parent.color = 1
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                # Cazul 2: Fratele nodului si copiii lui sunt negri
                if sibling.left.color == 0 and sibling.right.color == 0:
                    sibling.color = 1
                    node = node.parent
                else:
                    # Cazul 3: Fratele nodului este negru, iar copilul sau din dreapta este rosu
                    if sibling.right.color == 0:
                        sibling.left.color = 0
                        sibling.color = 1
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    # Cazul 4: Fratele nodului este negru si copilul sau din dreapta este negru
                    sibling.color = node.parent.color
                    node.parent.color = 0
                    sibling.right.color = 0
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                # Nodul este copilul dreapta al parintelui sau
                sibling = node.parent.left
                # Cazul 1: Fratele nodului este rosu
                if sibling.color == 1:
                    sibling.color = 0
                    node.parent.color = 1
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                # Cazul 2: Fratele nodului si copiii lui sunt negri
                if sibling.right.color == 0 and sibling.left.color == 0:
                    sibling.color = 1
                    node = node.parent
                else:
                    # Cazul 3: Fratele nodului este negru, iar copilul sau din stanga este rosu
                    if sibling.left.color == 0:
                        sibling.right.color = 0
                        sibling.color = 1
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    # Cazul 4: Fratele nodului este negru si copilul sau din stanga este negru
                    sibling.color = node.parent.color
                    node.parent.color = 0
                    sibling.left.color = 0
                    self.right_rotate(node.parent)
                    node = self.root
        # Nodul devine negru
        node.color = 0

    # Functia de afisare a RBT
    def show(self, node):
        if node == self.nil:
            return
        self.show(node.left)
        print(node.key,end= "")
        if node.color == 0:
            print("B")
        elif node.color == 1:
            print("R")
        self.show(node.right)



