def filtraje(marca,subcategoria,fabrica,categorias,Mark,Subcategory,Factory,Category,Product):
    filter_group = []

    if marca:
        filter_group.append(Mark.name.in_(marca))
 
    if subcategoria:
        filter_group.append(Subcategory.name.in_(subcategoria))
   
    if fabrica:
        filter_group.append(Factory.name.in_(fabrica))

    if categorias:
        filter_group.append(Category.name.in_(categorias))
   
    return filter_group