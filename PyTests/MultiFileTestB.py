import builderTest
choc = builderTest.Chocolate.Builder(1).b(2).c(3).compile();
print(choc.a, choc.b, choc.c);