def index():
    redirect(URL('default','inicio'))
    return locals()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def admin_desktop():

    # Vista para mostrar el listado de personas y organizaciones sugeridas

    if len(request.args) == 0:
        redirect(URL('desktop','admin_desktop', args='persona'))


    return locals()

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_persona():

    # Componente el cual muestra la grilla de personas sugeridas

    label_dict_persona = {'persona.ICN': T('Rut'),
                          'persona.firstLastName': T('Apellido Paterno'
                          ),
                          'persona.otherLastName': T('Apellido Materno'
                          )}

    db.persona.created_by.readable = True
    show_fields_persona = [db.persona.id, db.persona.ICN,
                           db.persona.firstName,
                           db.persona.firstLastName,
                           db.persona.otherLastName,
                           db.persona.state_publication,
                           db.persona.state_collaboration]

    # db.persona.created_by.represent=lambda id,row: db.auth_user(id).username
    
    query = (db.persona.created_by == auth.user_id )

    persona_grid = SQLFORM.grid(  # selectable=lambda ids: redirect(URL('sugerencia',
                                  #         'accept_persona', vars=dict(id=ids))),
        query,
        editable=True,
        details=False,
        deletable=False,
        user_signature=True,
        fields=show_fields_persona,
        create=False,
        headers=label_dict_persona,
        csv=False,
        paginate=10,
        searchable=False,
        formname='persona_grid_form',
        # links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
        #        , _href=URL('editor', 'accept_persona',
        #        vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
        #        _class='w2p_trap button btn', _href=URL('editor',
        #        'reject_persona', vars=dict(id=row.id))),
        #        lambda row: A(T('Programar'), **{'_href':'../load_display_persona#Lightbox_schedulepersona','_class':'w2p_trap button btn programar_persona','_data-toggle':'modal','_id':str(row.id)})]
        )

    if persona_grid.element('.web2py_counter'):
        persona_grid.element('.web2py_counter')[0] = ''

    if persona_grid.element('.web2py_table input[type=submit]'):

        persona_grid.element('.web2py_table input[type=submit]'
                             )['_value'] = \
            T('Aceptar Personas Seleccionadas')

        persona_grid.element('.web2py_table input[type=submit]'
                             )['_class'] = 'buttontext button'
    elif persona_grid.element('.web2py_grid input[type=submit]'):

        persona_grid.element('.web2py_grid input[type=submit]')['_value'
                ] = T('Aceptar')

    return dict(persona_grid=persona_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_organizacion():

    # Componente el cual muestra la grilla de organizaciones sugeridas

    label_dict_organizacion = \
        {'tipoOrganizacion.name': T('Tipo Organización')}

    show_fields_organizacion = [db.Organizacion.id,
                                db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias,
                                db.Organizacion.state_publication,
                                db.Organizacion.state_collaboration]

    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = ((db.Organizacion.tipoOrg != 2) \
        & (db.Organizacion.created_by == auth.user_id ))

    organizacion_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=True,
        deletable=False,
        fields=show_fields_organizacion,
        headers=label_dict_organizacion,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        # links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
        #        , _href=URL('editor', 'accept_organizacion',
        #        vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
        #        _class='w2p_trap button btn', _href=URL('editor',
        #        'reject_organizacion', vars=dict(id=row.id))),
        #        lambda row: A(T('Programar'), **{'_href':'../load_display_organizacion#Lightbox_scheduleorganizacion','_class':'w2p_trap button btn programar_organizacion','_data-toggle':'modal','_id':str(row.id)})],
        links_in_grid=True,
        formname='organizacion_grid_form',
        )

    if organizacion_grid.element('.web2py_counter'):
        organizacion_grid.element('.web2py_counter')[0] = ''

    if organizacion_grid.element('.web2py_table input[type=submit]'):

        organizacion_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Organizaciones Seleccionadas')
    elif organizacion_grid.element('.web2py_grid input[type=submit]'):
        organizacion_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    return dict(organizacion_grid=organizacion_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_empresa():

    label_dict_empresa = \
        {'tipoOrganizacion.name': T('Tipo Organización')}



    # Componente el cual muestra la grilla de empresas sugeridas

    show_fields_empresa = [db.Organizacion.id,
                                db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias,
                                db.Organizacion.state_publication,
                                db.Organizacion.state_collaboration]

    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = ((db.Organizacion.tipoOrg == 2) \
        & (db.Organizacion.created_by == auth.user_id ))

    empresa_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=True,
        deletable=False,
        fields=show_fields_empresa,
        headers=label_dict_empresa,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        # links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
        #        , _href=URL('editor', 'accept_organizacion',
        #        vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
        #        _class='w2p_trap button btn', _href=URL('editor',
        #        'reject_organizacion', vars=dict(id=row.id))),
        #        lambda row: A(T('Programar'), **{'_href':'../load_display_empresa#Lightbox_scheduleempresa#Lightbox_scheduleempresa','_class':'w2p_trap button btn programar_organizacion','_data-toggle':'modal','_id':str(row.id)})],
        links_in_grid=True,
        formname='empresa_grid_form',
        )

    if empresa_grid.element('.web2py_counter'):
        empresa_grid.element('.web2py_counter')[0] = ''

    if empresa_grid.element('.web2py_table input[type=submit]'):

        empresa_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Empresas Seleccionadas')
    elif empresa_grid.element('.web2py_grid input[type=submit]'):
        empresa_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    return dict(empresa_grid=empresa_grid)

@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def display_caso():

    label_dict_empresa = \
        {'tipoOrganizacion.name': T('Tipo Organización')}



    # Componente el cual muestra la grilla de empresas sugeridas

    show_fields_caso = [db.caso.id,
                        db.caso.name,
                        db.caso.country,
                        db.caso.city,
                        db.caso.state_publication,
                        db.caso.state_collaboration]

    # db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = ((db.caso.created_by == auth.user_id ))

    caso_grid = SQLFORM.grid(
        query,
        editable=True,
        details=False,
        user_signature=True,
        deletable=False,
        fields=show_fields_caso,
        # headers=label_dict_empresa,
        create=False,
        csv=False,
        paginate=10,
        searchable=False,
        # links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
        #        , _href=URL('editor', 'accept_caso',
        #        vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
        #        _class='w2p_trap button btn', _href=URL('editor',
        #        'reject_caso', vars=dict(id=row.id))),
        #        lambda row: A(T('Programar'), **{'_href':'../load_display_caso#Lightbox_schedulecaso#Lightbox_schedulecaso','_class':'w2p_trap button btn programar_caso','_data-toggle':'modal','_id':str(row.id)})],
        links_in_grid=True,
        formname='caso_grid_form',
        )

    if caso_grid.element('.web2py_counter'):
        caso_grid.element('.web2py_counter')[0] = ''

    if caso_grid.element('.web2py_table input[type=submit]'):

        caso_grid.element('.web2py_table input[type=submit]'
                                  )['_value'] = \
            T('Aceptar Empresas Seleccionadas')
    elif caso_grid.element('.web2py_grid input[type=submit]'):
        caso_grid.element('.web2py_grid input[type=submit]'
                                  )['_value'] = T('Aceptar')

    return dict(caso_grid=caso_grid)


#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_persona():
    return locals()

#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_organizacion():
    return locals()

#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_empresa():
    return locals()

#funcion auxiliar usada para mostrar el ajax sin que se recargue la pagina completa dentro del div
@auth.requires(auth.has_membership(group_id = 'superadmin') or auth.has_membership(group_id = 'admin') or auth.has_membership(group_id = 'editor'))
def load_display_caso():
    return locals()