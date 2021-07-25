site = {'location': 'London', 'code': 'ZUK92', 'Tier': 1, 'users': 500}
print(site)

site1 = site.copy()
print(id(site), id(site1))

# site.clear()
# print(site)

site_template_keys = ['code', 'location', 'tier', 'users']
# site_template = {}.fromkeys(site_template_keys)
site_template = dict.fromkeys(site_template_keys)
print(site_template)

site_london = dict.fromkeys(site_template_keys)
site_london['code'] = 'ZUK92'
site_london['location'] = 'London'
site_london['tier'] = 1
site_london['users'] = 750
print(site_london)

print(site_london.get('code'))
print(site_london.get('router_model', 'Oops!'))
print(site_london)
print(site_london.setdefault('ios version', 15.1))
print(site_london)


routers = dict.fromkeys(['name', 'model', 'version'], 'r1')
print(routers)

print(routers.keys(), type(routers.keys()))
print(routers.items())

site_london1 = site_london # Create another pointer to the same memory location.
# Both site_london and site_london1 refer to the same variable. You can create an independent variable with dict.copy() method.
print(id(site_london), id(site_london1))
site_london1.update({'users' : 50})
print(site_london1)
print(site_london)

p = site_london.pop('ios version')
print(p)
print(site_london)

# Below example shows that you can't create a dictionary with dict.fromkeys() method when you use changeable types as values (list for example).
# Because all values will point to the same location in memory! Keep this in mind!
new_site = dict.fromkeys(site_template_keys, list())
print(new_site)
new_site['code'].append(1)
print(new_site)