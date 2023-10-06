#include <iostream>

struct Node {

    Node(int v) {
        value = v;
    }

    int value{};
    Node* left = nullptr;
    Node* right = nullptr;
};

void max_beapify(Node* root) {
    if (root == nullptr) return;
    if (root->right == nullptr and root->left == nullptr) return;
    if (root->right == nullptr) {
        if (root->value >= root->left->value) return;
        // swap v and left
        int tmp{root->value};
        root->value = root->left->value;
        root->left->value = tmp;

        max_beapify(root->left);
        return;
    }
    if (root->left == nullptr) {
        if (root->value >= root->right->value) return;
        // swap v and right
        int tmp{root->value};
        root->value = root->right->value;
        root->right->value = tmp;

        max_beapify(root->right);
        return;
    }

    Node* r = root->right;
    Node* l = root->left;
    int v = root->value;
    int lv = l->value;
    int rv = r->value;

    if (v > lv and v > rv) return;

    if (r->left == nullptr) {
        if (rv > lv) {
            // swap right and root
            r->value = v;
            root->value = rv;
        } else {
            // swap left and root
            l->value = v;
            root->value = lv;
        }
        return;
    }

    Node* m = r->left;
    int mv = m->value;

    if (mv > v) { //min(a,b,c,d) is now in position m
        root->value = mv;
        m->value = v;
        mv = v;
        v = root->value;
    }

    if (lv > rv) {
        root->value = lv;
        l->value = v;
        max_beapify(l);
    } else {
        root->value = rv;
        r->value = v;
        max_beapify(r);
    }
}

int main() {
    std::cout << "Hello, World!" << std::endl;

    Node* a1 = new Node(5);

    Node* b1 = new Node(7);
    Node* b2 = new Node(9);

    Node* c1 = new Node(4);
    Node* c2 = new Node(6);
    Node* c3 = new Node(8);

    a1->left = b1; a1->right = b2;
    b1->left = c1; b1->right = c2;
    b2->left = c2; b2->right = c3;

    std::cout << a1->value << std::endl;
    std::cout << b1->value << " " << b2->value << std::endl;
    std::cout << c1->value << " " << c2->value << " " << c3->value << std::endl;

    max_beapify(a1);

    std::cout << a1->value << std::endl;
    std::cout << b1->value << " " << b2->value << std::endl;
    std::cout << c1->value << " " << c2->value << " " << c3->value << std::endl;

    delete a1;
    delete b1; delete b2;
    delete c1; delete c2; delete c3;

    return 0;
}
