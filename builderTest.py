class Chocolate:
    def __init__(self):
        self.a = None;
        self.b = None;
        self.c = None;
        pass

    class Builder:
        def __init__(self, a):
            self.a = a;
        
        def b(self, b):
            self.b = b;
            return self;
        
        def c(self, c):
            self.c = c;
            return self;

        def compile(self):
            choc = Chocolate();
            choc.a = self.a;
            choc.b = self.b;
            choc.c = self.c;
            return choc;

c = Chocolate.Builder(1).c(2).b(3).compile();
print(c.a, c.b, c.c);