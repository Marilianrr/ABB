class ArvoreBinaria:
    class Node:
        def __init__(self, chave, registro):
            self.chave = chave # Chave de busca (por exemplo, CPF)
            self.registro = registro # Registro de dados (sequência de bytes)
            self.left = None
            self.right = None
            self.duplicates = [] # Lista de registros duplicados com a mesma chave

    def __init__(self, num_registros, tamanho_registro):
        self.edl = [b'\x00' * tamanho_registro] * num_registros  # Arquivo de registros (sequências de bytes)
        self.tamanho_registro = tamanho_registro
        self.index = {}  # Dicionário para mapear chaves para posições na EDL
        self.root = None  # Raiz da árvore binária

    def insert(self, chave, registro):
        posicao = len(self.index)
        self.index[chave] = posicao  # Mapeia a chave para a posição na EDL
        self.edl[posicao] = registro   # Insere o registro na EDL
        self.root = self._insert_node(self.root, chave, registro)  # Insere na árvore

    def delete(self, chave):
        if chave in self.index:
            posicao = self.index[chave]
            self.edl[posicao] = b' ' * self.tamanho_registro  # Marca a posição na EDL como vazia
            del self.index[chave]  # Remove a chave do índice
            self.root = self._delete_node(self.root, chave)  # Remove da árvore

    def access(self, chave):
        node = self._search_node(self.root, chave)

        if node:
            posicao = self.index[chave]
            registro = self.edl[posicao]

            print(f"Chave de busca: {chave}")
            print(f"Posição na EDL: {posicao}")
            print(f"Registro de dados: {registro.decode('utf-8')}")
        else:
            print(f"Registro com chave {chave} não encontrado na base de dados.")

    def ordered_edl(self):
        return self._inorder_traversal(self.root)

    def _insert_node(self, node, chave, registro):
        if node is None:
            return self.Node(chave, registro) # Cria um novo nó se o nó atual for nulo
        if chave == node.chave:
            node.duplicates.append(registro)  # Se a chave for a mesma, adiciona à lista de duplicatas
        elif chave < node.chave:
            node.left = self._insert_node(node.left, chave, registro)  # Insere à esquerda
        else:
            node.right = self._insert_node(node.right, chave, registro)  # Insere à direita
        return node

    def _delete_node(self, node, chave):
        if node is None:
            return node
        if chave == node.chave:
            if node.duplicates:
                node.duplicates.pop()  # Remove uma duplicata se existir
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                min_key = self._min_value_node(node.right)
                node.chave = min_key
                node.right = self._delete_node(node.right, min_key)
        elif chave < node.chave:
            node.left = self._delete_node(node.left, chave)
        else:
            node.right = self._delete_node(node.right, chave)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current.chave

    def _search_node(self, node, chave):
        if node is None or chave == node.chave:
            return node
        if chave < node.chave:
            return self._search_node(node.left, chave)
        return self._search_node(node.right, chave)

    def _inorder_traversal(self, node):
        result = []
        if node:
            result.extend(self._inorder_traversal(node.left))
            result.append(node.chave)
            if node.duplicates:
                result.extend(node.duplicates)
            result.extend(self._inorder_traversal(node.right))
        return result

if __name__ == "__main__":
    num_registros = 5
    tamanho_registro = 12

    arvore = ArvoreBinaria(num_registros, tamanho_registro)

    arvore.insert("12345678901", b'Joao       ')
    arvore.insert("98765432109", b'Maria      ')
    arvore.insert("45678901234", b'Pedro      ')
    arvore.insert("78901234567", b'Ana        ')
    arvore.insert("23456789012", b'Carlos     ')

    print("Listagem de Pessoas na EDL (Desordenada):")
    for chave, posicao in arvore.index.items():
        registro = arvore.edl[posicao]
        print(f"Chave: {chave}, Posição: {posicao}, Registro: {registro.decode('utf-8')}")

    print("\nListagem de Pessoas na EDL (Ordenada):")
    for chave in arvore.ordered_edl():
        print(f"Chave: {chave}, Registro: {arvore.edl[arvore.index[chave]].decode('utf-8')}")
