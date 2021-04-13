from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('Id', show=False)
    user_id = Col('User_id', show=False)
    name = Col('Nome')
    phone = Col('Telefone')
    mail = Col('Email')
    edit = LinkCol('Editar', 'edit_phone', url_kwargs=dict(id='id'))
    delete = LinkCol('Remover', 'delete_phone', url_kwargs=dict(id='id'))