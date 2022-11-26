import pandas as pd

fitches = pd.read_csv('Leninka_fitches_normal_big_categories.csv')
spheres = pd.read_csv('Leninka_3.csv')

new_column = []

# for one_fitcha in fitches:
#     count = 0
#     for one_sphere in spheres:
#         if one_fitcha['ID'] == one_sphere['ID']:
#             sph = one_sphere['Сфера ИТ']
#             if count == 0:
#                 sphereIT = sph
#             else:
#                 sphereIT += f',{sph}'
    
#     new_column.append(sphereIT)

spheres_ids = spheres['ID']
fitches_ids = fitches['ID']
spheres_sph = spheres['Сфера ИТ']

index_f = 0
for id_f in fitches_ids:
    index_s = 0
    flag = False
    sphereIT = ''

    for id_s in spheres_ids:
        if id_s == id_f:
            sph = spheres_sph[index_s]

            if not flag:
                sphereIT = sph
            else:
                sphereIT += f',{sph}'
            flag = True

        if sphereIT == '':
            sphereIT = None

        index_s += 1
    new_column.append(sphereIT)
    index_f += 1

# print(new_column)

fitches["IT sphere"] = new_column

fitches.to_csv('./concat info.csv')
