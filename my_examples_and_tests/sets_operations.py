set1 = {}
print(type(set1))

set1 = set()
print(type(set1))

set1 = {1, 2, 3, 4}
set2 = {2, 4, 6, 8}
print(set1)
print(set2)

print(set1.union(set2))
print(set1.intersection(set2))

print(set1 & set2 == set1.intersection(set2))
print(set1 | set2 == set2.union(set1))


