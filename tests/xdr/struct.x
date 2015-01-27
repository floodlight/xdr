const X = 3;

struct foo {
    int a;
    int b[X];
    int c<2>;
    string d<>;
    opaque e<X>;
    bar f;
};

enum bar {
    I = 100,
    J = 200
};
