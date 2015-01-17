union foo switch (int type) {
    case 1:
        int a;
    case 2:
        int b;
    case 3:
        string c<>;
    case 4:
        bar d;
};

struct bar {
    int a;
    int b;
};
