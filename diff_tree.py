from l4_ex4 import Stack
import re


class BinaryTree:
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        """Adds left child (new_node) to the node. New_node can be a value or a tree."""
        if not isinstance(new_node, BinaryTree):
            if not self.left_child:
                self.left_child = BinaryTree(new_node)
            else:
                t = BinaryTree(new_node)
                t.left_child = self.left_child
                self.left_child = t
        else:
            self.left_child = new_node

    def insert_right(self, new_node):
        """Adds right child (new_node) to the node. New_node can be a value or a tree."""
        if not isinstance(new_node, BinaryTree):
            if not self.right_child:
                self.right_child = BinaryTree(new_node)
            else:
                t = BinaryTree(new_node)
                t.right_child = self.right_child
                self.right_child = t
        else:
            self.right_child = new_node

    def get_right_child(self):
        """Returns right child of a node."""
        return self.right_child

    def get_left_child(self):
        """Returns left child of a node."""
        return self.left_child

    def set_root_val(self, obj):
        """Change value of a node to given."""
        self.key = obj

    def get_root_val(self):
        """Returns value of a node."""
        return self.key

    def has_any_children(self):
        """Returns true if a node has any child."""
        return self.right_child or self.left_child

    def has_both_children(self):
        """Returns true if a node has both children."""
        return self.right_child and self.left_child

    def is_leaf(self):
        """Returns true if the node is a leaf."""
        return not self.has_any_children()

    def __str__(self):
        """Override of print method."""
        return str(self._print_tree())

    def _print_tree(self):
        """Helper function to the print method, returns a list of all nodes [node, left_child, right_child]."""
        if isinstance(self.key, BinaryTree):
            return self.key._print_tree()

        if not self.has_any_children():
            return [self.key, [], []]
        elif self.has_both_children() and self.left_child and self.right_child:
            return [self.key, self.left_child._print_tree(), self.right_child._print_tree()]
        elif self.get_left_child():
            return [self.key, self.left_child._print_tree(), []]
        elif self.get_right_child():
            return [self.key, [], self.right_child._print_tree()]


def build_parse_tree(fp_exp):
    """ Function takes math expression and converts them to BinaryTrees. We assume that the expression is correct:
    brackets surround each operation and its operands and every sign is separated with space.
    Returns instance of class BinaryTree or ValueError."""
    fp_exp = re.sub(r'([a-z]{2,})', r'# \1', fp_exp)  # '# sin x'
    fp_list = fp_exp.split()
    p_stack = Stack()
    e_tree = BinaryTree('')
    p_stack.push(e_tree)
    current_tree = e_tree
    for i in fp_list:
        if i == '(':
            current_tree.insert_left('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_left_child()

        elif i not in ['+', '-', '*', '/', ')', 'sin', 'cos', 'log', 'exp', "**"]:
            current_tree.set_root_val(i)
            parent = p_stack.pop()
            current_tree = parent

        elif i in ['+', '-', '*', '/', '**', 'sin', 'cos', 'log', 'exp']:
            current_tree.set_root_val(i)
            current_tree.insert_right('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_right_child()

        elif i == ')':
            current_tree = p_stack.pop()
        else:
            raise ValueError
    return e_tree


def _cut_tree(e_tree):
    """Helper function. Converts e_tree(instance of class BinaryTree) to appropriate list."""
    if e_tree.is_leaf():
        return e_tree.key
    else:
        return [_cut_tree(e_tree.left_child), e_tree.key, _cut_tree(e_tree.right_child)]


def cut_tree(e_tree):
    """Converts e_tree(instance of class BinaryTree) to a string (math expression)."""
    exp_str = str(_cut_tree(e_tree))
    exp_str = re.sub("\'", '', exp_str)
    exp_str = re.sub(",", '', exp_str)
    exp_str = re.sub(r'\[', '(', exp_str)
    exp_str = re.sub(r'\]', ')', exp_str)
    exp_str = re.sub(r'# ', '', exp_str)
    return exp_str


def dif_of_fun(fun):
    """Helper function. Returns derivative (str) of sin, cos and exp."""
    if fun == "sin":
        return "cos"
    elif fun == "cos":
        return "-sin"
    elif fun == "exp":
        return "exp"
    else:
        return fun


def diff_parse_tree(e_tree):
    """Takes a BinaryTree and returns derivative (with respect to x) of this tree. Compute derivatives of +, -, *, /,
    sin, cos, exp, log, **, (power must be float or int) and compound functions."""
    current_tree = e_tree
    current = e_tree.key
    new_tree = BinaryTree("")

    if e_tree.is_leaf():
        if current == "x":
            new_tree.set_root_val('1')
            return new_tree.key
        else:
            new_tree.set_root_val('0')
            return new_tree.key

    elif current in ["*", "/", "+", "-", "**", "sin", "cos", "log", "exp"]:
        tem_l = current_tree.left_child
        tem_r = current_tree.right_child

        if current == "*":
            new_tree.set_root_val("+")
            new_tree.insert_left("*")
            new_tree.insert_right("*")
            new_tree.left_child.insert_left(diff_parse_tree(tem_l))
            new_tree.left_child.insert_right(tem_r)
            new_tree.right_child.insert_left(tem_l)
            new_tree.right_child.insert_right(diff_parse_tree(tem_r))

        elif current == "+":
            new_tree.set_root_val("+")

            new_tree.insert_left(diff_parse_tree(tem_l))
            new_tree.insert_right(diff_parse_tree(tem_r))

        elif current == "-":
            new_tree.set_root_val("-")
            new_tree.insert_left(diff_parse_tree(tem_l))
            new_tree.insert_right(diff_parse_tree(tem_r))

        elif current == "/":
            new_tree.set_root_val("/")
            new_tree.insert_right("*")
            new_tree.right_child.insert_left(tem_r)
            new_tree.right_child.insert_right(tem_r)
            new_tree.insert_left("-")
            new_tree.left_child.insert_left("*")
            new_tree.left_child.insert_right("*")
            temp_left = new_tree.left_child.left_child
            temp_right = new_tree.left_child.right_child
            temp_left.insert_left(diff_parse_tree(tem_l))
            temp_left.insert_right(tem_r)
            temp_right.insert_left(tem_l)
            temp_right.insert_right(diff_parse_tree(tem_r))

        elif current == "**":
            new_tree.set_root_val("*")
            new_tree.insert_left("*")
            new_tree.left_child.insert_left(tem_r)
            if float(tem_r.key) - 1 == 1.0:
                new_tree.left_child.insert_right(tem_l)
            elif float(tem_r.key) - 1 == 0.0:
                new_tree.left_child.insert_right(1)
            else:
                new_tree.left_child.insert_right("**")
                new_tree.left_child.right_child.insert_left(tem_l)
                new_tree.left_child.right_child.insert_right(float(tem_r.key) - 1)
            new_tree.insert_right(diff_parse_tree(tem_l))

        elif current in ["sin", "cos", "exp"]:
            new_tree.set_root_val("*")
            new_tree.insert_left(dif_of_fun(current))
            new_tree.left_child.insert_right(tem_r)
            new_tree.left_child.insert_left("#")
            new_tree.insert_right(diff_parse_tree(tem_r))

        elif current == "log":
            new_tree.set_root_val("*")
            new_tree.insert_left("/")
            new_tree.left_child.insert_left(1)
            new_tree.left_child.insert_right(tem_r)
            new_tree.insert_right(diff_parse_tree(tem_r))

    return new_tree


if __name__ == '__main__':
    pt = build_parse_tree("( x * 2 )")
    print("parsed expression: ", pt)
    tree = diff_parse_tree(pt)
    print("derivative (tree): ", tree)
    print("derivative (expression): ", cut_tree(tree))
    print()

    s1 = "( ( x + 2 ) + 6 )"
    pt1 = build_parse_tree(s1)
    tree1 = diff_parse_tree(pt1)
    print(f"{s1}' = {cut_tree(tree1)}")

    s2 = "( ( 5 - x ) + ( 6 * x ) )"
    pt2 = build_parse_tree(s2)
    tree2 = diff_parse_tree(pt2)
    print(f"{s2}' = {cut_tree(tree2)}")

    s3 = "( x / 5 )"
    pt3 = build_parse_tree(s3)
    tree3 = diff_parse_tree(pt3)
    print(f"{s3}' = {cut_tree(tree3)}")

    s4 = "( sin x )"
    pt4 = build_parse_tree(s4)
    tree4 = diff_parse_tree(pt4)
    print(f"{s4}' = {cut_tree(tree4)}")

    s5 = "( cos ( x + 2 ) )"
    pt5 = build_parse_tree(s5)
    tree5 = diff_parse_tree(pt5)
    print(f"{s5}' = {cut_tree(tree5)}")

    s6 = "( log ( exp x ) )"
    pt6 = build_parse_tree(s6)
    tree6 = diff_parse_tree(pt6)
    print(f"{s6}' = {cut_tree(tree6)}")

    s7 = "( x ** 3 )"
    pt7 = build_parse_tree(s7)
    tree7 = diff_parse_tree(pt7)
    print(f"{s7}' = {cut_tree(tree7)}")

    s8 = "( ( x ** -9 ) + ( ( sin x ) / ( cos x ) ) )"
    pt8 = build_parse_tree(s8)
    tree8 = diff_parse_tree(pt8)
    print(f"{s8}' = {cut_tree(tree8)}")

    s9 = "( log ( sin ( x + ( ( x + 3 ) * x ) ) ) )"
    pt9 = build_parse_tree(s9)
    tree9 = diff_parse_tree(pt9)
    print(f"{s9}' = {cut_tree(tree9)}")

    s10 = "( ( x + 2 ) ** 6 )"
    pt10 = build_parse_tree(s10)
    tree10 = diff_parse_tree(pt10)
    print(f"{s10}' = {cut_tree(tree10)}")
