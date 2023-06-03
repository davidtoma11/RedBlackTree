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
        self.color = 0          # Culoarea nodului (0 = negru, 1 = roșu)

# Definim clasa pentru RedBlackTree
class RedBlackTree:
    # Constructorul clasei. Initializam arborele cu un nod nil (un nod fictiv, negru)
    def __init__(self):
        self.nil = Node(None)
        self.nil.color = 0      # Nodul nil este negru
        self.root = self.nil    # Initial, arborele nu are niciun nod, deci rădăcina este nil

    def insert(self, key):
        # Cream un nou nod cu cheia specificată
        new_node = Node(key)

        # Adaugam nodul ca o frunza
        new_node.left = self.nil
        new_node.right = self.nil

        current = self.root  # Pornim de la rădăcina arborelui
        parent = None

        while current != self.nil:
            parent = current  # Nodul curent devine parintele pentru urmatorul pas

            # Comparăm cheia noului nod cu cheia nodului curent
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right


        new_node.parent = parent  # Conectam noul nod ca fiu al parintelui gasit
        if parent is None:
            # Daca parintele este None, inseamna că arborele era inițial gol și noul nod devine radacina arborelui
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Setam culoarea noului nod la rosu
        new_node.color = 1

        # "Reparam" arborele
        self.insert_fixup(new_node)


    def insert_fixup(self, node):
        while node.parent is not None and node.parent.color == 1:  # Verificăm dacă părintele nodului este roșu
            if node.parent == node.parent.parent.left:  # Cazul în care părintele nodului este fiul stâng al bunicului său
                uncle = node.parent.parent.right  # Obținem unchiul nodului (fratele părintelui)
                if uncle.color == 1:  # Cazul 1: Unchiul nodului este, de asemenea, roșu
                    node.parent.color = 0
                    uncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # Cazul 2: Unchiul nodului este negru și nodul este fiul drept al părintelui
                        node = node.parent  # Reducem cazul 2 la cazul 3 prin rotire la stânga pe părinte
                        self.left_rotate(node)
                    # Cazul 3: Unchiul nodului este negru și nodul este fiul stâng al părintelui
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            else:  # Cazul în care parintele nodului este fiul drept al bunicului sau
                uncle = node.parent.parent.left
                if uncle.color == 1:  # Cazul 1: Unchiul nodului este, de asemenea, roșu
                    node.parent.color = 0
                    uncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # Cazul 2: Unchiul nodului este negru și nodul este fiul stâng al părintelui
                        node = node.parent  # Reducem cazul 2 la cazul 3 prin rotire la dreapta pe părinte
                        self.right_rotate(node)
                    # Cazul 3: Unchiul nodului este negru și nodul este fiul drept al părintelui
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)

        self.root.color = 0  # Setăm culoarea rădăcinii la negru pentru a respecta proprietățile Red-Black Tree


    def right_rotate(self, x):
        # Salvam copilul stanga al nodului x în variabila y
        y = x.left

        # Actualizam legatura dintre x și copilul dreapta al lui y
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x

        # Actualizăm legăturile dintre y și părinții lui x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        # Setam x ca fiu drept al lui y
        y.right = x

        # Setam y ca părinte al lui x
        x.parent = y


    def left_rotate(self, x):
        # Salvam copilul dreapta al nodului x în variabila y
        y = x.right

        # Actualizăm legatura dintre x și copilul stanga al lui y
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        # Actualizam legăturile dintre y și părinții lui x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        # Setam x ca fiu stâng al lui y
        y.left = x

        # Setam y ca părinte al lui x
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

    def delete(self, key):

        node = self.search(key)
        if node == self.nil:
            return

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
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color

        # Daca nodul sters era negru, trebuie sa ne asiguram ca regulile de RedBlackTree sunt respectate
        if original_color == 0:
            self.delete_fixup(child)

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
        print(node.key, end="-")
        if node.color == 0:
            print("B")
        else:
            print("R")
        self.show(node.right)


rb_tree = RedBlackTree()

rb_tree.insert(50)
rb_tree.insert(30)
rb_tree.insert(70)
rb_tree.insert(20)
rb_tree.insert(40)
rb_tree.insert(60)
rb_tree.insert(80)


print("Arborele Red-Black dupa inserare:")
rb_tree.show(rb_tree.root)



