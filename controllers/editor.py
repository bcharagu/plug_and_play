@auth.requires_login()
def admin_collaboration():

    # Vista para mostrar el listado de personas y organizaciones sugeridas

    if len(request.args) == 0:
        redirect(URL('editor','admin_collaboration', args='persona'))


    return locals()


def display_persona():

    # Componente el cual muestra la grilla de personas sugeridas

    label_dict_persona = {'persona.ICN': T('Rut'),
                          'persona.firstLastName': T('Apellido Paterno'
                          ),
                          'persona.otherLastName': T('Apellido Materno'
                          )}

    show_fields_persona = [db.persona.id, db.persona.ICN,
                           db.persona.firstName,
                           db.persona.firstLastName,
                           db.persona.otherLastName]

    persona_grid = SQLFORM.grid(  # selectable=lambda ids: redirect(URL('sugerencia',
                                  #         'accept_persona', vars=dict(id=ids))),
        db.persona.state_collaboration != 'for_revision' and db.persona.state_publication == 'draft',
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
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('editor', 'accept_persona',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('editor',
               'reject_persona', vars=dict(id=row.id)))],
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


def accept_persona():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ni una Persona seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_persona = db(db.persona.id == a_id).select().first()
    a_persona.state_publication ='published'
    a_persona.update_record()

    session.flash = T('Colaboración Publicada')
    redirect(URL('display_persona'))

    return dict()

def reject_persona():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las personas seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ni una Persona seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_persona = db(db.persona.id == a_id).select().first()
    a_persona.state_collaboration ='rejected'
    a_persona.state_publication ='draft'
    a_persona.update_record()

    session.flash = T('Colaboración Rechazada')
    redirect(URL('display_persona'))

    return dict()


def display_organizacion():

    # Componente el cual muestra la grilla de organizaciones sugeridas

    label_dict_organizacion = \
        {'tipoOrganizacion.name': T('Tipo Organización')}

    show_fields_organizacion = [db.Organizacion.id,
                                db.Organizacion.tipoOrg,
                                # db.tipoOrganizacion.name,
                                db.Organizacion.hasSocialReason,
                                db.Organizacion.alias]

    db.Organizacion.tipoOrg.represent=lambda id,row: db.tipoOrganizacion(id).name

    query = (db.Organizacion.tipoOrg == db.tipoOrganizacion.id) \
        & (db.Organizacion.state_collaboration != 'for_revision' and db.Organizacion.state_publication == 'draft')

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
        links=[lambda row: A(T('Aceptar'), _class='w2p_trap button btn'
               , _href=URL('editor', 'accept_organizacion',
               vars=dict(id=row.id))), lambda row: A(T('Rechazar'),
               _class='w2p_trap button btn', _href=URL('editor',
               'reject_organizacion', vars=dict(id=row.id)))],
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


def accept_organizacion():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las organizaciones seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ninguna Organizacion seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_org = db(db.Organizacion.id == a_id).select().first()
    a_org.state_publication ='published'
    a_org.state_collaboration ='accepted'
    a_org.update_record()

    session.flash = T('Colaboración Aceptada')
    redirect(URL('display_organizacion'))

    return dict()

def reject_organizacion():

    # Funcion que pasa el estado de colaboracion de revision a aceptado
    # para las organizaciones seleccionadas en la grilla

    if 'id' in request.vars:
        ids_to_accept = request.vars['id']
    else:
        session.flash = T('Ni una Organizacion seleccionada')

    # if len(ids_to_accept) == 1:
    a_id = int(ids_to_accept)
    a_org = db(db.Organizacion.id == a_id).select().first()
    a_org.state_collaboration ='rejected'
    a_org.state_publication ='draft'

    a_org.update_record()

    session.flash = T('Colaboración Rechazada')
    redirect(URL('display_organizacion'))

    return dict()